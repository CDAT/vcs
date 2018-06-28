from .pipeline2d import Pipeline2D
from . import fillareautils
# from .. import vcs2vtk

import numpy
import vcs
import vtk


class IsofillPipeline(Pipeline2D):

    """Implementation of the Pipeline interface for VCS isofill plots."""

    def __init__(self, gm, context_, plot_keyargs):
        super(IsofillPipeline, self).__init__(gm, context_, plot_keyargs)
        self._needsCellData = False

    def _updateContourLevelsAndColors(self):
        self._updateContourLevelsAndColorsGeneric()

    def _plotInternal(self):
        """Overrides baseclass implementation."""

        preppedCountours = self._prepContours()
        tmpLevels = preppedCountours["tmpLevels"]
        tmpIndices = preppedCountours["tmpIndices"]
        tmpColors = preppedCountours["tmpColors"]
        tmpOpacities = preppedCountours["tmpOpacities"]
        style = self._gm.fillareastyle

        luts = []
        cots = []
        mappers = []
        _colorMap = self.getColorMap()

        plotting_dataset_bounds = self.getPlottingBounds()
        x1, x2, y1, y2 = plotting_dataset_bounds
        fareapixelspacing, fareapixelscale = self._patternSpacingAndScale()

        for i, l in enumerate(tmpLevels):
            # Ok here we are trying to group together levels can be, a join
            # will happen if: next set of levels continues where one left off
            # AND pattern is identical
            mapper = vtk.vtkPolyDataMapper()
            lut = vtk.vtkLookupTable()
            cot = vtk.vtkBandedPolyDataContourFilter()
            cot.ClippingOn()
            # cot.SetInputData(self._vtkPolyDataFilter.GetOutput())
            cot.SetInputData(self._vtkDataSetFittedToViewport)
            cot.SetNumberOfContours(len(l))
            cot.SetClipTolerance(0.)
            for j, v in enumerate(l):
                cot.SetValue(j, v)
            cot.Update()

            cots.append(cot)
            mapper.SetInputConnection(cot.GetOutputPort())
            lut.SetNumberOfTableValues(len(tmpColors[i]))
            for j, color in enumerate(tmpColors[i]):
                r, g, b, a = self.getColorIndexOrRGBA(_colorMap, color)
                if style == 'solid':
                    tmpOpacity = tmpOpacities[j]
                    if tmpOpacity is None:
                        tmpOpacity = a / 100.
                    else:
                        tmpOpacity = tmpOpacities[j] / 100.
                    lut.SetTableValue(j, r / 100., g / 100., b / 100., tmpOpacity)
                else:
                    lut.SetTableValue(j, 1., 1., 1., 0.)
            luts.append([lut, [0, len(l) - 1, True]])
            mapper.SetLookupTable(lut)
            minRange = 0
            maxRange = len(l) - 1
            if (i == 0 and self._scalarRange[0] < l[0]):
                # band 0 is from self._scalarRange[0] to l[0]
                # we don't show band 0
                minRange += 1
            mapper.SetScalarRange(minRange, maxRange)
            mapper.SetScalarModeToUseCellData()
            mappers.append(mapper)

        self._resultDict["vtk_backend_luts"] = luts
        if len(cots) > 0:
            self._resultDict["vtk_backend_contours"] = cots

        numLevels = len(self._contourLevels)
        if mappers == []:  # ok didn't need to have special banded contours
            print('This seems like a weird case, do not get it')
            mapper = vtk.vtkPolyDataMapper()
            mappers = [mapper]
            # Colortable bit
            # make sure length match
            while len(self._contourColors) < len(self._contourLevels):
                self._contourColors.append(self._contourColors[-1])

            lut = vtk.vtkLookupTable()
            lut.SetNumberOfTableValues(numLevels)
            for i in range(numLevels):
                r, g, b, a = self.getColorIndexOrRGBA(_colorMap, self._contourColors[i])
                lut.SetTableValue(i, r / 100., g / 100., b / 100., a / 100.)

            mapper.SetLookupTable(lut)
            if numpy.allclose(self._contourLevels[0], -1.e20):
                lmn = self._min - 1.
            else:
                lmn = self._contourLevels[0]
            if numpy.allclose(self._contourLevels[-1], 1.e20):
                lmx = self._max + 1.
            else:
                lmx = self._contourLevels[-1]
            mapper.SetScalarRange(lmn, lmx)
            self._resultDict["vtk_backend_luts"] = [[lut, [lmn, lmx, True]]]

        if self._maskedDataMapper is not None:
            mappers.insert(0, self._maskedDataMapper)

        # And now we need actors to actually render this thing
        actors = []
        ct = 0
        vp = self._resultDict.get('ratio_autot_viewport',
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

        area.GetAxis(vtk.vtkAxis.LEFT).SetVisible(False)
        area.GetAxis(vtk.vtkAxis.RIGHT).SetVisible(False)
        area.GetAxis(vtk.vtkAxis.BOTTOM).SetVisible(False)
        area.GetAxis(vtk.vtkAxis.TOP).SetVisible(False)

        cam = dataset_renderer.GetActiveCamera()
        cam.ParallelProjectionOn()
        # We increase the parallel projection parallelepiped with 1/1000 so that
        # it does not overlap with the outline of the dataset. This resulted in
        # system dependent display of the outline.
        cam.SetParallelScale(self._context_yd * 1.001)
        cd = cam.GetDistance()
        cam.SetPosition(self._context_xc, self._context_yc, cd)
        cam.SetFocalPoint(self._context_xc, self._context_yc, 0.)
        if self._vtkGeoTransform is None:
            if self._context_flipY:
                cam.Elevation(180.)
                cam.Roll(180.)
                pass
            if self._context_flipX:
                cam.Azimuth(180.)


        # mIdx = 0

        for mapper in mappers:
            act = vtk.vtkActor()
            act.SetMapper(mapper)
            mapper.Update()
            poly = mapper.GetInput()

            if not poly:
                print(' #$#$#$#$#$#$#$ => This must be that useless mapper we created above for some mysterious reason')
                continue

            patact = None
            # TODO see comment in boxfill.
            if mapper is self._maskedDataMapper:
                actors.append([act, self._maskedDataMapper, plotting_dataset_bounds])
            else:
                actors.append([act, plotting_dataset_bounds])

            if style == "solid":
                if mapper is self._maskedDataMapper:
                    # FIXME: Not quite sure how I got away without this in the other cases
                    mappedColors = vtk.vtkUnsignedCharArray()
                    mappedColors.SetNumberOfComponents(4)
                    for i in range(poly.GetNumberOfCells()):
                        mappedColors.InsertNextTypedTuple([0, 0, 0, 255])
                else:
                    attrs = poly.GetCellData()
                    data = attrs.GetScalars()
                    lut = mapper.GetLookupTable()
                    scalarRange = mapper.GetScalarRange()
                    lut.SetRange(scalarRange)
                    mappedColors = lut.MapScalars(data, vtk.VTK_COLOR_MODE_DEFAULT, 0)

                    # fname = 'isofill-solid-%d' % mIdx
                    # vcs2vtk.debugWriteGrid(poly, fname)
                    # mIdx += 1

                item = vtk.vtkPolyDataItem()
                item.SetPolyData(poly)
                item.SetScalarMode(vtk.VTK_SCALAR_MODE_USE_CELL_DATA)
                item.SetMappedColors(mappedColors)
                area.GetDrawAreaItem().AddItem(item)

            if mapper is not self._maskedDataMapper:
                # Since pattern creation requires a single color, assuming the first
                c = self.getColorIndexOrRGBA(_colorMap, tmpColors[ct][0])

                patact = fillareautils.make_patterned_polydata(poly,
                                                               fillareastyle=style,
                                                               fillareaindex=tmpIndices[ct],
                                                               fillareacolors=c,
                                                               fillareaopacity=tmpOpacities[ct],
                                                               fillareapixelspacing=fareapixelspacing,
                                                               fillareapixelscale=fareapixelscale,
                                                               size=self._context().renWin.GetSize(),
                                                               renderer=dataset_renderer)

                if patact is not None:
                    actors.append([patact, plotting_dataset_bounds])

                    patMapper = patact.GetMapper()
                    patMapper.Update()
                    patPoly = patMapper.GetInput()

                    item = vtk.vtkPolyDataItem()
                    item.SetPolyData(patPoly)

                    item.SetScalarMode(vtk.VTK_SCALAR_MODE_USE_CELL_DATA)
                    colorArray = patPoly.GetCellData().GetArray('Colors')

                    item.SetMappedColors(colorArray)
                    area.GetDrawAreaItem().AddItem(item)

                # increment the count
                ct += 1

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

        # Compensate for the different viewport size of the colorbar
        legendpixspacing = [int(fareapixelspacing[0] / (vp[1] - vp[0])),
                            int(fareapixelspacing[1] / (vp[3] - vp[2]))]
        legendpixscale = fareapixelscale / (vp[1] - vp[0])

        self._resultDict.update(
            self._context().renderColorBar(self._template, self._contourLevels,
                                           self._contourColors, legend,
                                           self.getColorMap(),
                                           style=style,
                                           index=self._gm.fillareaindices,
                                           opacity=self._gm.fillareaopacity,
                                           pixelspacing=legendpixspacing,
                                           pixelscale=legendpixscale))

        projection = vcs.elements["projection"][self._gm.projection]
        kwargs['xaxisconvert'] = self._gm.xaxisconvert
        kwargs['yaxisconvert'] = self._gm.yaxisconvert
        if self._data1.getAxis(-1).isLongitude() and self._data1.getAxis(-2).isLatitude():
            self._context().plotContinents(self._plot_kargs.get("continents", self._useContinents),
                                           plotting_dataset_bounds, projection,
                                           self._dataWrapModulo,
                                           vp, self._template.data.priority, **kwargs)
