from .pipeline2d import Pipeline2D
from .. import vcs2vtk
from . import fillareautils

import numpy
import vcs
import vtk


class MeshfillPipeline(Pipeline2D):

    """Implementation of the Pipeline interface for VCS meshfill plots."""

    def __init__(self, gm, context_, plot_keyargs):
        super(MeshfillPipeline, self).__init__(gm, context_, plot_keyargs)

        self._needsCellData = True

    def _updateScalarData(self):
        """Overrides baseclass implementation."""
        # We don't trim _data2 for meshfill:
        self._data1 = self._context().trimData2D(self._originalData1)
        _convert = self._gm.yaxisconvert
        _func = vcs.utils.axisConvertFunctions[_convert]["forward"]
        self._data2 = self._originalData2
        self._data2[..., 0, :] = _func(self._data2[..., 0, :])
        _convert = self._gm.xaxisconvert
        _func = vcs.utils.axisConvertFunctions[_convert]["forward"]
        self._data2[..., 1, :] = _func(self._data2[..., 1, :])

    def _updateContourLevelsAndColors(self):
        self._updateContourLevelsAndColorsGeneric()

    def _plotInternal(self):

        prepedContours = self._prepContours()
        tmpLevels = prepedContours["tmpLevels"]
        tmpIndices = prepedContours["tmpIndices"]
        tmpColors = prepedContours["tmpColors"]
        tmpOpacities = prepedContours["tmpOpacities"]

        style = self._gm.fillareastyle
        fareapixelspacing, fareapixelscale = self._patternSpacingAndScale()

        mappers = []
        luts = []
        geos = []
        wholeDataMin, wholeDataMax = vcs.minmax(self._originalData1)
        plotting_dataset_bounds = self.getPlottingBounds()
        x1, x2, y1, y2 = plotting_dataset_bounds
        # We need to do the convertion thing
        _convert = self._gm.yaxisconvert
        _func = vcs.utils.axisConvertFunctions[_convert]["forward"]
        y1 = _func(y1)
        y2 = _func(y2)
        _convert = self._gm.xaxisconvert
        _func = vcs.utils.axisConvertFunctions[_convert]["forward"]
        x1 = _func(x1)
        x2 = _func(x2)
        _colorMap = self.getColorMap()
        for i, l in enumerate(tmpLevels):
            # Ok here we are trying to group together levels can be, a join
            # will happen if: next set of levels contnues where one left off
            # AND pattern is identical
            # TODO this should really just be a single polydata that is
            # colored by scalars:
            for j, color in enumerate(tmpColors[i]):
                mapper = vtk.vtkPolyDataMapper()
                lut = vtk.vtkLookupTable()
                th = vtk.vtkThreshold()
                th.ThresholdBetween(l[j], l[j + 1])
                # th.SetInputConnection(self._vtkPolyDataFilter.GetOutputPort())
                th.SetInputData(self._vtkDataSetFittedToViewport)
                geoFilter2 = vtk.vtkDataSetSurfaceFilter()
                geoFilter2.SetInputConnection(th.GetOutputPort())
                # Make the polydata output available here for patterning later
                geoFilter2.Update()
                geos.append(geoFilter2)
                mapper.SetInputConnection(geoFilter2.GetOutputPort())
                lut.SetNumberOfTableValues(1)
                r, g, b, a = self.getColorIndexOrRGBA(_colorMap, color)
                if style == 'solid':
                    tmpOpacity = tmpOpacities[j]
                    if tmpOpacity is None:
                        tmpOpacity = a / 100.
                    else:
                        tmpOpacity = tmpOpacities[j] / 100.
                    lut.SetTableValue(
                        0, r / 100., g / 100., b / 100., tmpOpacity)
                else:
                    lut.SetTableValue(0, 1., 1., 1., 0.)
                mapper.SetLookupTable(lut)
                mapper.SetScalarRange(l[j], l[j + 1])
                luts.append([lut, [l[j], l[j + 1], True]])
                # Store the mapper only if it's worth it?
                # Need to do it with the whole slab min/max for animation
                # purposes
                if not (l[j + 1] < wholeDataMin or l[j] > wholeDataMax):
                    mappers.append(mapper)

        self._resultDict["vtk_backend_luts"] = luts
        if len(geos) > 0:
            self._resultDict["vtk_backend_geofilters"] = geos

        if self._maskedDataMapper is not None:
            # Note that this is different for meshfill -- others prepend.
            mappers.append(self._maskedDataMapper)

        wireColor = [0, 0, 0, 255]

        # Add a second mapper for wireframe meshfill:
        if self._gm.mesh:
            lineMappers = []
            for polyMapper in mappers:
                edgeFilter = vtk.vtkExtractEdges()
                edgeFilter.SetInputConnection(
                    polyMapper.GetInputConnection(0, 0))

                lineMapper = vtk.vtkPolyDataMapper()
                lineMapper.SetInputConnection(
                    edgeFilter.GetOutputPort(0))

                lineMapper._useWireFrame = True

                lineMappers.append(lineMapper)
            mappers.extend(lineMappers)

        # And now we need actors to actually render this thing
        actors = []
        vp = self._resultDict.get(
            'ratio_autot_viewport',
            [self._template.data.x1, self._template.data.x2,
             self._template.data.y1, self._template.data.y2])
        cti = 0
        ctj = 0

        # view and interactive area
        view = self._context().contextView
        dataset_renderer = view.GetRenderer()
        area = vtk.vtkInteractiveArea()
        view.GetScene().AddItem(area)

        adjusted_plotting_bounds = vcs2vtk.getProjectedBoundsForWorldCoords(plotting_dataset_bounds, self._gm.projection)
        drawAreaBounds = vcs2vtk.computeDrawAreaBounds(adjusted_plotting_bounds)

        [renWinWidth, renWinHeight] = self._context().renWin.GetSize()
        geom = vtk.vtkRecti(int(vp[0] * renWinWidth), int(vp[2] * renWinHeight), int((vp[1] - vp[0]) * renWinWidth), int((vp[3] - vp[2]) * renWinHeight))

        vcs2vtk.configureContextArea(area, drawAreaBounds, geom)

        mIdx = 0

        for mapper in mappers:
            act = vtk.vtkActor()
            act.SetMapper(mapper)
            mapper.Update()
            poly = mapper.GetInput()

            item = None

            wireframe = False
            if hasattr(mapper, "_useWireFrame"):
                wireframe = True

            if wireframe:
                item = vtk.vtkPolyDataItem()
                item.SetPolyData(poly)

                colorArray = vtk.vtkUnsignedCharArray()
                colorArray.SetNumberOfComponents(4)
                for i in range(poly.GetNumberOfCells()):
                    colorArray.InsertNextTypedTuple(wireColor)

                item.SetScalarMode(vtk.VTK_SCALAR_MODE_USE_CELL_DATA)
                item.SetMappedColors(colorArray)
                area.GetDrawAreaItem().AddItem(item)
            elif style == "solid":
                if self._needsCellData:
                    attrs = poly.GetCellData()
                else:
                    attrs = poly.GetPointData()

                data = attrs.GetScalars()
                deleteColors = False

                if data:
                    lut = mapper.GetLookupTable()
                    scalarRange = mapper.GetScalarRange()
                    lut.SetRange(scalarRange)
                    mappedColors = lut.MapScalars(data, vtk.VTK_COLOR_MODE_DEFAULT, 0)
                    deleteColors = True
                else:
                    loc = 'point'
                    numTuples = poly.GetNumberOfPoints()
                    if self._needsCellData:
                        loc = 'cell'
                        numTuples = poly.GetNumberOfCells()
                    print('WARNING: meshfill pipeline: poly does not have Scalars array on {0} data, using solid color'.format(loc))
                    color = [0, 0, 0, 255]
                    mappedColors = vcs2vtk.generateSolidColorArray(numTuples, color)

                mappedColors.SetName('Colors')

                item = vtk.vtkPolyDataItem()
                item.SetPolyData(poly)

                if self._needsCellData:
                    item.SetScalarMode(vtk.VTK_SCALAR_MODE_USE_CELL_DATA)
                else:
                    item.SetScalarMode(vtk.VTK_SCALAR_MODE_USE_POINT_DATA)

                item.SetMappedColors(mappedColors)
                if deleteColors:
                    mappedColors.FastDelete()
                area.GetDrawAreaItem().AddItem(item)

            # TODO See comment in boxfill.
            if item is not None:
                if mapper is self._maskedDataMapper:
                    actors.append([item, self._maskedDataMapper, plotting_dataset_bounds])
                else:
                    actors.append([item, plotting_dataset_bounds])

            if mapper is not self._maskedDataMapper:

                if not wireframe:
                    # Since pattern creation requires a single color, assuming the
                    # first
                    if ctj >= len(tmpColors[cti]):
                        ctj = 0
                        cti += 1
                    c = self.getColorIndexOrRGBA(_colorMap, tmpColors[cti][ctj])

                    patact = fillareautils.make_patterned_polydata(poly,
                                                                   fillareastyle=style,
                                                                   fillareaindex=tmpIndices[cti],
                                                                   fillareacolors=c,
                                                                   fillareaopacity=tmpOpacities[cti],
                                                                   fillareapixelspacing=fareapixelspacing,
                                                                   fillareapixelscale=fareapixelscale,
                                                                   size=self._context().renWin.GetSize(),
                                                                   screenGeom=self._context().renWin.GetSize())
                    ctj += 1
                if patact is not None:
                    actors.append([patact, plotting_dataset_bounds])

                    patMapper = patact.GetMapper()
                    patMapper.Update()
                    patPoly = patMapper.GetInput()

                    patItem = vtk.vtkPolyDataItem()
                    patItem.SetPolyData(patPoly)

                    patItem.SetScalarMode(vtk.VTK_SCALAR_MODE_USE_CELL_DATA)
                    colorArray = patPoly.GetCellData().GetArray('Colors')

                    patItem.SetMappedColors(colorArray)
                    area.GetDrawAreaItem().AddItem(patItem)

                    actors.append([patItem, plotting_dataset_bounds])

        t = self._originalData1.getTime()
        if self._originalData1.ndim > 2:
            z = self._originalData1.getAxis(-3)
        else:
            z = None
        self._resultDict["vtk_backend_actors"] = actors
        kwargs = {
            "vtk_backend_grid": self._vtkDataSet,
            "dataset_bounds": self._vtkDataSetBounds,
            "plotting_dataset_bounds": plotting_dataset_bounds,
            "vtk_dataset_bounds_no_mask": self._vtkDataSetBoundsNoMask,
            "vtk_backend_geo": self._vtkGeoTransform,
            "vtk_backend_draw_area_bounds": drawAreaBounds,
            "vtk_backend_viewport_scale": [
                self._context_xScale,
                self._context_yScale
            ]
        }
        if ("ratio_autot_viewport" in self._resultDict):
            kwargs["ratio_autot_viewport"] = vp
        self._resultDict.update(self._context().renderTemplate(self._template, self._data1, self._gm,
                                t, z,
                                X=numpy.arange(min(x1, x2),
                                               max(x1, x2) * 1.1,
                                               abs(x2 - x1) / 10.),
                                Y=numpy.arange(min(y1, y2),
                                               max(y1, y2) * 1.1,
                                               abs(y2 - y1) / 10.), **kwargs))

        legend = getattr(self._gm, "legend", None)

        if self._gm.ext_1:
            if isinstance(self._contourLevels[0], list):
                if numpy.less(abs(self._contourLevels[0][0]), 1.e20):
                    # Ok we need to add the ext levels
                    self._contourLevels.insert(
                        0, [-1.e20, self._contourLevels[0][0]])
            else:
                if numpy.less(abs(self._contourLevels[0]), 1.e20):
                    # need to add an ext
                    self._contourLevels.insert(0, -1.e20)
        if self._gm.ext_2:
            if isinstance(self._contourLevels[-1], list):
                if numpy.less(abs(self._contourLevels[-1][1]), 1.e20):
                    # need ext
                    self._contourLevels.append([self._contourLevels[-1][1],
                                                1.e20])
            else:
                if numpy.less(abs(self._contourLevels[-1]), 1.e20):
                    # need exts
                    self._contourLevels.append(1.e20)

        patternArgs = {}
        patternArgs['style'] = self._gm.fillareastyle
        patternArgs['index'] = self._gm.fillareaindices
        if patternArgs['index'] is None:
            patternArgs['index'] = [1, ]
        # Compensate for the different viewport size of the colorbar
        patternArgs['opacity'] = self._gm.fillareaopacity
        patternArgs['pixelspacing'] = [int(fareapixelspacing[0] / (vp[1] - vp[0])),
                                       int(fareapixelspacing[1] / (vp[3] - vp[2]))]
        patternArgs['pixelscale'] = fareapixelscale / (vp[1] - vp[0])
        self._resultDict.update(
            self._context().renderColorBar(self._template, self._contourLevels,
                                           self._contourColors,
                                           legend,
                                           self.getColorMap(),
                                           **patternArgs))

        projection = vcs.elements["projection"][self._gm.projection]
        kwargs['xaxisconvert'] = self._gm.xaxisconvert
        kwargs['yaxisconvert'] = self._gm.yaxisconvert
        self._context().plotContinents(self._plot_kargs.get("continents", self._useContinents),
                                       plotting_dataset_bounds, projection,
                                       self._dataWrapModulo,
                                       vp, self._template.data.priority, **kwargs)

    def getPlottingBounds(self):
        """gm.datawc if it is set or dataset_bounds
        """
        if (self._vtkGeoTransform):
            return vcs2vtk.getWrappedBounds(
                [self._gm.datawc_x1, self._gm.datawc_x2, self._gm.datawc_y1, self._gm.datawc_y2],
                self._vtkDataSetBounds, self._dataWrapModulo)
        else:
            return vcs2vtk.getPlottingBounds(
                [self._gm.datawc_x1, self._gm.datawc_x2, self._gm.datawc_y1, self._gm.datawc_y2],
                self._vtkDataSetBounds, self._vtkGeoTransform)
