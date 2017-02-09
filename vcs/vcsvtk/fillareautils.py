import vtk
from patterns import pattern_list


def make_patterned_polydata(inputContours, fillareastyle=None,
                            fillareaindex=None, fillareacolors=None,
                            fillareaopacity=None,
                            fillareapixelspacing=None, fillareapixelscale=None,
                            size=None, renderer=None):
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
            fillareapixelspacing = [int(0.015 * x) if int(0.015 * x) > 1 else 1 for x in size]
        else:
            fillareapixelspacing = [15, 15]
    if fillareapixelscale is None:
        fillareapixelscale = 0.8 * min(fillareapixelspacing[0],
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

    xres = yres = 1
    scale = 1.0
    if renderer is not None:
        # Be smart about calculating the resolution by taking the screen pixel
        # size into account
        # First, convert a distance of one unit screen distance to data
        # coordinates
        point1 = [1.0, 1.0, 0.0]
        point2 = [0.0, 0.0, 0.0]
        renderer.SetDisplayPoint(point1)
        renderer.DisplayToWorld()
        wpoint1 = renderer.GetWorldPoint()
        renderer.SetDisplayPoint(point2)
        renderer.DisplayToWorld()
        wpoint2 = renderer.GetWorldPoint()
        diffwpoints = [abs(wpoint1[0] - wpoint2[0]),
                       abs(wpoint1[1] - wpoint2[1])]
        diffwpoints = [1.0 if i < 1e-6 else i for i in diffwpoints]

        # Choosing an arbitary factor to scale the number of points.  A spacing
        # of 10 pixels and a scale of 7.5 pixels was chosen based on visual
        # inspection of result.  Essentially, it means each glyph is 10 pixels
        # away from its neighbors and 7.5 pixels high and wide.
        xres = int(xBounds / (fillareapixelspacing[0] * diffwpoints[0])) + 1
        yres = int(yBounds / (fillareapixelspacing[1] * diffwpoints[1])) + 1
        scale = fillareapixelscale * min(diffwpoints[0], diffwpoints[1])
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
    create_pattern(patternPolyData, scale,
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
    colors = vtk.vtkUnsignedCharArray()
    colors.SetNumberOfComponents(4)
    colors.SetName("Colors")
    clippedPolyData.GetCellData().SetScalars(colors)
    for i in range(clippedPolyData.GetNumberOfCells()):
        colors.InsertNextTypedTuple(color)


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
