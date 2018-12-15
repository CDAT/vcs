from __future__ import division
from .pipeline2d import Pipeline2D
from .. import vcs2vtk
import vcs
import numpy
import vtk
import warnings


class StreamlinePipeline(Pipeline2D):

    """Implementation of the Pipeline interface for VCS streamline plots."""

    def __init__(self, gm, context_, plot_keyargs):
        super(StreamlinePipeline, self).__init__(gm, context_, plot_keyargs)
        self._needsCellData = False
        self._needsVectors = True

    def _updateContourLevelsAndColors(self):
        """Overrides baseclass implementation."""
        """Set legend information and colors"""
        self._updateContourLevelsAndColorsGeneric()

    def _plotInternal(self):
        """Overrides baseclass implementation."""
        # Preserve time and z axis for plotting these inof in rendertemplate
        projection = vcs.elements["projection"][self._gm.projection]
        taxis = self._originalData1.getTime()

        if self._originalData1.ndim > 2:
            zaxis = self._originalData1.getAxis(-3)
        else:
            zaxis = None

        # Streamline color
        if (not self._gm.coloredbyvector):
            ln_tmp = self._gm.linetype
            if ln_tmp is None:
                ln_tmp = "default"
            try:
                ln_tmp = vcs.getline(ln_tmp)
                lwidth = ln_tmp.width[0]  # noqa
                lcolor = ln_tmp.color[0]
                lstyle = ln_tmp.type[0]  # noqa
            except Exception:
                lstyle = "solid"  # noqa
                lwidth = 1.  # noqa
                lcolor = [0., 0., 0., 100.]
            if self._gm.linewidth is not None:
                lwidth = self._gm.linewidth  # noqa
            if self._gm.linecolor is not None:
                lcolor = self._gm.linecolor

        # The unscaled continent bounds were fine in the presence of axis
        # conversion, so save them here
        continentBounds = vcs2vtk.computeDrawAreaBounds(self._vtkDataSetBoundsNoMask,
                                                        self._context_flipX, self._context_flipY)

        # Only scaling the data in the presence of axis conversion changes
        # the seed points in any other cases, and thus results in plots
        # different from the baselines but still fundamentally sound, it
        # seems.  Always scaling the data results in no differences in the
        # plots between Context2D and the old baselines.

        # Transform the input data
        T = vtk.vtkTransform()
        T.Scale(self._context_xScale, self._context_yScale, 1.)

        self._vtkDataSetFittedToViewport = vcs2vtk.applyTransformationToDataset(T, self._vtkDataSetFittedToViewport)
        self._vtkDataSetBoundsNoMask = self._vtkDataSetFittedToViewport.GetBounds()

        polydata = self._vtkDataSetFittedToViewport
        plotting_dataset_bounds = self.getPlottingBounds()
        x1, x2, y1, y2 = plotting_dataset_bounds
        vp = self._resultDict.get('ratio_autot_viewport',
                                  [self._template.data.x1, self._template.data.x2,
                                   self._template.data.y1, self._template.data.y2])

        # view and interactive area
        view = self._context().contextView
        area = vtk.vtkInteractiveArea()
        view.GetScene().AddItem(area)

        drawAreaBounds = vcs2vtk.computeDrawAreaBounds(self._vtkDataSetBoundsNoMask,
                                                       self._context_flipX, self._context_flipY)

        [renWinWidth, renWinHeight] = self._context().renWin.GetSize()
        geom = vtk.vtkRecti(int(vp[0] * renWinWidth),
                            int(vp[2] * renWinHeight),
                            int((vp[1] - vp[0]) * renWinWidth),
                            int((vp[3] - vp[2]) * renWinHeight))

        vcs2vtk.configureContextArea(area, drawAreaBounds, geom)

        dataLength = polydata.GetLength()

        if (not self._gm.evenlyspaced):
            # generate random seeds in a circle centered in the center of
            # the bounding box for the data.

            # by default vtkPointSource uses a global random source in vtkMath which is
            # seeded only once. It makes more sense to seed a random sequence each time you draw
            # the streamline plot.
            pointSequence = vtk.vtkMinimalStandardRandomSequence()
            pointSequence.SetSeedOnly(1177)  # replicate the seed from vtkMath

            seed = vtk.vtkPointSource()
            seed.SetNumberOfPoints(self._gm.numberofseeds)
            seed.SetCenter(polydata.GetCenter())
            seed.SetRadius(dataLength / 2.0)
            seed.SetRandomSequence(pointSequence)
            seed.Update()
            seedData = seed.GetOutput()

            # project all points to Z = 0 plane
            points = seedData.GetPoints()
            for i in range(0, points.GetNumberOfPoints()):
                p = list(points.GetPoint(i))
                p[2] = 0
                points.SetPoint(i, p)

        if (self._gm.integratortype == 0):
            integrator = vtk.vtkRungeKutta2()
        elif (self._gm.integratortype == 1):
            integrator = vtk.vtkRungeKutta4()
        else:
            if (self._gm.evenlyspaced):
                warnings.warn(
                    "You cannot use RungeKutta45 for evenly spaced streamlines."
                    "Using RungeKutta4 instead")
                integrator = vtk.vtkRungeKutta4()
            else:
                integrator = vtk.vtkRungeKutta45()

        if (self._gm.evenlyspaced):
            streamer = vtk.vtkEvenlySpacedStreamlines2D()
            startseed = self._gm.startseed \
                if self._gm.startseed else polydata.GetCenter()
            streamer.SetStartPosition(startseed)
            streamer.SetSeparatingDistance(self._gm.separatingdistance)
            streamer.SetSeparatingDistanceRatio(self._gm.separatingdistanceratio)
            streamer.SetClosedLoopMaximumDistance(self._gm.closedloopmaximumdistance)
        else:
            # integrate streamlines on normalized vector so that
            # IntegrationTime stores distance
            streamer = vtk.vtkStreamTracer()
            streamer.SetSourceData(seedData)
            streamer.SetIntegrationDirection(self._gm.integrationdirection)
            streamer.SetMinimumIntegrationStep(self._gm.minimumsteplength)
            streamer.SetMaximumIntegrationStep(self._gm.maximumsteplength)
            streamer.SetMaximumError(self._gm.maximumerror)
            streamer.SetMaximumPropagation(dataLength * self._gm.maximumstreamlinelength)

        streamer.SetInputData(polydata)
        streamer.SetInputArrayToProcess(0, 0, 0, 0, "vector")
        streamer.SetIntegrationStepUnit(self._gm.integrationstepunit)
        streamer.SetInitialIntegrationStep(self._gm.initialsteplength)
        streamer.SetMaximumNumberOfSteps(self._gm.maximumsteps)
        streamer.SetTerminalSpeed(self._gm.terminalspeed)
        streamer.SetIntegrator(integrator)

        # add arc_length to streamlines
        arcLengthFilter = vtk.vtkAppendArcLength()
        arcLengthFilter.SetInputConnection(streamer.GetOutputPort())

        arcLengthFilter.Update()
        streamlines = arcLengthFilter.GetOutput()

        # glyph seed points
        contour = vtk.vtkContourFilter()
        contour.SetInputConnection(arcLengthFilter.GetOutputPort())
        contour.SetValue(0, 0.001)
        if (streamlines.GetNumberOfPoints()):
            r = streamlines.GetPointData().GetArray("arc_length").GetRange()
            numberofglyphsoneside = self._gm.numberofglyphs // 2
            for i in range(1, numberofglyphsoneside):
                contour.SetValue(i, r[1] / numberofglyphsoneside * i)
        else:
            warnings.warn("No streamlines created. "
                          "The 'startseed' parameter needs to be inside the domain and "
                          "not over masked data.")
        contour.SetInputArrayToProcess(0, 0, 0, 0, "arc_length")

        # arrow glyph source
        glyph2DSource = vtk.vtkGlyphSource2D()
        glyph2DSource.SetGlyphTypeToTriangle()
        glyph2DSource.SetRotationAngle(-90)
        glyph2DSource.SetFilled(self._gm.filledglyph)

        # arrow glyph adjustment
        transform = vtk.vtkTransform()
        transform.Scale(1., self._gm.glyphbasefactor, 1.)
        transformFilter = vtk.vtkTransformFilter()
        transformFilter.SetInputConnection(glyph2DSource.GetOutputPort())
        transformFilter.SetTransform(transform)
        transformFilter.Update()
        glyphLength = transformFilter.GetOutput().GetLength()

        #  drawing the glyphs at the seed points
        glyph = vtk.vtkGlyph2D()
        glyph.SetInputConnection(contour.GetOutputPort())
        glyph.SetInputArrayToProcess(1, 0, 0, 0, "vector")
        glyph.SetSourceData(transformFilter.GetOutput())
        glyph.SetScaleModeToDataScalingOff()
        glyph.SetScaleFactor(dataLength * self._gm.glyphscalefactor / glyphLength)
        glyph.SetColorModeToColorByVector()

        glyphMapper = vtk.vtkPolyDataMapper()
        glyphActor = vtk.vtkActor()

        mapper = vtk.vtkPolyDataMapper()
        act = vtk.vtkActor()

        glyph.Update()
        glyphDataset = glyph.GetOutput()
        streamer.Update()
        lineDataset = streamer.GetOutput()

        deleteLineColors = False
        deleteGlyphColors = False

        # color the streamlines and glyphs
        cmap = self.getColorMap()
        if (self._gm.coloredbyvector):
            numLevels = len(self._contourLevels) - 1
            while len(self._contourColors) < numLevels:
                self._contourColors.append(self._contourColors[-1])

            lut = vtk.vtkLookupTable()
            lut.SetNumberOfTableValues(numLevels)
            for i in range(numLevels):
                r, g, b, a = self.getColorIndexOrRGBA(cmap, self._contourColors[i])
                lut.SetTableValue(i, r / 100., g / 100., b / 100., a / 100.)
            lut.SetVectorModeToMagnitude()
            if numpy.allclose(self._contourLevels[0], -1.e20):
                lmn = self._vectorRange[0]
            else:
                lmn = self._contourLevels[0][0]
            if numpy.allclose(self._contourLevels[-1], 1.e20):
                lmx = self._vectorRange[1]
            else:
                lmx = self._contourLevels[-1][-1]
            lut.SetRange(lmn, lmx)

            mapper.ScalarVisibilityOn()
            mapper.SetLookupTable(lut)
            mapper.UseLookupTableScalarRangeOn()
            mapper.SetScalarModeToUsePointFieldData()
            mapper.SelectColorArray("vector")

            lineAttrs = lineDataset.GetPointData()
            lineData = lineAttrs.GetArray("vector")

            if lineData and numLevels:
                lineColors = lut.MapScalars(lineData, vtk.VTK_COLOR_MODE_DEFAULT, 0)
                deleteLineColors = True
            else:
                print('WARNING: streamline pipeline cannot map scalars for "lineData", using solid color')
                numTuples = lineDataset.GetNumberOfPoints()
                color = [0, 0, 0, 255]
                lineColors = vcs2vtk.generateSolidColorArray(numTuples, color)

            glyphMapper.ScalarVisibilityOn()
            glyphMapper.SetLookupTable(lut)
            glyphMapper.UseLookupTableScalarRangeOn()
            glyphMapper.SetScalarModeToUsePointFieldData()
            glyphMapper.SelectColorArray("VectorMagnitude")

            glyphAttrs = glyphDataset.GetPointData()
            glyphData = glyphAttrs.GetArray("VectorMagnitude")

            if glyphData and numLevels:
                glyphColors = lut.MapScalars(glyphData, vtk.VTK_COLOR_MODE_DEFAULT, 0)
                deleteGlyphColors = True
            else:
                print('WARNING: streamline pipeline cannot map scalars for "glyphData", using solid color')
                numTuples = glyphDataset.GetNumberOfPoints()
                color = [0, 0, 0, 255]
                glyphColors = vcs2vtk.generateSolidColorArray(numTuples, color)
        else:
            mapper.ScalarVisibilityOff()
            glyphMapper.ScalarVisibilityOff()
            if isinstance(lcolor, (list, tuple)):
                r, g, b, a = lcolor
            else:
                r, g, b, a = cmap.index[lcolor]
            act.GetProperty().SetColor(r / 100., g / 100., b / 100.)
            glyphActor.GetProperty().SetColor(r / 100., g / 100., b / 100.)

            fixedColor = [int((r / 100.) * 255), int((g / 100.) * 255), int((b / 100.) * 255), 255]

            numTuples = lineDataset.GetNumberOfPoints()
            lineColors = vcs2vtk.generateSolidColorArray(numTuples, fixedColor)

            numTuples = glyphDataset.GetNumberOfPoints()
            glyphColors = vcs2vtk.generateSolidColorArray(numTuples, fixedColor)

        # Add the streamlines
        lineItem = vtk.vtkPolyDataItem()
        lineItem.SetPolyData(lineDataset)
        lineItem.SetScalarMode(vtk.VTK_SCALAR_MODE_USE_POINT_DATA)
        lineItem.SetMappedColors(lineColors)
        if deleteLineColors:
            lineColors.FastDelete()
        area.GetDrawAreaItem().AddItem(lineItem)

        # Add the glyphs
        glyphItem = vtk.vtkPolyDataItem()
        glyphItem.SetPolyData(glyphDataset)
        glyphItem.SetScalarMode(vtk.VTK_SCALAR_MODE_USE_POINT_DATA)
        glyphItem.SetMappedColors(glyphColors)
        if deleteGlyphColors:
            glyphColors.FastDelete()
        area.GetDrawAreaItem().AddItem(glyphItem)

        plotting_dataset_bounds = self.getPlottingBounds()
        vp = self._resultDict.get('ratio_autot_viewport',
                                  [self._template.data.x1, self._template.data.x2,
                                   self._template.data.y1, self._template.data.y2])

        kwargs = {
            'vtk_backend_grid': self._vtkDataSet,
            'dataset_bounds': self._vtkDataSetBounds,
            'plotting_dataset_bounds': plotting_dataset_bounds,
            "vtk_dataset_bounds_no_mask": self._vtkDataSetBoundsNoMask,
            'vtk_backend_geo': self._vtkGeoTransform,
            "vtk_backend_draw_area_bounds": continentBounds,
            "vtk_backend_viewport_scale": [
                self._context_xScale,
                self._context_yScale
            ]
        }
        if ('ratio_autot_viewport' in self._resultDict):
            kwargs["ratio_autot_viewport"] = vp
        self._resultDict.update(self._context().renderTemplate(
            self._template, self._data1,
            self._gm, taxis, zaxis, **kwargs))
        if (self._gm.coloredbyvector):
            self._resultDict.update(
                self._context().renderColorBar(self._template, self._contourLevels,
                                               self._contourColors,
                                               None,
                                               self.getColorMap()))

        kwargs['xaxisconvert'] = self._gm.xaxisconvert
        kwargs['yaxisconvert'] = self._gm.yaxisconvert
        if self._data1.getAxis(-1).isLongitude() and self._data1.getAxis(-2).isLatitude():
            self._context().plotContinents(self._plot_kargs.get("continents", self._useContinents),
                                           plotting_dataset_bounds, projection,
                                           self._dataWrapModulo, vp,
                                           self._template.data.priority, **kwargs)
        self._resultDict["vtk_backend_actors"] = [[lineItem, plotting_dataset_bounds]]
        self._resultDict["vtk_backend_luts"] = [[None, None]]
