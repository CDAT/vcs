from .pipeline import Pipeline

import vcs
from vcs import vcs2vtk
import vtk

import math


class VectorPipeline(Pipeline):

    """Implementation of the Pipeline interface for VCS vector plots."""

    def __init__(self, gm, context_):
        super(VectorPipeline, self).__init__(gm, context_)

    def plot(self, data1, data2, tmpl, grid, transform):
        """Overrides baseclass implementation."""
        # Preserve time and z axis for plotting these inof in rendertemplate
        geo = None  # to make flake8 happy
        projection = vcs.elements["projection"][self._gm.projection]
        returned = {}
        taxis = data1.getTime()
        if data1.ndim > 2:
            zaxis = data1.getAxis(-3)
        else:
            zaxis = None

        # Ok get3 only the last 2 dims
        data1 = self._context().trimData2D(data1)
        data2 = self._context().trimData2D(data2)

        scale = 1.0

        lat = data1.getLatitude()[:]
        lon = data1.getLongitude()[:]

        if projection is not None:
            scale = (lat.max() - lat.min()) * (lon.max() - lon.min())

        gridGenDict = vcs2vtk.genGridOnPoints(data1, self._gm, deep=False, grid=grid,
                                              geo=transform, skipReprojection=False,
                                              data2=data2)

        data1 = gridGenDict["data"]
        data2 = gridGenDict["data2"]
        geo = gridGenDict["geo"]

        for k in ['vtk_backend_grid', 'xm', 'xM', 'ym', 'yM', 'continents',
                  'wrap', 'geo']:
            exec("%s = gridGenDict['%s']" % (k, k))
        grid = gridGenDict['vtk_backend_grid']
        self._dataWrapModulo = gridGenDict['wrap']

        if geo is not None:
            newv = vtk.vtkDoubleArray()
            newv.SetNumberOfComponents(3)
            newv.InsertTupleValue(0, [lon.min(), lat.min(),  0])
            newv.InsertTupleValue(1, [lon.max(), lat.max(),  0])

            vcs2vtk.projectArray(newv, projection,
                                 [gridGenDict['xm'], gridGenDict['xM'],
                                  gridGenDict['ym'], gridGenDict['yM']])
            dimMin = [0, 0, 0]
            dimMax = [0, 0, 0]
            newv.GetTupleValue(0, dimMin)
            newv.GetTupleValue(1, dimMax)
            scale = (dimMax[1] - dimMin[1]) * (dimMax[0] - dimMin[0])/scale
        else:
            scale = 1.0

        returned["vtk_backend_grid"] = grid
        returned["vtk_backend_geo"] = geo
        missingMapper = vcs2vtk.putMaskOnVTKGrid(data1, grid, None, False,
                                                 deep=False)

        # None/False are for color and cellData
        # (sent to vcs2vtk.putMaskOnVTKGrid)
        returned["vtk_backend_missing_mapper"] = (missingMapper, None, False)

        w = vcs2vtk.generateVectorArray(data1, data2, grid)

        grid.GetPointData().AddArray(w)

        # Vector attempt
        l = self._gm.line
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
            lcolor = 0
        if self._gm.linewidth is not None:
            lwidth = self._gm.linewidth  # noqa
        if self._gm.linecolor is not None:
            lcolor = self._gm.linecolor

        arrow = vtk.vtkGlyphSource2D()
        arrow.SetGlyphTypeToArrow()
        arrow.SetOutputPointsPrecision(vtk.vtkAlgorithm.DOUBLE_PRECISION)
        arrow.FilledOff()

        glyphFilter = vtk.vtkGlyph2D()
        glyphFilter.SetInputData(grid)
        glyphFilter.SetInputArrayToProcess(1, 0, 0, 0, "vectors")
        glyphFilter.SetSourceConnection(arrow.GetOutputPort())
        glyphFilter.SetVectorModeToUseVector()

        # Rotate arrows to match vector data:
        glyphFilter.OrientOn()

        # Scale to vector magnitude:
        glyphFilter.SetScaleModeToScaleByVector()
        glyphFilter.SetScaleFactor(math.sqrt(scale) * 2.0 * self._gm.scale)

        # These are some unfortunately named methods. It does *not* clamp the
        # scale range to [min, max], but rather remaps the range
        # [min, max] --> [0, 1].
        glyphFilter.ClampingOn()
        glyphFilter.SetRange(0.01, 1.0)

        mapper = vtk.vtkPolyDataMapper()

        glyphFilter.Update()
        data = glyphFilter.GetOutput()

        mapper.SetInputData(data)
        act = vtk.vtkActor()
        act.SetMapper(mapper)

        cmap = self.getColorMap()
        r, g, b = cmap.index[lcolor]
        act.GetProperty().SetColor(r / 100., g / 100., b / 100.)

        x1, x2, y1, y2 = vcs.utils.getworldcoordinates(self._gm, data1.getAxis(-1),
                                                       data1.getAxis(-2))
        if geo is None:
            wc = [x1, x2, y1, y2]
        else:
            wc = None

        # TODO: doWrap is broken for vectors
        # act = vcs2vtk.doWrap(act, [x1, x2, y1, y2], self._dataWrapModulo)

        self._context().fitToViewport(act, [tmpl.data.x1, tmpl.data.x2,
                                            tmpl.data.y1, tmpl.data.y2],
                                      wc=wc,
                                      priority=tmpl.data.priority,
                                      create_renderer=True)

        returned.update(self._context().renderTemplate(tmpl, data1,
                        self._gm, taxis, zaxis))

        if self._context().canvas._continents is None:
            continents = False
        if continents:
            self._context().plotContinents(x1, x2, y1, y2, projection,
                                           self._dataWrapModulo, tmpl)

        returned["vtk_backend_actors"] = [[act, [x1, x2, y1, y2]]]
        returned["vtk_backend_glyphfilters"] = [glyphFilter]
        returned["vtk_backend_luts"] = [[None, None]]

        return returned
