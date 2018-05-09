from .pipeline2d import Pipeline2D
from . import fillareautils

import numpy
import vcs
import vtk


class BoxfillPipeline(Pipeline2D):

    """Implementation of the Pipeline interface for VCS boxfill plots.

    Internal variables:
        - self._contourLabels: Contour labels.
        - self._mappers: Mappers produced by this pipeline.
            TODO _mappers should be removed and replaced by a more specific
            set of ivars (at minimum, identify what the mappers are rendering).
    """

    def __init__(self, gm, context_, plot_keyargs):
        super(BoxfillPipeline, self).__init__(gm, context_, plot_keyargs)

        self._contourLabels = None
        self._mappers = None
        self._customBoxfillArgs = {}
        self._needsCellData = True

    def _updateScalarData(self):
        """Overrides baseclass implementation."""
        # Update data1 if this is a log10 boxfill:
        data = self._originalData1.clone()
        X = self.convertAxis(data.getAxis(-1), "x")
        Y = self.convertAxis(data.getAxis(-2), "y")
        data.setAxis(-1, X)
        data.setAxis(-2, Y)
        if self._gm.boxfill_type == "log10":
            data = numpy.ma.log10(data)

        self._data1 = self._context().trimData2D(data)
        self._data2 = self._context().trimData2D(self._originalData2)

    def _updateContourLevelsAndColors(self):
        """Overrides baseclass implementation."""
        if self._gm.boxfill_type != "custom":
            self._updateContourLevelsAndColorsForBoxfill()
        else:
            self._updateContourLevelsAndColorsGeneric()

        if isinstance(self._contourLevels, numpy.ndarray):
            self._contourLevels = self._contourLevels.tolist()

    def _updateContourLevelsAndColorsForBoxfill(self):
        """Set contour information for a standard boxfill."""
        self._contourLevels = self._gm.getlevels(self._scalarRange[0], self._scalarRange[1])
        self._contourLabels = self._gm.getlegendlabels(self._contourLevels)
        # Use consecutive colors:
        self._contourColors = list(range(self._gm.color_1, self._gm.color_2 + 1))

    def _plotInternal(self):
        """Overrides baseclass implementation."""
        # Special case for custom boxfills:
        if self._gm.boxfill_type != "custom":
            self._plotInternalBoxfill()
        else:
            self._plotInternalCustomBoxfill()

        if self._maskedDataMapper is not None:
            self._mappers.insert(0, self._maskedDataMapper)

        plotting_dataset_bounds = self.getPlottingBounds()
        x1, x2, y1, y2 = plotting_dataset_bounds

        # And now we need actors to actually render this thing
        actors = []
        cti = 0
        ctj = 0
        _colorMap = self.getColorMap()
        _style = self._gm.fillareastyle
        vp = self._resultDict.get(
            'ratio_autot_viewport',
            [self._template.data.x1, self._template.data.x2,
             self._template.data.y1, self._template.data.y2])
        dataset_renderer = None
        fareapixelspacing, fareapixelscale = self._patternSpacingAndScale()

        # view and interactive area
        view = vtk.vtkContextView()
        view.SetRenderWindow(self._context().renWin)
        area = vtk.vtkInteractiveArea()
        view.GetScene().AddItem(area)

        for mapper in self._mappers:
            act = vtk.vtkActor()
            act.SetMapper(mapper)

            # create a new renderer for this mapper
            # (we need one for each mapper because of camera flips)
            # if not dataset_renderer:
            dataset_renderer, xScale, yScale = self._context().fitToViewport(
                act, vp,
                wc=plotting_dataset_bounds, geoBounds=self._vtkDataSetBoundsNoMask,
                geo=self._vtkGeoTransform,
                priority=self._template.data.priority,
                create_renderer=(dataset_renderer is None),
                add_actor=(_style == "solid"))

            rect = vtk.vtkRectd(self._vtkDataSetBoundsNoMask[0], self._vtkDataSetBoundsNoMask[2],
                                self._vtkDataSetBoundsNoMask[1] - self._vtkDataSetBoundsNoMask[0],
                                self._vtkDataSetBoundsNoMask[3] - self._vtkDataSetBoundsNoMask[2])
            mapper.Update()
            poly = mapper.GetInput()
            # create poly item
            item = vtk.vtkPolyDataItem()
            item.SetPolyData(poly)
            if self._needsCellData:
                item.SetScalarMode(vtk.VTK_SCALAR_MODE_USE_CELL_DATA)
                data = poly.GetCellData().GetScalars()
            else:
                item.SetScalarMode(vtk.VTK_SCALAR_MODE_USE_POINT_DATA)
                data = poly.GetPointData().GetScalars()
            lut = mapper.GetLookupTable()
            range = mapper.GetScalarRange()
            lut.SetRange(range)
            mappedColors = lut.MapScalars(data, vtk.VTK_COLOR_MODE_DEFAULT, 0)
            item.SetMappedColors(mappedColors)
            area.SetDrawAreaBounds(rect)
            area.GetDrawAreaItem().AddItem(item)
            area.SetShowGrid(False)
            axisLeft = area.GetAxis(vtk.vtkAxis.LEFT)
            axisRight = area.GetAxis(vtk.vtkAxis.RIGHT)
            axisBottom = area.GetAxis(vtk.vtkAxis.BOTTOM)
            axisTop = area.GetAxis(vtk.vtkAxis.TOP)
            axisTop.SetVisible(False)
            axisRight.SetVisible(False)
            axisLeft.SetVisible(False)
            axisBottom.SetVisible(False)
            # axis = self._data1.getAxisList()[0]
            # axisLeft.SetTitle(axis.id)
            # axis = self._data1.getAxisList()[1]
            # axisBottom.SetTitle(axis.id)

            # adjust the viewport
            device = view.GetContext().GetDevice()
            device.Begin(view.GetRenderer())
            rectLeft = axisLeft.GetBoundingRect(view.GetContext())
            rectRight = axisRight.GetBoundingRect(view.GetContext())
            rectTop = axisTop.GetBoundingRect(view.GetContext())
            rectBottom = axisBottom.GetBoundingRect(view.GetContext())
            device.End()
            xmin = vp[0] - rectLeft.GetWidth() / self._context().renWin.GetSize()[0]
            xmax = vp[1] + rectRight.GetWidth() / self._context().renWin.GetSize()[0]
            ymin = vp[2] - rectBottom.GetHeight() / self._context().renWin.GetSize()[1]
            ymax = vp[3] + rectTop.GetHeight() / self._context().renWin.GetSize()[1]

            # xmin, ymin, xmax, ymax
            dataset_renderer = view.GetRenderer()
            dataset_renderer.SetViewport(xmin, ymin, xmax, ymax)

            # TODO We shouldn't need this conditional branch, the 'else' body
            # should be used and GetMapper called to get the mapper as needed.
            # If this is needed for other reasons, we need a comment explaining
            # why.
            if mapper is self._maskedDataMapper:
                actors.append([act, self._maskedDataMapper, plotting_dataset_bounds])
            else:
                actors.append([act, plotting_dataset_bounds])

                if self._gm.boxfill_type == "custom":
                    # Patterns/hatches creation for custom boxfill plots
                    patact = None

                    tmpColors = self._customBoxfillArgs["tmpColors"]
                    if ctj >= len(tmpColors[cti]):
                        ctj = 0
                        cti += 1
                    # Since pattern creation requires a single color, assuming the first
                    c = self.getColorIndexOrRGBA(_colorMap, tmpColors[cti][ctj])

                    patact = fillareautils.make_patterned_polydata(
                        mapper.GetInput(),
                        fillareastyle=_style,
                        fillareaindex=self._customBoxfillArgs["tmpIndices"][cti],
                        fillareacolors=c,
                        fillareaopacity=self._customBoxfillArgs["tmpOpacities"][cti],
                        fillareapixelspacing=fareapixelspacing,
                        fillareapixelscale=fareapixelscale,
                        size=self._context().renWin.GetSize(),
                        renderer=dataset_renderer)

                    ctj += 1

                    if patact is not None:
                        dataset_renderer.AddActor(patact)
                        actors.append([patact, plotting_dataset_bounds])

        self._resultDict["vtk_backend_actors"] = actors

        t = self._originalData1.getTime()
        if self._originalData1.ndim > 2:
            z = self._originalData1.getAxis(-3)
        else:
            z = None
        kwargs = {"vtk_backend_grid": self._vtkDataSet,
                  "dataset_bounds": self._vtkDataSetBounds,
                  "plotting_dataset_bounds": plotting_dataset_bounds,
                  "vtk_dataset_bounds_no_mask": self._vtkDataSetBoundsNoMask,
                  "vtk_backend_geo": self._vtkGeoTransform}
        if ("ratio_autot_viewport" in self._resultDict):
            kwargs["ratio_autot_viewport"] = vp
        self._resultDict.update(self._context().renderTemplate(
            self._template,
            self._data1,
            self._gm, t, z, **kwargs))

        if getattr(self._gm, "legend", None) is not None:
            self._contourLabels = self._gm.legend

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

        # Do not pass patterning parameters for color bar rendering if the
        # boxfill type is non-custom
        patternArgs = {}
        if self._gm.boxfill_type == "custom":
            patternArgs['style'] = self._gm.fillareastyle
            patternArgs['index'] = self._gm.fillareaindices
            patternArgs['opacity'] = self._gm.fillareaopacity
            # Compensate for the different viewport size of the colorbar
            patternArgs['pixelspacing'] = [int(fareapixelspacing[0] / (vp[1] - vp[0])),
                                           int(fareapixelspacing[1] / (vp[3] - vp[2]))]
            patternArgs['pixelscale'] = fareapixelscale / (vp[1] - vp[0])

        self._resultDict.update(
            self._context().renderColorBar(self._template, self._contourLevels,
                                           self._contourColors,
                                           self._contourLabels,
                                           self.getColorMap(),
                                           **patternArgs))

        projection = vcs.elements["projection"][self._gm.projection]
        kwargs['xaxisconvert'] = self._gm.xaxisconvert
        kwargs['yaxisconvert'] = self._gm.yaxisconvert
        if self._data1.getAxis(-1).isLongitude() and self._data1.getAxis(-2).isLatitude():
            self._context().plotContinents(self._plot_kargs.get("continents", self._useContinents),
                                           plotting_dataset_bounds, projection,
                                           self._dataWrapModulo,
                                           vp, self._template.data.priority, **kwargs)

    def _plotInternalBoxfill(self):
        """Implements the logic to render a non-custom boxfill."""
        # Prep mapper
        mapper = vtk.vtkPolyDataMapper()
        self._mappers = [mapper]

        if self._gm.ext_1 and self._gm.ext_2:
            mapper.SetInputConnection(self._vtkPolyDataFilter.GetOutputPort())
            self._resultDict["vtk_backend_geofilters"] = \
                [self._vtkPolyDataFilter]
        else:
            thr = vtk.vtkThreshold()
            thr.SetInputConnection(self._vtkPolyDataFilter.GetOutputPort())
            if not self._gm.ext_1 and not self._gm.ext_2:
                thr.ThresholdBetween(self._contourLevels[0],
                                     self._contourLevels[-1])
            elif self._gm.ext_1 and not self._gm.ext_2:
                thr.ThresholdByLower(self._contourLevels[-1])
            elif not self._gm.ext_1 and self._gm.ext_2:
                thr.ThresholdByUpper(self._contourLevels[0])

            geoFilter2 = vtk.vtkDataSetSurfaceFilter()
            geoFilter2.SetInputConnection(thr.GetOutputPort())
            mapper.SetInputConnection(geoFilter2.GetOutputPort())
            self._resultDict["vtk_backend_geofilters"] = [geoFilter2]

        # Colortable bit
        # make sure length match
        numLevels = len(self._contourLevels) - 1
        while len(self._contourColors) < numLevels:
            self._contourColors.append(self._contourColors[-1])

        lut = vtk.vtkLookupTable()
        lut.SetNumberOfTableValues(numLevels)
        _colorMap = self.getColorMap()
        for i in range(numLevels):
            r, g, b, a = self.getColorIndexOrRGBA(_colorMap, self._contourColors[i])
            lut.SetTableValue(i, r / 100., g / 100., b / 100., a / 100.)

        mapper.SetLookupTable(lut)
        if numpy.allclose(self._contourLevels[0], -1.e20):
            lmn = self._min - 1.
        else:
            lmn = self._contourLevels[0]
        if numpy.allclose(self._contourLevels[-1], 1.e20):
            lmx = self._mx + 1.
        else:
            lmx = self._contourLevels[-1]
        mapper.SetScalarRange(lmn, lmx)
        self._resultDict["vtk_backend_luts"] = [[lut, [lmn, lmx, True]]]

    def _plotInternalCustomBoxfill(self):
        """Implements the logic to render a custom boxfill."""
        self._mappers = []

        self._customBoxfillArgs = self._prepContours()
        tmpLevels = self._customBoxfillArgs["tmpLevels"]
        tmpColors = self._customBoxfillArgs["tmpColors"]
        tmpOpacities = self._customBoxfillArgs["tmpOpacities"]

        style = self._gm.fillareastyle

        luts = []
        geos = []
        wholeDataMin, wholeDataMax = vcs.minmax(self._originalData1)
        _colorMap = self.getColorMap()
        for i, l in enumerate(tmpLevels):
            # Ok here we are trying to group together levels can be, a join
            # will happen if: next set of levels continues where one left off
            # AND pattern is identical

            # TODO this should really just be a single polydata/mapper/actor:
            for j, color in enumerate(tmpColors[i]):
                mapper = vtk.vtkPolyDataMapper()
                lut = vtk.vtkLookupTable()
                th = vtk.vtkThreshold()
                th.ThresholdBetween(l[j], l[j + 1])
                th.SetInputConnection(self._vtkPolyDataFilter.GetOutputPort())
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
                    lut.SetTableValue(0, r / 100., g / 100., b / 100., tmpOpacity)
                else:
                    lut.SetTableValue(0, 1., 1., 1., 0.)
                mapper.SetLookupTable(lut)
                mapper.SetScalarRange(l[j], l[j + 1])
                luts.append([lut, [l[j], l[j + 1], False]])
                # Store the mapper only if it's worth it?
                # Need to do it with the whole slab min/max for animation
                # purposes
                if not (l[j + 1] < wholeDataMin or l[j] > wholeDataMax):
                    self._mappers.append(mapper)

        self._resultDict["vtk_backend_luts"] = luts
        if len(geos) > 0:
            self._resultDict["vtk_backend_geofilters"] = geos
