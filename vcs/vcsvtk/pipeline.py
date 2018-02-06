import weakref
import vcs
import numpy
import cdms2

class Pipeline(object):

    """Base class for a VTK pipeline implementation of a VCS plot command.

    The Pipeline class defines an interface for creating VTK pipeline from a
    VTK plot command. Refer to the method documentation for details.
    """

    def __init__(self, graphics_method, context_):
        """Initialize the pipeline object.

        _gm is a vcs graphics method
        _context is a weakref of the VTKVCSBackend object that created this
            Pipeline.
        """
        self._context = weakref.ref(context_)
        self._gm = graphics_method

    # For now, we'll just throw everything at plot. This might need to be
    # broken up into set_data, set_template, etc methods...
    def plot(self, data1, data2, template, grid, transform, **kargs):
        raise NotImplementedError("Missing override.")
        """
        def clean_val(value):
            if numpy.allclose(value, 0.):
                return 0.
            elif value < 0:
                sign = -1
                value = -value
            else:
                sign = 1
            i = int(numpy.log10(value))
            if i > 0:
                j = i
                k = 10.
            else:
                j = i - 1
                k = 10.
            v = int(value / numpy.power(k, j)) * numpy.power(k, j)
            return v * sign

        def mkdic(method, values):
            if method == 'area_wt':
                func = numpy.sin
                func2 = numpy.arcsin
            elif method == 'exp':
                func = numpy.exp
                func2 = numpy.log
            elif method == 'ln':
                func = numpy.log
                func2 = numpy.exp
            elif method == 'log10':
                func = numpy.log10
            vals = []
            for v in values:
                if method == 'area_wt':
                    vals.append(func(v * numpy.pi / 180.))
                else:
                    vals.append(func(v))
            min, max = vcs.minmax(vals)
            levs = vcs.mkscale(min, max)
# levs=vcs.mkevenlevels(min,max)
            vals = []
            for l in levs:
                if method == 'log10':
                    v = numpy.power(10, l)
                elif method == 'area_wt':
                    v = func2(l) / numpy.pi * 180.
                else:
                    v = func2(l)
                vals.append(clean_val(v))
            dic = vcs.mklabels(vals)
            dic2 = {}
            for k in list(dic.keys()):
                try:
                    if method == 'area_wt':
                        dic2[func(k * numpy.pi / 180.)] = dic[k]
                    else:
                        dic2[func(k)] = dic[k]
                except Exception:
                    pass
            return dic2
    """

    def convertAxis(self, axis, location):
        """Convert axis to log/area_wgt, etc..."""
        _convert  = getattr(self._gm,"{}axisconvert".format(location), "linear")
        _bounds = axis.getBounds()
        _func = vcs.utils.axisConvertFunctions[_convert]["forward"]
        _axis = _func(axis[:])
        _axis = cdms2.createAxis(_axis,id=axis.id)
        if _bounds is not None:
            _bounds = _func(_bounds)
            _axis.setBounds(bounds)
        
        """
        for number in ["1", "2"]:
            for name in ["ticlabels", "mtics"]:
                lbls = getattr(self._gm, "{}{}{}".format(location, name, number))
                if lbls in ["", "*"]:
                    continue
                new_lbls = {}
                for l in lbls:
                    new_lbls[_func(l)] = lbls[l]
                setattr(self._gm, "{}{}{}".format(location, name, number), new_lbls)
            wc = getattr(self._gm, "datawc_{}{}".format(location, number))
            if not numpy.allclose(wc,1.e20):  # defined value
                setattr(self._gm, "datawc_{}{}".format(location, number), _func(wc))
        print("WAS:",axis,"is",_axis)
        self._gm.list()
        """
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

        ratio = (datasetBounds[1] - datasetBounds[0]) / (datasetBounds[3] - datasetBounds[2])
        ratioWindow = (viewportBounds[1] - viewportBounds[0]) * windowSize[0] /\
            (viewportBounds[3] - viewportBounds[2]) / windowSize[1]
        if (ratio > ratioWindow):
            yMiddle = (viewportBounds[2] + viewportBounds[3]) * windowSize[1] / 2
            ySizeHalf = (viewportBounds[1] - viewportBounds[0]) * windowSize[0] / ratio / 2
            viewportBounds[2] = (yMiddle - ySizeHalf) / windowSize[1]
            viewportBounds[3] = (yMiddle + ySizeHalf) / windowSize[1]
        elif (ratio < ratioWindow):
            xMiddle = (viewportBounds[0] + viewportBounds[1]) * windowSize[0] / 2
            xSizeHalf = (viewportBounds[3] - viewportBounds[2]) * windowSize[1] * ratio / 2
            viewportBounds[0] = (xMiddle - xSizeHalf) / windowSize[0]
            viewportBounds[1] = (xMiddle + xSizeHalf) / windowSize[0]
        return viewportBounds
