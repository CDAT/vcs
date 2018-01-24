"""
=====================================
VCS: Visualization and Control System
=====================================

-------
Authors
-------

Creator: `Dean Williams`_ (LLNL, AIMS Team)

Lead Developer: `Charles Doutriaux`_ (LLNL, AIMS Team)

Contributors: https://github.com/UV-CDAT/uvcdat/graphs/contributors

Support Email: uvcdat-support@llnl.gov

Project Site: http://uvcdat.llnl.gov/

Project Repo: https://github.com/UV-CDAT/uvcdat/graphs/contributors

.. _Dean Williams: http://computation.llnl.gov/about/our-people/highlights/dean-williams

.. _Charles Doutriaux: https://github.com/doutriaux1

-----------
Description
-----------
VCS is a visualization library for scientific data. It has a simple
model for defining a plot, that is decomposed into three parts:

1. **Data**: If it's iterable, we'll plot it... or at least try!
   Currently we support numpy arrays, lists (nested and not),
   and CDMS2 variables (there's some special support for metadata
   from CDMS2 that gives some niceties in your plot, but it's not
   mandatory).
2. **Graphics Method**: We have a variety of plot types that we
   support out-of-the box; you can easily customize every aspect
   of them to create the effect that you're looking for. If you can't,
   we also support defining your own graphics methods, which you can
   share with other users using standard python infrastructure (conda, pip).
3. **Template**: Templates control the appearance of everything that
   *isn't* your data. They position labels, control fonts, adjust borders,
   place legends, and more. They're very flexible, and give the fine-grained
   control of your plot that is needed for the truly perfect plot. Once you've
   customized them, you can also save them out for later use, and distribute
   them to other users.
"""
import warnings
import difflib


class bestMatch(object):
    def __setattr__(self, a, v):
        try:
            prop = getattr(self.__class__, a)
            isprop = isinstance(prop, property)
        except Exception:
            isprop = False
        if isprop or not hasattr(self, "__slots__") or a in self.__slots__:
            super(bestMatch, self).__setattr__(a, v)
        else:
            props = []
            for attr in dir(self.__class__):
                if isinstance(getattr(self.__class__, attr), property):
                    props.append(attr)
            possible = self.__slots__ + props
            matches = difflib.get_close_matches(a, possible)
            real_matches = []
            for m in matches:
                if m[0] != "_":
                    real_matches.append(m)
            if len(real_matches) == 1:
                raise AttributeError(
                    "'%s' object has no attribute '%s' did you mean %s ?" %
                    (self.__class__.__name__, a, repr(real_matches[0])))
            elif len(real_matches) > 1:
                raise AttributeError(
                    "'%s' object has no attribute '%s' did you mean one of %s ?" %
                    (self.__class__.__name__, a, repr(real_matches)))
            else:
                raise AttributeError(
                    "'%s' object has no attribute '%s' valid attributes are: %s" %
                    (self.__class__.__name__, a, repr(
                        self.__slots__)))


class VCSDeprecationWarning(DeprecationWarning):
    pass


# Python < 3 DeprecationWarning ignored by default
# warnings.simplefilter('default')
warnings.simplefilter("default", VCSDeprecationWarning)

_doValidation = True
next_canvas_id = 1
import cdat_info  # noqa
prefix = cdat_info.get_prefix()
sample_data = cdat_info.get_sampledata_path()
cdat_info.pingPCMDIdb("cdat", "vcs")
from .utils import *  # noqa
from . import colors  # noqa
from . import Canvas  # noqa
from .vcshelp import *  # noqa
from .queries import *  # noqa
from . import install_vcs  # noqa
import os  # noqa
from .manageElements import *  # noqa
import collections  # noqa

_colorMap = "viridis"

_default_time_units = 'days since 2000'

#
#
# Set up the User's  directory if necessary. Copy files from      #
# $PYTHONHOME/bin to the newly created $HOME/.uvcdat directory.          #
#
#
install_vcs._files()

