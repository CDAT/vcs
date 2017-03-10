from .pipeline2d import Pipeline2D

import vcs
from vcs import vcs2vtk
import math
import numpy
import vtk


class StreamlinePipeline(Pipeline2D):

    """Implementation of the Pipeline interface for VCS streamline plots."""

    def __init__(self, gm, context_):
        super(StreamlinePipeline, self).__init__(gm, context_)
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

        lat = None
        lon = None

        latAccessor = self._data1.getLatitude()
        lonAccessor = self._data1.getLongitude()
        if latAccessor:
            lat = latAccessor[:]
        if lonAccessor:
            lon = lonAccessor[:]

        # Streamline color
        if (not self._gm.coloredbyvector):
            l = self._gm.linetype
            if l is None:
                l = "default"
            try:
                l = vcs.getline(l)
                lwidth = l.width[0]  # noqa
                lcolor = l.color[0]
                lstyle = l.type[0]  # noqa
            except:
                lstyle = "solid"  # noqa
                lwidth = 1.  # noqa
                lcolor = [0., 0., 0., 100.]
            if self._gm.linewidth is not None:
                lwidth = self._gm.linewidth  # noqa
            if self._gm.linecolor is not None:
                lcolor = self._gm.linecolor

        # get the data
        polydata = self._vtkPolyDataFilter.GetOutput()
        vectors = polydata.GetPointData().GetVectors()
        vcs2vtk.debugWriteGrid(polydata, "data")


        # generate random seeds in a circle centered in the center of
        # the bounding box for the data.
        bb = polydata.GetBounds()
        center = [(bb[0] + bb[1])/2, (bb[2] + bb[3])/2, 0]
        radius = math.sqrt((bb[1] - bb[0]) ** 2 + (bb[3] - bb[2]) ** 2) / 2.0

        seed = vtk.vtkPointSource()
        seed.SetNumberOfPoints(self._gm.numberofseeds)
        seed.SetCenter(center)
        seed.SetRadius(radius)
        seed.Update()
        seedData = seed.GetOutput()

        # project all points to Z = 0 plane
        points=seedData.GetPoints()
        for i in range(0, points.GetNumberOfPoints()):
            p = list(points.GetPoint(i))
            p[2] = 0
            points.SetPoint(i, p)

        vcs2vtk.debugWriteGrid(seedData, "seeds")

        if (self._gm.integratortype == 0):
            integrator = vtk.vtkRungeKutta2()
        elif (self._gm.integratortype == 1):
            integrator = vtk.vtkRungeKutta4()
        else:
            integrator = vtk.vtkRungeKutta45()

        streamer = vtk.vtkStreamTracer()
        streamer.SetInputData(polydata)
        streamer.SetSourceData(seedData)
        streamer.SetIntegrationDirection(self._gm.integrationdirection)
        streamer.SetIntegrationStepUnit(self._gm.integrationstepunit)
        streamer.SetInitialIntegrationStep(self._gm.initialsteplength)
        streamer.SetMinimumIntegrationStep(self._gm.minimumsteplength)
        streamer.SetMaximumIntegrationStep(self._gm.maximumsteplength)
        streamer.SetMaximumNumberOfSteps(self._gm.maximumsteps)
        streamer.SetMaximumPropagation(2 * radius * self._gm.maximumstreamlinelength)
        streamer.SetTerminalSpeed(self._gm.terminalspeed)
        streamer.SetMaximumError(self._gm.maximumerror)
        streamer.SetIntegrator(integrator)

        streamer.Update()
        streamlines = streamer.GetOutput()
        vcs2vtk.debugWriteGrid(streamlines, "streamlines")

        # visualize direction of the flow with glyphs
        contour = vtk.vtkContourFilter()
        contour.SetInputConnection(streamer.GetOutputPort())
        contour.SetValue(0, 0)
        contour.SetInputArrayToProcess(0, 0, 0, 0, "IntegrationTime")

        contour.Update()
        vcs2vtk.debugWriteGrid(contour.GetOutput(), "contour")

        glyph2DSource = vtk.vtkGlyphSource2D()
        glyph2DSource.SetGlyphTypeToEdgeArrow()
        glyph2DSource.SetFilled(1)
        glyph2DSource.Update()

        glyph = vtk.vtkGlyph2D()
        glyph.SetInputConnection(contour.GetOutputPort())
        glyph.SetInputArrayToProcess(1, 0, 0, 0, "vector")
        glyph.SetSourceData(glyph2DSource.GetOutput())
        glyph.SetScaleModeToDataScalingOff()
        glyph.SetScaleFactor(2 * radius * self._gm.glyphscalefactor)
        glyph.OrientOn()
        glyph.SetColorModeToColorByVector()
        glyph.Update()
        vcs2vtk.debugWriteGrid(glyph.GetOutput(), "glyph")

        glyphMapper = vtk.vtkPolyDataMapper()
        glyphMapper.SetInputConnection(glyph.GetOutputPort())
        glyphActor = vtk.vtkActor()
        glyphActor.SetMapper(glyphMapper)

        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputConnection(streamer.GetOutputPort())
        act = vtk.vtkActor()
        act.SetMapper(mapper)

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

            glyphMapper.ScalarVisibilityOn()
            glyphMapper.SetLookupTable(lut)
            glyphMapper.UseLookupTableScalarRangeOn()
            glyphMapper.SetScalarModeToUsePointFieldData()
            glyphMapper.SelectColorArray("VectorMagnitude")
        else:
            mapper.ScalarVisibilityOff()
            glyphMapper.ScalarVisibilityOff()
            if isinstance(lcolor, (list, tuple)):
                r, g, b, a = lcolor
            else:
                r, g, b, a = cmap.index[lcolor]
            act.GetProperty().SetColor(r / 100., g / 100., b / 100.)
            glyphActor.GetProperty().SetColor(r / 100., g / 100., b / 100.)

        plotting_dataset_bounds = vcs2vtk.getPlottingBounds(
            vcs.utils.getworldcoordinates(self._gm,
                                          self._data1.getAxis(-1),
                                          self._data1.getAxis(-2)),
            self._vtkDataSetBounds, self._vtkGeoTransform)
        x1, x2, y1, y2 = plotting_dataset_bounds
        if self._vtkGeoTransform is None:
            wc = plotting_dataset_bounds
        else:
            xrange = list(act.GetXRange())
            yrange = list(act.GetYRange())
            wc = [xrange[0], xrange[1], yrange[0], yrange[1]]

        vp = self._resultDict.get('ratio_autot_viewport',
                                  [self._template.data.x1, self._template.data.x2,
                                   self._template.data.y1, self._template.data.y2])

        dataset_renderer, xScale, yScale = self._context().fitToViewport(
            act, vp,
            wc=wc,
            priority=self._template.data.priority,
            create_renderer=True)
        glyph_renderer, xScale, yScale = self._context().fitToViewport(
            glyphActor, vp,
            wc=wc,
            priority=self._template.data.priority,
            create_renderer=False)

        kwargs = {'vtk_backend_grid': self._vtkDataSet,
                  'dataset_bounds': self._vtkDataSetBounds,
                  'plotting_dataset_bounds': plotting_dataset_bounds,
                  "vtk_dataset_bounds_no_mask": self._vtkDataSetBoundsNoMask,
                  'vtk_backend_geo': self._vtkGeoTransform}
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


        if self._context().canvas._continents is None:
            self._useContinents = False
        if self._useContinents:
            continents_renderer, xScale, yScale = self._context().plotContinents(
                plotting_dataset_bounds, projection,
                self._dataWrapModulo, vp, self._template.data.priority, **kwargs)
        self._resultDict["vtk_backend_actors"] = [[act, plotting_dataset_bounds]]
        self._resultDict["vtk_backend_luts"] = [[None, None]]
