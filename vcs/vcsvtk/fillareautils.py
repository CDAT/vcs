
import math
import vtk
import vtk.util.numpy_support as ns
import numpy as np

from .patterns import pattern_list


def affine(value, inMin, inMax, outMin, outMax):
    return ((float(value - inMin) / float(inMax - inMin)) * (outMax - outMin)) + outMin


def computeDiffPoints(sp1, sp2, dataRange, screenGeom):
    # Offsets into data range or screen don't matter
    # because we're just computing differences
    dp1 = [
        affine(sp1[0], 0, screenGeom[0], 0, dataRange[0]),
        affine(sp1[1], 0, screenGeom[1], 0, dataRange[1])
    ]

    dp2 = [
        affine(sp2[0], 0, screenGeom[0], 0, dataRange[0]),
        affine(sp2[1], 0, screenGeom[1], 0, dataRange[1])
    ]

    dx = abs(dp2[0] - dp1[0])
    dy = abs(dp2[1] - dp1[1])

    return [dx, dy]


def computeResolutionAndScale(dataRange, screenGeom, vpScale=[1.0, 1.0],
                              pxScale=None, pxSpacing=None, threshold=1e-6):
    pt1 = [0.0, 0.0]
    pt2 = [1.0, 1.0]
    diffwpoints = computeDiffPoints(pt1, pt2, dataRange, screenGeom)
    diffwpoints = [1.0 if i < threshold else i for i in diffwpoints]
    max_dw = max(*diffwpoints)
    diffwpoints = [max_dw * vpScale[1], max_dw * vpScale[0]]

    # Choosing an arbitary factor to scale the number of points.  A spacing
    # of 10 pixels and a scale of 7.5 pixels was chosen based on visual
    # inspection of result.  Essentially, it means each glyph is 10 pixels
    # away from its neighbors and 7.5 pixels high and wide.
    xres = yres = 1
    scale = [1.0, 1.0]
    if pxSpacing:
        xres = int(dataRange[0] / (pxSpacing[0] * diffwpoints[0])) + 1
        yres = int(dataRange[1] / (pxSpacing[1] * diffwpoints[1])) + 1

    if pxScale:
        scale = [pxScale * x for x in diffwpoints[:2]]

    return ([xres, yres], scale)


def computeMarkerScale(dataRange, screenGeom, pxScale=None):
    pt1 = [0.0, 0.0]
    pt2 = [pxScale, pxScale]
    diffwpoints = computeDiffPoints(pt1, pt2, dataRange, screenGeom)

    dataAspect = abs(float(dataRange[0]) / dataRange[1])
    screenAspect = float(screenGeom[0]) / screenGeom[1]

    scale = max(*diffwpoints)
    if dataAspect > 1:
        scale = min(*diffwpoints)

    return scale


