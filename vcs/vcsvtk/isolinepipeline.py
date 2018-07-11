from .pipeline2d import Pipeline2D
from .. import vcs2vtk

import numpy
import vcs
import vtk


def getPaintHandler(paintAttrs):
    print('Have paintAttrs when creating handler: ', paintAttrs)

    @vtk.calldata_type(vtk.VTK_OBJECT)
    def onPaintEvent(object, event, context2DPainter):
        pen = context2DPainter.GetPen()

        oldLineType = pen.GetLineType()
        oldLineWidth = pen.GetWidth()

        pen.SetLineType(paintAttrs['stippleType'])
        pen.SetWidth(paintAttrs['lineWidth'])

        poly = paintAttrs['poly']
        colors = paintAttrs['colors']
        mode = paintAttrs['mode']
        context2DPainter.DrawPolyData(0, 0, poly, colors, mode)

        pen.SetLineType(oldLineType)
        pen.SetWidth(oldLineWidth)

    return onPaintEvent


class IsolinePipeline(Pipeline2D):

    """Implementation of the Pipeline interface for VCS isoline plots."""

    def __init__(self, gm, context_, plot_keyargs):
        super(IsolinePipeline, self).__init__(gm, context_, plot_keyargs)
        self._needsCellData = False

    def extendAttribute(self, attributes, default):
        if len(attributes) < len(self._contourLevels):
            if (len(attributes) == 0):
                attributeValue = default
            else:
                attributeValue = attributes[-1]
            attributes += [attributeValue] * (len(self._contourLevels) - len(attributes))

    def _updateContourLevelsAndColors(self):
        """Overrides baseclass implementation."""
        # Contour values:
        self._contourLevels = self._gm.levels
        if numpy.allclose(self._contourLevels[0], [0., 1.e20]) or \
           numpy.allclose(self._contourLevels, 1.e20):
            self._contourLevels = vcs.mkscale(self._scalarRange[0],
                                              self._scalarRange[1])
            if len(self._contourLevels) == 1:  # constant value ?
                self._contourLevels = [self._contourLevels[0],
                                       self._contourLevels[0] + .00001]
        else:
            if isinstance(self._gm.levels[0], (list, tuple)):
                self._contourLevels = [x[0] for x in self._gm.levels]
            else:
                if numpy.allclose(self._contourLevels[0], 1.e20):
                    self._contourLevels[0] = -1.e20
        self._contourColors = self._gm.linecolors
        self.extendAttribute(self._contourColors, default='black')

    def _plotInternal(self):
        """Overrides baseclass implementation."""
        tmpLevels = []
        tmpColors = []
        tmpLineWidths = []
        tmpLineTypes = []

        linewidth = self._gm.linewidths
        self.extendAttribute(linewidth, default=1.0)

        linetype = self._gm.linetypes
        self.extendAttribute(linetype, default='solid')

        plotting_dataset_bounds = self.getPlottingBounds()
        x1, x2, y1, y2 = plotting_dataset_bounds

        for i, lv_tmp in enumerate(self._contourLevels):
            if i == 0:
                W = linewidth[i]
                S = linetype[i]
                C = [self._contourColors[i]]
                if lv_tmp == 1.e20:
                    L = [-1.e20]
                else:
                    L = [lv_tmp]
            else:
                if W == linewidth[i] and S == linetype[i]:
                    # Ok same style and width, lets keep going
                    L.append(lv_tmp)
                    C.append(self._contourColors[i])
                else:
                    tmpLevels.append(L)
                    tmpColors.append(C)
                    tmpLineWidths.append(W)
                    tmpLineTypes.append(S)
                    L = [lv_tmp]
                    C = [self._contourColors[i]]
                    W = linewidth[i]
                    S = linetype[i]

        tmpLevels.append(L)
        tmpColors.append(C)
        tmpLineWidths.append(W)
        tmpLineTypes.append(S)

        cots = []
        textprops = []
        luts = []

        actors = []
        mappers = []

        if self._gm.label and (self._gm.text or self._gm.textcolors):
            # Text objects:
            if self._gm.text:
                texts = self._gm.text
                while len(texts) < len(self._contourLevels):
                    texts.append(texts[-1])
            else:
                texts = [None] * len(self._contourLevels)

            # Custom colors:
            if self._gm.textcolors:
                colorOverrides = self._gm.textcolors
                while len(colorOverrides) < len(self._contourLevels):
                    colorOverrides.append(colorOverrides[-1])
            else:
                colorOverrides = [None] * len(self._gm.text)

            # Custom background colors and opacities:
            backgroundColors = self._gm.labelbackgroundcolors
            if backgroundColors:
                while len(backgroundColors) < len(self._contourLevels):
                    backgroundColors.append(backgroundColors[-1])
            backgroundOpacities = self._gm.labelbackgroundopacities
            if backgroundOpacities:
                while len(backgroundOpacities) < len(self._contourLevels):
                    backgroundOpacities.append(backgroundOpacities[-1])

        countLevels = 0
        vp = self._resultDict.get(
            'ratio_autot_viewport',
            [self._template.data.x1, self._template.data.x2,
             self._template.data.y1, self._template.data.y2])


        # view and interactive area
        view = self._context().contextView
        dataset_renderer = view.GetRenderer()
        area = vtk.vtkInteractiveArea()
        view.GetScene().AddItem(area)

        rect = vtk.vtkRectd(self._vtkDataSetBoundsNoMask[0], self._vtkDataSetBoundsNoMask[2],
                            self._vtkDataSetBoundsNoMask[1] - self._vtkDataSetBoundsNoMask[0],
                            self._vtkDataSetBoundsNoMask[3] - self._vtkDataSetBoundsNoMask[2])

        [renWinWidth, renWinHeight] = self._context().renWin.GetSize()
        geom = vtk.vtkRecti(int(vp[0] * renWinWidth), int(vp[2] * renWinHeight), int((vp[1] - vp[0]) * renWinWidth), int((vp[3] - vp[2]) * renWinHeight))

        area.SetDrawAreaBounds(rect)
        area.SetGeometry(geom)
        area.SetFillViewport(False)
        area.SetShowGrid(False)

        axisLeft = area.GetAxis(vtk.vtkAxis.LEFT)
        axisRight = area.GetAxis(vtk.vtkAxis.RIGHT)
        axisBottom = area.GetAxis(vtk.vtkAxis.BOTTOM)
        axisTop = area.GetAxis(vtk.vtkAxis.TOP)

        axisLeft.SetVisible(False)
        axisRight.SetVisible(False)
        axisBottom.SetVisible(False)
        axisTop.SetVisible(False)

        axisLeft.SetMargins(0, 0)
        axisRight.SetMargins(0, 0)
        axisBottom.SetMargins(0, 0)
        axisTop.SetMargins(0, 0)

        for i, l in enumerate(tmpLevels):
            numLevels = len(l)

            cot = vtk.vtkContourFilter()
            # if self._hasCellData:
            #     cot.SetInputConnection(self._vtkPolyDataFilter.GetOutputPort())
            # else:
            #     cot.SetInputData(self._vtkDataSet)

            cot.SetInputData(self._vtkDataSetFittedToViewport)
            cot.SetNumberOfContours(numLevels)

            for n in range(numLevels):
                cot.SetValue(n, l[n])
            # TODO remove update
            cot.Update()

            lut = vtk.vtkLookupTable()
            lut.SetNumberOfTableValues(len(tmpColors[i]))
            cmap = self.getColorMap()
            for n, col in enumerate(tmpColors[i]):
                r, g, b, a = self.getColorIndexOrRGBA(cmap, col)
                lut.SetTableValue(n, r / 100., g / 100., b / 100., a / 100.)

            # Setup isoline labels
            if self._gm.label:
                # Setup label mapping array:
                tpropMap = vtk.vtkDoubleArray()
                tpropMap.SetNumberOfComponents(1)
                tpropMap.SetNumberOfTuples(numLevels)
                for n, val in enumerate(l):
                    tpropMap.SetTuple(n, [val])

                # Prep text properties:
                tprops = vtk.vtkTextPropertyCollection()
                if self._gm.text or self._gm.textcolors:
                    ttexts = texts[countLevels:(countLevels + len(l))]

                    for idx, tc in enumerate(ttexts):
                        if vcs.queries.istextcombined(tc):
                            tt, to = tuple(tc.name.split(":::"))
                        elif tc is None:
                            tt = "default"
                            to = "default"
                        elif vcs.queries.istexttable(tc):
                            tt = tc.name
                            to = "default"
                        elif vcs.queries.istextorientation(tc):
                            to = tc.name
                            tt = "default"
                        elif isinstance(tc, str):
                            sp = tc.split(":::")
                            if len(sp) == 2:
                                tt = sp[0]
                                to = sp[1]
                            else:  # Hum don't know what do do with this
                                if sp[0] in vcs.listelements("textcombined"):
                                    tc = vcs.gettextcombined(tc)
                                    tt, to = tuple(tc.name.split(":::"))
                                elif sp[0] in vcs.listelements("textorientation"):
                                    to = sp[0]
                                    tt = "default"
                                elif sp[0] in vcs.listelements("texttable"):
                                    tt = sp[0]
                                    to = "default"

                        colorOverride = colorOverrides[countLevels + idx]
                        if colorOverride is not None:
                            tt = vcs.createtexttable(None, tt)
                            tt.color = colorOverride
                            tt = tt.name
                        if backgroundColors is not None:
                            texttbl = vcs.gettexttable(tt)
                            texttbl.backgroundcolor = backgroundColors[countLevels + idx]
                        if backgroundOpacities is not None:
                            texttbl = vcs.gettexttable(tt)
                            texttbl.backgroundopacity = backgroundOpacities[countLevels + idx]
                        tprop = vtk.vtkTextProperty()
                        vcs2vtk.prepTextProperty(tprop,
                                                 self._context().renWin.GetSize(),
                                                 to, tt, cmap=cmap)
                        tprops.AddItem(tprop)
                        if colorOverride is not None:
                            del(vcs.elements["texttable"][tt])
                else:  # No text properties specified. Use the default:
                    tprop = vtk.vtkTextProperty()
                    vcs2vtk.prepTextProperty(tprop,
                                             self._context().renWin.GetSize(),
                                             cmap=cmap)
                    tprops.AddItem(tprop)
                textprops.append(tprops)

                mapper = vtk.vtkLabeledContourMapper()
                mapper.SetTextProperties(tprops)
                mapper.SetTextPropertyMapping(tpropMap)
                mapper.SetLabelVisibility(1)
                mapper.SetSkipDistance(self._gm.labelskipdistance)

                pdMapper = mapper.GetPolyDataMapper()

                luts.append([lut, [l[0], l[-1], False]])
            else:  # No isoline labels:
                mapper = vtk.vtkPolyDataMapper()
                pdMapper = mapper
                luts.append([lut, [l[0], l[-1], False]])
            pdMapper.SetLookupTable(lut)
            pdMapper.SetScalarRange(l[0], l[-1])
            pdMapper.SetScalarModeToUsePointData()

            stripper = vtk.vtkStripper()
            stripper.SetInputConnection(cot.GetOutputPort())
            mapper.SetInputConnection(stripper.GetOutputPort())
            # TODO remove update, make pipeline
            stripper.Update()
            poly = stripper.GetOutput()
            mappers.append(mapper)
            cots.append(cot)

            # Create actor to add to scene
            act = vtk.vtkActor()
            # act.SetMapper(mapper)
            # # Set line properties here
            # p = act.GetProperty()
            # p.SetLineWidth(tmpLineWidths[i])
            # vcs2vtk.stippleLine(p, tmpLineTypes[i])

            actors.append([act, plotting_dataset_bounds])

            # create a new renderer for this mapper
            # (we need one for each mapper because of cmaera flips)
            # dataset_renderer, xScale, yScale = self._context().fitToViewport(
            #     act, vp,
            #     wc=plotting_dataset_bounds, geoBounds=self._vtkDataSetBoundsNoMask,
            #     geo=self._vtkGeoTransform,
            #     priority=self._template.data.priority,
            #     create_renderer=(dataset_renderer is None))


            if self._needsCellData:
                attrs = poly.GetCellData()
                scalarMode = vtk.VTK_SCALAR_MODE_USE_CELL_DATA
            else:
                attrs = poly.GetPointData()
                scalarMode = vtk.VTK_SCALAR_MODE_USE_POINT_DATA

            data = attrs.GetScalars()
            mappedColors = lut.MapScalars(data, vtk.VTK_COLOR_MODE_DEFAULT, 0)

            customItem = vtk.vtkPaintNotifierItem()
            attrs = {
                'contextItem': customItem,
                'poly': poly,
                'colors': mappedColors,
                'mode': scalarMode,
                'lineWidth': tmpLineWidths[i],
                'stippleType': vcs2vtk.getStipple(tmpLineTypes[i])
            }
            customItem.AddObserver(vtk.vtkCommand.Context2DPaintEvent, getPaintHandler(attrs))

            area.GetDrawAreaItem().AddItem(customItem)


            countLevels += len(l)
        if len(textprops) > 0:
            self._resultDict["vtk_backend_contours_labels_text_properties"] = \
                textprops
        if len(luts) > 0:
            if self._gm.label:
                self._resultDict["vtk_backend_labeled_luts"] = luts
            else:
                self._resultDict["vtk_backend_luts"] = luts
        if len(cots) > 0:
            self._resultDict["vtk_backend_contours"] = cots

        if self._maskedDataMapper is not None:
            mappers.insert(0, self._maskedDataMapper)
            act = vtk.vtkActor()
            act.SetMapper(self._maskedDataMapper)
            actors.append([act, self._maskedDataMapper, plotting_dataset_bounds])
            # create a new renderer for this mapper
            # (we need one for each mapper because of cmaera flips)
            # self._context().fitToViewport(
            #     act, vp,
            #     wc=plotting_dataset_bounds, geoBounds=self._vtkDataSetBoundsNoMask,
            #     geo=self._vtkGeoTransform,
            #     priority=self._template.data.priority,
            #     create_renderer=True)

            self._maskedDataMapper.Update()
            maskedData = self._maskedDataMapper.GetInput()
            maskedColors = vtk.vtkUnsignedCharArray()
            maskedColors.SetNumberOfComponents(4)
            for i in range(poly.GetNumberOfCells()):
                maskedColors.InsertNextTypedTuple([0, 0, 0, 255])
            maskItem = vtk.vtkPolyDataItem()
            maskItem.SetPolyData(maskedData)
            maskItem.SetScalarMode(vtk.VTK_SCALAR_MODE_USE_CELL_DATA)
            maskItem.SetMappedColors(maskedColors)
            area.GetDrawAreaItem().AddItem(maskItem)


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
                  "vtk_backend_geo": self._vtkGeoTransform,
                  "vtk_backend_pipeline_context_area": area}
        if ("ratio_autot_viewport" in self._resultDict):
            kwargs["ratio_autot_viewport"] = vp
        self._resultDict.update(self._context().renderTemplate(
            self._template,
            self._data1,
            self._gm, t, z, **kwargs))

        projection = vcs.elements["projection"][self._gm.projection]
        kwargs['xaxisconvert'] = self._gm.xaxisconvert
        kwargs['yaxisconvert'] = self._gm.yaxisconvert
        if self._data1.getAxis(-1).isLongitude() and self._data1.getAxis(-2).isLatitude():
            self._context().plotContinents(self._plot_kargs.get("continents", self._useContinents),
                                           plotting_dataset_bounds, projection,
                                           self._dataWrapModulo,
                                           vp, self._template.data.priority, **kwargs)
