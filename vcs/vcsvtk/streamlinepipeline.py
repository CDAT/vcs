from .pipeline2d import Pipeline2D

import vcs
from vcs import vcs2vtk
import math
import numpy
import vtk
from vtk.util import numpy_support

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

        self._vtkPolyDataFilter.Update()
        polydata = self._vtkPolyDataFilter.GetOutput()

        # generate random seeds in a circle centered in the center of
        # the bounding box for the data.
        dataLength = polydata.GetLength()

        seed = vtk.vtkPointSource()
        seed.SetNumberOfPoints(self._gm.numberofseeds)
        seed.SetCenter(polydata.GetCenter())
        seed.SetRadius(dataLength / 2.0)
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
            integrator = vtk.vtkRungeKutta45()

        # integrate streamlines on normalized vector so that
        # IntegrationTime stores distance
        streamer = vtk.vtkStreamTracer()
        streamer.SetInputData(polydata)
        streamer.SetInputArrayToProcess(0, 0, 0, 0, "vector")
        streamer.SetSourceData(seedData)
        streamer.SetIntegrationDirection(self._gm.integrationdirection)
        streamer.SetIntegrationStepUnit(self._gm.integrationstepunit)
        streamer.SetInitialIntegrationStep(self._gm.initialsteplength)
        streamer.SetMinimumIntegrationStep(self._gm.minimumsteplength)
        streamer.SetMaximumIntegrationStep(self._gm.maximumsteplength)
        streamer.SetMaximumNumberOfSteps(self._gm.maximumsteps)
        streamer.SetMaximumPropagation(dataLength * self._gm.maximumstreamlinelength)
        streamer.SetTerminalSpeed(self._gm.terminalspeed)
        streamer.SetMaximumError(self._gm.maximumerror)
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
        r = streamlines.GetPointData().GetArray("arc_length").GetRange()
        numberofglyphsoneside = self._gm.numberofglyphs / 2
        for i in range(1, numberofglyphsoneside):
            contour.SetValue(i, r[1] / numberofglyphsoneside * i)
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
        glyphMapper.SetInputConnection(glyph.GetOutputPort())
        glyphActor = vtk.vtkActor()
        glyphActor.SetMapper(glyphMapper)

        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputConnection(streamer.GetOutputPort())
        act = vtk.vtkActor()
        act.SetMapper(mapper)

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

        plotting_dataset_bounds = self.getPlottingBounds()
        vp = self._resultDict.get('ratio_autot_viewport',
                                  [self._template.data.x1, self._template.data.x2,
                                   self._template.data.y1, self._template.data.y2])

        dataset_renderer, xScale, yScale = self._context().fitToViewport(
            act, vp,
            wc=plotting_dataset_bounds, geoBounds=self._vtkDataSetBoundsNoMask,
            geo=self._vtkGeoTransform,
            priority=self._template.data.priority,
            create_renderer=True)
        glyph_renderer, xScale, yScale = self._context().fitToViewport(
            glyphActor, vp,
            wc=plotting_dataset_bounds, geoBounds=self._vtkDataSetBoundsNoMask,
            geo=self._vtkGeoTransform,
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