def make_patterned_polydata(inputContours, fillareastyle=None,
                            fillareaindex=None, fillareacolors=None,
                            fillareaopacity=None,
                            fillareapixelspacing=None, fillareapixelscale=None,
                            size=None, screenGeom=None, vpScale=[1.0, 1.0]):
    if inputContours is None or fillareastyle == 'solid':
        return None
    if inputContours.GetNumberOfCells() == 0:
        return None
    if fillareaindex is None:
        fillareaindex = 1
    if fillareaopacity is None:
        fillareaopacity = 100
    if fillareapixelspacing is None:
        if size is not None:
            sp = int(0.015 * min(size[0], size[1]))
            fillareapixelspacing = 2 * [sp if sp > 1 else 1]
        else:
            fillareapixelspacing = [15, 15]
    if fillareapixelscale is None:
        fillareapixelscale = 1.0 * min(fillareapixelspacing[0],
                                       fillareapixelspacing[1])

    # Create a point set laid out on a plane that will be glyphed with the
    # pattern / hatch
    # The bounds of the plane match the bounds of the input polydata
    bounds = inputContours.GetBounds()

    patternPolyData = vtk.vtkPolyData()
    patternPts = vtk.vtkPoints()
    patternPolyData.SetPoints(patternPts)

    xBounds = bounds[1] - bounds[0]
    yBounds = bounds[3] - bounds[2]

    if screenGeom is not None:
        [xres, yres], scale = computeResolutionAndScale([xBounds, yBounds],
                                                        screenGeom,
                                                        vpScale,
                                                        fillareapixelscale,
                                                        fillareapixelspacing)
    else:
        if xBounds <= 1 and yBounds <= 1 and size is not None:
            xBounds *= size[0] / 3
            yBounds *= size[1] / 3

        xres = int(xBounds / 3)
        yres = int(yBounds / 3)

    numPts = (xres + 1) * (yres + 1)
    patternPts.Allocate(numPts)
    normals = vtk.vtkFloatArray()
    normals.SetName("Normals")
    normals.SetNumberOfComponents(3)
    normals.Allocate(3 * numPts)
    tcoords = vtk.vtkFloatArray()
    tcoords.SetName("TextureCoordinates")
    tcoords.SetNumberOfComponents(2)
    tcoords.Allocate(2 * numPts)

    x = [0.0, 0.0, 0.0]
    tc = [0.0, 0.0]
    v1 = [0.0, bounds[3] - bounds[2]]
    v2 = [bounds[1] - bounds[0], 0.0]
    normal = [0.0, 0.0, 1.0]
    numPt = 0
    for i in range(yres + 1):
        tc[0] = i * 1.0 / yres
        for j in range(xres + 1):
            tc[1] = j * 1.0 / xres
            for ii in range(2):
                x[ii] = bounds[2 * ii] + tc[0] * v1[ii] + tc[1] * v2[ii]
            patternPts.InsertPoint(numPt, x)
            tcoords.InsertTuple(numPt, tc)
            normals.InsertTuple(numPt, normal)
            numPt += 1
    patternPolyData.GetPointData().SetNormals(normals)
    patternPolyData.GetPointData().SetTCoords(tcoords)

    # Create the pattern
    scale_max = max(*scale)
    create_pattern(patternPolyData, [scale_max, scale_max],
                   fillareastyle, fillareaindex)

    # Create pipeline to create a clipped polydata from the pattern plane.
    cutter = vtk.vtkCookieCutter()
    cutter.SetInputData(patternPolyData)
    cutter.SetLoopsData(inputContours)
    cutter.Update()

    # Now map the colors as cell scalars.
    # We are doing this here because the vtkCookieCutter does not preserve
    # cell scalars
    map_colors(cutter.GetOutput(), fillareastyle,
               fillareacolors, fillareaopacity)

    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputConnection(cutter.GetOutputPort())
    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    return actor


def map_colors(clippedPolyData, fillareastyle=None,
               fillareacolors=None, fillareaopacity=None):
    if fillareastyle == 'solid':
        return

    if fillareacolors is None:
        fillareacolors = [0, 0, 0]

    if fillareaopacity is None:
        fillareaopacity = 100

    color = [0, 0, 0]
    if fillareastyle == "hatch":
        color = [int(c / 100. * 255) for c in fillareacolors[:3]]
    opacity = int(fillareaopacity / 100. * 255)
    color.append(opacity)

    colorNpArray = np.empty([clippedPolyData.GetNumberOfCells(), 4])
    colorNpArray[:,0] = color[0]
    colorNpArray[:,1] = color[1]
    colorNpArray[:,2] = color[2]
    colorNpArray[:,3] = color[3]

    colors = ns.numpy_to_vtk(num_array=colorNpArray,
                             deep=True,
                             array_type=vtk.VTK_UNSIGNED_CHAR)
    colors.SetName("Colors")
    clippedPolyData.GetCellData().SetScalars(colors)


def create_pattern(patternPolyData, scale=1.0,
                   fillareastyle=None, fillareaindex=None):
    if fillareastyle == 'solid':
        return None

    if fillareaindex is None:
        fillareaindex = 1

    # Create a pattern source image of the given size
    pattern = pattern_list[fillareaindex](patternPolyData, scale=scale,
                                          style=fillareastyle)

    return pattern.render()
