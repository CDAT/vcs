from .pipeline import Pipeline

import numpy
import vcs
import cdms2


def smooth(x, beta, window_len=11):
    """ kaiser window smoothing """
    # extending the data at beginning and at the end
    # to apply the window at the borders
    s = numpy.r_[x[window_len - 1:0:-1], x, x[-1:-window_len:-1]]
    w = numpy.kaiser(window_len, beta)
    y = numpy.convolve(w / w.sum(), s, mode='valid')
    return y[(window_len / 2):-(window_len / 2)]


class Pipeline1D(Pipeline):

    """Implementation of the Pipeline interface for 1D VCS plots."""

    def __init__(self, gm, context_, plot_keyargs):
        super(Pipeline1D, self).__init__(gm, context_, plot_keyargs)

    def plot(self, data1, data2, tmpl, grid, transform, **kargs):
        """Overrides baseclass implementation."""
        Y = self._context().trimData1D(data1)
        data = data1  # For template
        if data2 is None:
            X = Y.getAxis(0)
        else:
            data = data2
            if self._gm.flip:
                raise RuntimeError("You cannot use the flip option on 1D graphic methods" +
                                   " if you are passing 2 arrays, please reverse order of arrays")
            X = Y
            data1._yname = data2.id
            Y = self._context().trimData1D(data2)

        if self._gm.flip:
            tmp = Y
            Y = X
            X = tmp

        X = self.convertAxis(cdms2.createAxis(X), "x")
        if self._gm.smooth is not None:
            Y = smooth(Y, self._gm.smooth)
        Y = self.convertAxis(cdms2.createAxis(Y), "y")

        ln_tmp = self._context().canvas.createline()
        Xs = X[:].tolist()
        Ys = Y[:].tolist()
        xs = []
        ys = []
        prev = None
        for i, v in enumerate(Ys):
            if v is not None and Xs[i] is not None:  # Valid data
                if prev is None:
                    prev = []
                    prev2 = []
                prev.append(Xs[i])
                prev2.append(v)
            else:
                if prev is not None:
                    xs.append(prev)
                    ys.append(prev2)
                    prev = None

        if prev is not None:
            xs.append(prev)
            ys.append(prev2)

        ln_tmp._x = xs
        ln_tmp._y = ys
        ln_tmp.color = [self._gm.linecolor, ]
        ln_tmp.priority = tmpl.data.priority
        if self._gm.linewidth > 0:
            ln_tmp.width = self._gm.linewidth
        else:
            ln_tmp.priority = 0
        ln_tmp.type = self._gm.linetype
        ln_tmp._viewport = [tmpl.data.x1, tmpl.data.x2,
                            tmpl.data.y1, tmpl.data.y2]

        # Also need to make sure it fills the whole space
        x1, x2, y1, y2 = vcs.utils.getworldcoordinates(self._gm, X, Y)
        if (y1 > y2) and numpy.allclose(self._gm.datawc_y1, 1.E20):
            tmp = y1
            y1 = y2
            y2 = tmp

        self._gm.datawc_x1 = x1
        self._gm.datawc_x2 = x2
        self._gm.datawc_y1 = y1
        self._gm.datawc_y2 = y2
        if numpy.allclose(y1, y2):
            y1 -= .0001
            y2 += .0001
        if numpy.allclose(x1, x2):
            x1 -= .0001
            x2 += .0001

        ln_tmp._worldcoordinate = [x1, x2, y1, y2]
        if self._gm.marker is not None:
            m = self._context().canvas.createmarker()
            m.type = self._gm.marker
            m.color = [self._gm.markercolor, ]
            if self._gm.markersize > 0:
                m.size = self._gm.markersize
            else:
                m.priority = 0
            m._x = ln_tmp.x
            m._y = ln_tmp.y
            m._viewport = ln_tmp.viewport
            m._worldcoordinate = ln_tmp.worldcoordinate

        if not (Y[:].min() > max(y1, y2) or Y[:].max() < min(y1, y2) or
                X[:].min() > max(x1, x2) or X[:].max() < min(x1, x2)):
            if ln_tmp.priority > 0:
                self._context().canvas.plot(ln_tmp, donotstoredisplay=True)
            if self._gm.marker is not None and m.priority > 0:
                self._context().canvas.plot(m, donotstoredisplay=True)

        ren2 = self._context().createRenderer()
        self._context().setLayer(ren2, ln_tmp.priority)
        self._context().renWin.AddRenderer(ren2)
        tmpl.plot(self._context().canvas, data, self._gm, bg=self._context().bg,
                  renderer=ren2, X=X, Y=Y)
        if hasattr(data1, "_yname"):
            del(data1._yname)
        del(vcs.elements["line"][ln_tmp.name])
        if self._gm.marker is not None:
            del(vcs.elements["marker"][m.name])

        if tmpl.legend.priority > 0:
            legd = self._context().canvas.createline()
            legd.x = [tmpl.legend.x1, tmpl.legend.x2]
            legd.y = [tmpl.legend.y1, tmpl.legend.y1]  # [y1, y1] intentional.
            legd.color = ln_tmp.color
            legd.width = ln_tmp.width
            legd.type = ln_tmp.type
            t = self._context().canvas.createtext(
                To_source=tmpl.legend.textorientation,
                Tt_source=tmpl.legend.texttable)
            t.x = tmpl.legend.x2
            t.y = tmpl.legend.y2
            t.string = data1.id
            self._context().canvas.plot(t, donotstoredisplay=True)
            sp = t.name.split(":::")
            del(vcs.elements["texttable"][sp[0]])
            del(vcs.elements["textorientation"][sp[1]])
            del(vcs.elements["textcombined"][t.name])
            self._context().canvas.plot(legd, donotstoredisplay=True)
            del(vcs.elements["line"][legd.name])
        return {}