#
#
# Set the user's XGKSFontDir environment variable.                              #
#
#

elements = collections.OrderedDict()
elements["list"] = {}
elements["projection"] = {}
elements["texttable"] = {}
elements["textorientation"] = {}
elements["textcombined"] = {}
elements["line"] = {}
elements["marker"] = {}
elements["fillarea"] = {}
elements["font"] = {}
elements["fontNumber"] = {}
elements["boxfill"] = {}
elements["isofill"] = {}
elements["isoline"] = {}
elements["meshfill"] = {}
elements["3d_scalar"] = {}
elements["3d_dual_scalar"] = {}
elements["3d_vector"] = {}
elements["template"] = {}
elements["taylordiagram"] = {}
elements["1d"] = {}
elements["vector"] = {}
elements["streamline"] = {}
elements["yxvsx"] = {}
elements["xyvsy"] = {}
elements["xvsy"] = {}
elements["scatter"] = {}
elements["colormap"] = {}
elements["display"] = {}

_protected_elements = {}
for k in list(elements.keys()):
    _protected_elements[k] = set()

dic = {}
for i in range(-5, 5):
    for j in range(-180, 181, 30):
        if j < 0:
            dic[i * 360 + j] = "%iW" % (-j)
        elif j > 0:
            dic[i * 360 + j] = "%iE" % j
        else:
            dic[i * 360] = "0"
elements["list"]["Lon30"] = dic

dic = {}
for j in range(-80, 81, 20):
    if j < 0:
        dic[j] = "%iS" % (-j)
    elif j > 0:
        dic[j] = "%iN" % j
    else:
        dic[0] = "Eq"
dic[-90] = "90S"
dic[90] = "90N"
elements["list"]["Lat20"] = dic

i = 1
for nm, fnt in [
    ("default", "AvantGarde-Book_Bold.ttf"),
    ("Clarendon", "Clarendon.ttf"),
    ("Courier", "Courier.ttf"),
    ("Helvetica", "HelvMono.ttf"),
    ("Adelon", "Adelon_Regular.ttf"),
    ("Times", "Times_CG_ATT.ttf"),
    ("Arabic", "Arabic.ttf"),
    ("Chinese", "Chinese_Generic1.ttf"),
    ("Greek", "Athens_Greek.ttf"),
    ("Hebrew", "hebrew.ttf"),
    ("Russian", "Russian.ttf"),
    ("Maths1", "jsMath-msam10.ttf"),
    ("Maths2", "blex.ttf"),
    ("Maths3", "jsMath-wasy10.ttf"),
    ("Maths4", "blsy.ttf"),
    ("AvantGarde", "AvantGarde-Book_Bold.ttf"),
    ("DejaVuSans-Bold", "DejaVuSans-Bold.ttf"),
    ("DejaVuSans-BoldOblique", "DejaVuSans-BoldOblique.ttf"),
    ("DejaVuSans-ExtraLight", "DejaVuSans-ExtraLight.ttf"),
    ("DejaVuSans-Oblique", "DejaVuSans-Oblique.ttf"),
    ("DejaVuSans", "DejaVuSans.ttf"),
    ("DejaVuSansCondensed-Bold", "DejaVuSansCondensed-Bold.ttf"),
    ("DejaVuSansCondensed-BoldOblique", "DejaVuSansCondensed-BoldOblique.ttf"),
    ("DejaVuSansCondensed-Oblique", "DejaVuSansCondensed-Oblique.ttf"),
    ("DejaVuSansCondensed", "DejaVuSansCondensed.ttf"),
]:
    pth = os.path.join(
        vcs.prefix,
        "share",
        "vcs",
        fnt)
    if os.path.exists(pth):
        vcs.elements["font"][nm] = pth
        vcs.elements["fontNumber"][i] = nm
        i += 1

