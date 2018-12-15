from .pipeline2d import Pipeline2D
from .. import vcs2vtk

import numpy
import vcs
import vtk


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
            else:
                backgroundOpacities = [100.0 for lev in self._contourLevels]

        countLevels = 0
        vp = self._resultDict.get(
            'ratio_autot_viewport',
            [self._template.data.x1, self._template.data.x2,
             self._template.data.y1, self._template.data.y2])

        # view and interactive area
        view = self._context().contextView
        area = vtk.vtkInteractiveArea()
        view.GetScene().AddItem(area)

        adjusted_plotting_bounds = vcs2vtk.getProjectedBoundsForWorldCoords(
            plotting_dataset_bounds, self._gm.projection)
        drawAreaBounds = vcs2vtk.computeDrawAreaBounds(adjusted_plotting_bounds)

        [renWinWidth, renWinHeight] = self._context().renWin.GetSize()
        geom = vtk.vtkRecti(int(vp[0] * renWinWidth),
                            int(vp[2] * renWinHeight),
                            int((vp[1] - vp[0]) * renWinWidth),
                            int((vp[3] - vp[2]) * renWinHeight))

        vcs2vtk.configureContextArea(area, drawAreaBounds, geom)

        # FIXME: This render call is needed to work around a bug somewhere in the
        # FIXME: vtkContextTransform code, where the transformation represented by
        # FIXME: Map[To|From]Scene() isn't set up properly until after a render call.
        self._context().renWin.Render()

        for i, l in enumerate(tmpLevels):
            numLevels = len(l)

            cot = vtk.vtkContourFilter()

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

                        tt = vcs.createtexttable(None, tt)

                        colorOverride = colorOverrides[countLevels + idx]
                        if colorOverride is not None:
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
                    tprop.SetBackgroundOpacity(1.0)
                    tprops.AddItem(tprop)
                textprops.append(tprops)

                item = vtk.vtkLabeledContourPolyDataItem()
                item.SetTextProperties(tprops)
                item.SetTextPropertyMapping(tpropMap)
                item.SetLabelVisibility(1)
                item.SetSkipDistance(self._gm.labelskipdistance)

                mapper = vtk.vtkLabeledContourMapper()
                pdMapper = mapper.GetPolyDataMapper()

                luts.append([lut, [l[0], l[-1], False]])
            else:  # No isoline labels:
                item = vtk.vtkPolyDataItem()
                mapper = vtk.vtkPolyDataMapper()
                pdMapper = mapper
                luts.append([lut, [l[0], l[-1], False]])
            pdMapper.SetLookupTable(lut)
            lut.SetRange(l[0], l[-1])
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

            if self._needsCellData:
                attrs = poly.GetCellData()
                scalarMode = vtk.VTK_SCALAR_MODE_USE_CELL_DATA
            else:
                attrs = poly.GetPointData()
                scalarMode = vtk.VTK_SCALAR_MODE_USE_POINT_DATA

            data = attrs.GetScalars()
            mappedColors = lut.MapScalars(data, vtk.VTK_COLOR_MODE_DEFAULT, 0)

            intValue = vtk.vtkIntArray()
            intValue.SetNumberOfComponents(1)
            intValue.SetName("StippleType")
            intValue.InsertNextValue(vcs2vtk.getStipple(tmpLineTypes[i]))
            poly.GetFieldData().AddArray(intValue)

            floatValue = vtk.vtkFloatArray()
            floatValue.SetNumberOfComponents(1)
            floatValue.SetName("LineWidth")
            floatValue.InsertNextValue(tmpLineWidths[i])
            poly.GetFieldData().AddArray(floatValue)

            item.SetPolyData(poly)
            item.SetScalarMode(scalarMode)
            item.SetMappedColors(mappedColors)
            mappedColors.FastDelete()
            area.GetDrawAreaItem().AddItem(item)

            actors.append([item, plotting_dataset_bounds])

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

            actors.append([maskItem, self._maskedDataMapper, plotting_dataset_bounds])

        self._resultDict["vtk_backend_actors"] = actors

        t = self._originalData1.getTime()
        if self._originalData1.ndim > 2:
            z = self._originalData1.getAxis(-3)
        else:
            z = None
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
