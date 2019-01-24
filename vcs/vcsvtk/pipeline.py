import weakref
import vcs
import cdms2


class Pipeline(object):

    """Base class for a VTK pipeline implementation of a VCS plot command.

    The Pipeline class defines an interface for creating VTK pipeline from a
    VTK plot command. Refer to the method documentation for details.
    """

    def __init__(self, graphics_method, context_, plot_keyargs):
        """Initialize the pipeline object.

        _gm is a vcs graphics method
        _context is a weakref of the VTKVCSBackend object that created this
            Pipeline.
        """
        self._context = weakref.ref(context_)
        self._gm = graphics_method
        self._plot_kargs = plot_keyargs

    # For now, we'll just throw everything at plot. This might need to be
    # broken up into set_data, set_template, etc methods...
    def plot(self, data1, data2, template, grid, transform, **kargs):
        raise NotImplementedError("Missing override.")

    def convertAxis(self, axis, location):
        """Convert axis to log/area_wgt, etc..."""
        _convert = getattr(
            self._gm,
            "{}axisconvert".format(location),
            "linear")
        _bounds = axis.getBounds()
        _func = vcs.utils.axisConvertFunctions[_convert]["forward"]
        _axis = _func(axis[:])
        _axis = cdms2.createAxis(_axis, id=axis.id)
        if _bounds is not None:
            _bounds = _func(_bounds)
            _axis.setBounds(_bounds)
        if hasattr(axis, "units"):
            _axis.units = axis.units

        return _axis

    def getColorMap(self):
        _colorMap = self._gm.colormap
        if _colorMap is None:
            _colorMap = \
                _colorMap = self._context().canvas.getcolormapname()
        if _colorMap is None:
            _colorMap = vcs._colorMap
        if isinstance(_colorMap, str):
            _colorMap = vcs.elements["colormap"][_colorMap]
        return _colorMap

    def getColorIndexOrRGBA(self, colormap, color):
        return vcs.utils.rgba_color(color, colormap)

    # Returns new viewport bounds such that the dataset displayed there
    # will not be deformed.
    def _processRatioAutot(self, template, dataset):
        viewportBounds = [template.data.x1, template.data.x2,
                          template.data.y1, template.data.y2]
        datasetBounds = dataset.GetBounds()
        windowSize = self._context().renWin.GetSize()

        ratio = (datasetBounds[1] - datasetBounds[0]) / \
            (datasetBounds[3] - datasetBounds[2])
        ratioWindow = (viewportBounds[1] - viewportBounds[0]) * windowSize[0] /\
            (viewportBounds[3] - viewportBounds[2]) / windowSize[1]
        if (ratio > ratioWindow):
            yMiddle = (viewportBounds[2] +
                       viewportBounds[3]) * windowSize[1] / 2
            ySizeHalf = (
                viewportBounds[1] - viewportBounds[0]) * windowSize[0] / ratio / 2
            viewportBounds[2] = (yMiddle - ySizeHalf) / windowSize[1]
            viewportBounds[3] = (yMiddle + ySizeHalf) / windowSize[1]
        elif (ratio < ratioWindow):
            xMiddle = (viewportBounds[0] +
                       viewportBounds[1]) * windowSize[0] / 2
            xSizeHalf = (
                viewportBounds[3] - viewportBounds[2]) * windowSize[1] * ratio / 2
            viewportBounds[0] = (xMiddle - xSizeHalf) / windowSize[0]
            viewportBounds[1] = (xMiddle + xSizeHalf) / windowSize[0]
        return viewportBounds

    def getZandT(self):
        t = self._originalData1.getTime()
        z = self._originalData1.getLevel()

        if self._originalData1.ndim > 2 and z is None:
            z = self._originalData1.getAxis(-3)
        if self._originalData1.ndim > 3 and t is None:
            t = self._originalData1.getAxis(-4)
        return z, t