p = projection.Proj("default")
p = projection.Proj("linear")
line.Tl("default")
line.Tl("solid")
line.Tl("deftaylordot")
line.type = ["dot"]
texttable.Tt("default")
textorientation.To("default")
to = textorientation.To("defcenter")
to.halign = "center"
to = textorientation.To("defup")
to.angle = -90
to.valign = "half"
to.halign = "center"
to = textorientation.To("defcentup")
to.angle = -90
to.valign = "half"
to.halign = "center"
to = textorientation.To("defright")
to.halign = "right"
boxfill.Gfb("default")
isofill.Gfi("default")
isoline.Gi("default")
unified1D.G1d("default")
yx = unified1D.G1d("default_yxvsx_")
vcs.elements["yxvsx"]["default"] = yx
xy = unified1D.G1d("default_xyvsy_")
xy.flip = True
vcs.elements["xyvsy"]["default"] = xy
sc = unified1D.G1d("default_scatter_")
sc._linewidth = 0
vcs.elements["scatter"]["default"] = sc
xvy = unified1D.G1d("default_xvsy_")
vcs.elements["xvsy"]["default"] = xvy
vector.Gv("default")
streamline.Gs("default")
marker.Tm("default")
meshfill.Gfm("default")
colormap.Cp("default")
displayplot.Dp("default")
dv3d.Gf3Dvector("default")
dv3d.Gf3Dscalar("default")
dv3d.Gf3Dscalar("Hovmoller3D")
dv3d.Gf3DDualScalar("default")

on = {'state': 1}
off = {'state': 0}

for nm in ["mercator", "orthographic", "lambert", "polar", "polyconic", "robinson",
           "mollweide", ]:
    p = projection.Proj(nm)
    if nm == "polar":
        p.type = -3
    else:
        p.type = nm

fillarea.Tf("default")
template.P("default")

t = taylor.Gtd("default")


pth = [vcs.prefix, 'share', 'vcs', 'initial.attributes']
try:
    vcs.scriptrun(os.path.join(*pth))
except BaseException:
    pass

for typ in list(elements.keys()):
    elts = elements[typ]
    for k in vcs.listelements(typ):  # let's save which elements should be saved and untouched
        _protected_elements[typ].add(k)

_dotdir, _dotdirenv = vcs.getdotdirectory()
user_init = os.path.join(
    os.path.expanduser("~"),
    _dotdir,
    'initial.attributes')
if os.path.exists(user_init):
    vcs.scriptrun(user_init)

canvaslist = []


def init(mode=1, pause_time=0, call_from_gui=0, size=None, backend="vtk",
         geometry=None, bg=None):
    """Initialize and construct a VCS Canvas object.

    :Example:

    .. doctest:: vcs_init

        >>> import vcs
        >>> portrait = vcs.init(size=.5) # Portrait of 1 width per 2 height
        >>> letter = vcs.init(size="letter") # also accepts "usletter"
        >>> a4 = vcs.init(size="a4")
        >>> import vtk
        >>> my_win = vtk.vtkRenderWindow() # To embed VCS in other applications
        >>> embedded = vcs.init(backend=my_win)
        >>> dict_init = vcs.init(geometry={"width": 1200, "height": 600})
        >>> tuple_init = vcs.init(geometry=(1200, 600))
        >>> bg_canvas = vcs.init(bg=True)

    :param size: Aspect ratio for canvas (width / height)
    :param backend: Which VCS backend to use
    :param geometry: Size (in pixels) you want the canvas to be.
    :param bg: Initialize a canvas to render in "background" mode (without
        displaying a window)
    :type size: float or case-insensitive str
    :type backend: str, :py:class:`vtk.vtkRenderWindow`
    :type geometry: dict or tuple
    :type bg: bool
    :return: An initialized canvas
    :rtype: vcs.Canvas.Canvas
    """
    canvas = Canvas.Canvas(
        mode=mode,
        pause_time=pause_time,
        call_from_gui=call_from_gui,
        size=size,
        backend=backend,
        geometry=geometry,
        bg=bg)
    global canvaslist
    canvaslist.append(canvas)
    return canvas
