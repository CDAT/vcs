"""
    Canvas objects are the 'visualization' component of VCS. Canvases allow the user to take data and plot it on a
    visible window. This gives users an easy way to preview how changes to data representation in VCS will change the
    visualization of that data.

    .. pragma: skip-doctest

    .. _list: https://docs.python.org/2/library/functions.html#list
    .. _tuple: https://docs.python.org/2/library/functions.html#tuple
    .. _dict: https://docs.python.org/2/library/stdtypes.html#mapping-types-dict
    .. _None: https://docs.python.org/2/library/constants.html?highlight=none#None
    .. _str: https://docs.python.org/2/library/functions.html?highlight=str#str
    .. _bool: https://docs.python.org/2/library/functions.html?highlight=bool#bool
    .. _float: https://docs.python.org/2/library/functions.html?highlight=float#float
    .. _int: https://docs.python.org/2/library/functions.html?highlight=float#int
    .. _long: https://docs.python.org/2/library/functions.html?highlight=float#long
    .. _file: https://docs.python.org/2/library/functions.html?highlight=open#file
"""
import warnings
import numpy.ma
import MV2
import numpy
import cdutil
from .queries import *  # noqa
from . import boxfill
from . import isofill
from . import isoline
from . import vector
from . import line
from . import marker
from . import fillarea
from . import texttable
from . import textorientation
from . import textcombined
from . import template
from . import displayplot
import vtk
from .VTKPlots import VTKVCSBackend
from weakref import WeakSet, WeakKeyDictionary

from .error import vcsError
import cdms2
import copy
import cdtime
import vcs
import os
import re
import sys
import random
from cdms2.grid import AbstractRectGrid
import shutil
import subprocess
import inspect
from . import VCS_validation_functions
from .xmldocs import plot_keywords_doc, graphics_method_core, axesconvert, xaxisconvert, \
    plot_1D_input, plot_2D_input, plot_output, plot_2_1D_input, plot_2_1D_options
gui_canvas_closed = 0
canvas_closed = 0
import vcs.manageElements  # noqa
from . import configurator  # noqa
from .projection import no_deformation_projections  # noqa
try:
    import vcsaddons  # noqa
    hasVCSAddons = True
except Exception:
    hasVCSAddons = False


def rotate(x, y, xorigin, yorigin, angle):
    # translate
    xtr = x - xorigin
    ytr = y - yorigin
    angle = angle/180.*numpy.pi
    xout = xtr * numpy.cos(angle) - ytr * numpy.sin(angle)
    yout = xtr * numpy.sin(angle) + ytr * numpy.cos(angle)

    xout += xorigin
    yout += yorigin
    return xout, yout


class JupyterFFMPEG(object):
    def __init__(self, source, ffmpeg_result, width=640, height=420, controls=True):
        self.source = source
        self.width = width
        self.height = height
        self.controls = controls
        self.result = ffmpeg_result

    def _repr_html_(self):
        html = "<video width='%i' height='%i'" % (self.width, self.height)
        if self.controls:
            html += "controls"
        html += "><source src='%s' type='video/mp4'>" % (self.source)
        return html


class SIGNAL(object):

    def __init__(self, name=None):
        self._functions = WeakSet()
        self._methods = WeakKeyDictionary()
        self._name = name

    def __call__(self, *args, **kargs):
        # Call handler functions
        for func in self._functions:
            func(*args, **kargs)

        # Call handler methods
        for obj, funcs in list(self._methods.items()):
            for func in funcs:
                func(obj, *args, **kargs)

    def connect(self, slot):
        if inspect.ismethod(slot):
            if slot.__self__ not in self._methods:
                self._methods[slot.__self__] = set()

            self._methods[slot.__self__].add(slot.__func__)

        else:
            self._functions.add(slot)

    def disconnect(self, slot):
        if inspect.ismethod(slot):
            if slot.__self__ in self._methods:
                self._methods[slot.__self__].remove(slot.__func__)
        else:
            if slot in self._functions:
                self._functions.remove(slot)

    def clear(self):
        self._functions.clear()
        self._methods.clear()


def dictionarytovcslist(dictionary, name):
    for k in list(dictionary.keys()):
        if not isinstance(k, (float, int)):
            raise Exception('Error, vcs list must have numbers only as keys')
    dictionarytovcslist(dictionary, name)
    return None


def _determine_arg_list(g_name, actual_args):
    """Determine what is in the argument list for plotting graphics methods"""

    itemplate_name = 2
    igraphics_method = 3
    igraphics_option = 4

    # Note: Set default graphics method to 'default', which is invalid.
    # If it is not modified in this routine, it will be filled in later
    # in _reconstruct_tv after the grid type is established.
    #
    # Xtrargs - {} - added by C.Doutriaux, needed for projection object passed
    # Need to be passed as keyword later
    arglist = [None, None, 'default', 'default', 'default', {}]
    arghold = []
    argstring = []
    args = actual_args
    found_slabs = 0
    for i in range(len(args)):
        if isinstance(args[i], str):
            argstring.append(args[i])
        else:
            try:
                possible_slab = cdms2.asVariable(args[i], 0)
                if hasattr(possible_slab, 'iscontiguous'):
                    if not possible_slab.iscontiguous():
                        # this seems to loose the id...
                        saved_id = possible_slab.id
                        possible_slab = possible_slab.ascontiguousarray()
                        possible_slab.id = saved_id
                arglist[found_slabs] = possible_slab
                if found_slabs == 2:
                    raise vcsError("Too many slab arguments.")
                found_slabs = found_slabs + 1
            except cdms2.CDMSError:
                arghold.append(args[i])

    #
    # Now find the template
    #
    args = arghold
    arghold = []
    found_template = 0
    for i in range(len(args)):
        if (istemplate(args[i])):
            if found_template:
                raise vcsError('You can only specify one template object.')
            arglist[itemplate_name] = args[i].name
            found_template = found_template + 1
        else:
            arghold.append(args[i])
    #
    # Now find the graphics method
    #
    args = arghold
    arghold = []
    found_graphics_method = 0
    for i in range(len(args)):
        if (isgraphicsmethod(args[i])):
            if found_graphics_method:
                raise vcsError('You can only specify one graphics method.')
            arglist[igraphics_method] = graphicsmethodtype(args[i])
            arglist[igraphics_option] = args[i].name
            found_graphics_method = found_graphics_method + 1
        elif (isline(args[i])):
            if found_graphics_method:
                raise vcsError('You can only specify one graphics method.')
            arglist[igraphics_method] = 'line'
            arglist[igraphics_option] = args[i].name
            found_graphics_method = found_graphics_method + 1
        elif (ismarker(args[i])):
            if found_graphics_method:
                raise vcsError('You can only specify one graphics method.')
            arglist[igraphics_method] = 'marker'
            arglist[igraphics_option] = args[i].name
            found_graphics_method = found_graphics_method + 1
        elif (isfillarea(args[i])):
            if found_graphics_method:
                raise vcsError('You can only specify one graphics method.')
            arglist[igraphics_method] = 'fillarea'
            arglist[igraphics_option] = args[i].name
            found_graphics_method = found_graphics_method + 1
        elif (istext(args[i])):
            if found_graphics_method:
                raise vcsError('You can only specify one graphics method.')
            arglist[igraphics_method] = 'text'
            arglist[igraphics_option] = args[
                i].Tt_name + ':::' + args[i].To_name
            found_graphics_method = found_graphics_method + 1
        elif (isprojection(args[i])):
            arglist[5]['projection'] = args[i].name
        elif hasVCSAddons and isinstance(args[i], vcsaddons.core.VCSaddon):
            if found_graphics_method:
                raise vcsError('You can only specify one graphics method.')
            arglist[igraphics_method] = graphicsmethodtype(args[i])
            arglist[igraphics_option] = args[i].name
            found_graphics_method = found_graphics_method + 1
        else:
            raise vcsError("Unknown type %s of argument to plotting command." %
                           type(args[i]))
    if g_name is not None:
        arglist[igraphics_method] = g_name

# Now install the string arguments, left to right.
    if found_template == 0:
        if len(argstring) > 0:
            arglist[itemplate_name] = argstring[0]
            del argstring[0]
    if found_graphics_method == 0 and g_name is None:
        if len(argstring) > 0:
            arglist[igraphics_method] = argstring[0]
            del argstring[0]

# Check for various errors
    if len(argstring) >= 1:
        arglist[igraphics_option] = argstring[0]
        del argstring[0]

    if len(argstring) > 0:
        if g_name is None:
            raise vcsError("Error in argument list for vcs plot command.")
        else:
            raise vcsError(
                "Error in argument list for vcs %s  command." %
                g_name)

    if hasVCSAddons and isinstance(arglist[igraphics_method], vcsaddons.core.VCSaddon):
        if found_slabs != arglist[igraphics_method].g_nslabs:
            raise vcsError(
                "%s requires %i slab(s)" %
                (arglist[igraphics_method].g_name,
                 arglist[igraphics_method].g_nslabs))
    else:
        if arglist[igraphics_method].lower() in (
                'scatter', 'vector', 'streamline', 'xvsy', 'stream', 'glyph',
                '3d_vector', '3d_dual_scalar'):
            if found_slabs != 2:
                raise vcsError(
                    "Graphics method %s requires 2 slabs." %
                    arglist[igraphics_method])
        elif arglist[igraphics_method].lower() == 'meshfill':
            if found_slabs == 0:
                raise vcsError("Graphics method requires at least 1 slab.")
            elif found_slabs == 1:
                g = arglist[0].getGrid()
                if not isinstance(g, (cdms2.gengrid.AbstractGenericGrid,
                                      cdms2.hgrid.AbstractCurveGrid, cdms2.grid.TransientRectGrid)):
                    raise vcsError("Meshfill requires 2 slab if first slab doesn't have a "
                                   "Rectilinear, Curvilinear or Generic Grid type")
        elif ((arglist[igraphics_method] == 'line') or
              (arglist[igraphics_method] == 'marker') or
              (arglist[igraphics_method] == 'fillarea') or
              (arglist[igraphics_method] == 'text')):
            if found_slabs != 0:
                raise vcsError(
                    "Continents or low-level primative methods requires 0 slabs.")
        elif arglist[igraphics_method].lower() == 'default':
            pass                            # Check later
        else:
            if found_slabs != 1 and not(
                    found_slabs == 2 and arglist[igraphics_method].lower() == "1d"):
                raise vcsError(
                    "Graphics method %s requires 1 slab." %
                    arglist[igraphics_method])
    if isinstance(arglist[3], str):
        arglist[3] = arglist[3].lower()
    return arglist


def _process_keyword(obj, target, source, keyargs, default=None):
    """ Set obj.target from:
    - keyargs[source]
    - default
    - obj.source
    in that order."""
    arg = keyargs.get(source)
    if arg is not None:
        setattr(obj, target, arg)
    elif default is not None:
        setattr(obj, target, default)
    elif hasattr(obj, source):
        setattr(obj, target, getattr(obj, source))
    return arg


class Canvas(vcs.bestMatch):
    """Usually created using :py:func:`vcs.init`, this object provides easy access
    to the functionality of the entire VCS module:

    See :py:func:`vcs.Canvas.Canvas.plot` for more information on the type of
    data that can be plotted on a Canvas object.

    .. pragma: skip-doctest
    """
    __slots__ = [
        '_mode',
        '_pause_time',
        '_viewport',
        '_worldcoordinate',
        '_winfo_id',
        '_varglist',
        '_animate_info',
        '_isplottinggridded',
        '_user_actions_names',
        '_user_actions',
        '_animate',
        '_canvas',
        '_canvas_id',
        'canvas_template_editor',
        'ratio',
        'size',
        'ParameterChanged',
        'colormap',
        'backgroundcolor',
        'width',
        'height',
        'display_names',
        '_dotdir',
        '_dotdirenv',
        'drawLogo',
        'enableLogo',
        'backend',
        'configurator',
        '_Canvas__last_plot_actual_args',
        '_Canvas__last_plot_keyargs',
        '__last_plot_actual_args',
        '__last_plot_keyargs',
        '_continents',
        '_continents_line',
        '_savedcontinentstype',
    ]

#     def applicationFocusChanged(self, old, current ):
#         self.backend.applicationFocusChanged()

    def _set_user_actions_names(self, value):
        value = VCS_validation_functions.checkListElements(
            self,
            'user_actions_names',
            value,
            VCS_validation_functions.checkString)
        self._user_actions_names = value
        while len(self._user_actions) < len(self._user_actions_names):
            self._user_actions.append(self._user_actions[-1])

    def _get_user_actions_names(self):
        return self._user_actions_names
    user_actions_names = property(
        _get_user_actions_names,
        _set_user_actions_names)

    def _set_user_actions(self, value):
        value = VCS_validation_functions.checkListElements(
            self,
            'user_actions_names',
            value,
            VCS_validation_functions.checkCallable)
        self._user_actions = value
        while len(self._user_actions) < len(self._user_actions_names):
            self._user_actions.append(self._user_actions[-1])

    def _get_user_actions(self):
        return self._user_actions
    user_actions = property(_get_user_actions, _set_user_actions)

    def _setmode(self, value):
        value = VCS_validation_functions.checkInt(
            self,
            'mode',
            value,
            minvalue=0,
            maxvalue=1)
        self._mode = value

    def _getmode(self):
        return self._mode
    mode = property(_getmode, _setmode)

    def _setwinfo_id(self, value):
        value = VCS_validation_functions.checkInt(self, 'winfo_id', value)
        self._winfo_id = value

    def _getwinfo_id(self):
        return self._winfo_id
    winfo_id = property(_getwinfo_id, _setwinfo_id)

    def _setvarglist(self, value):
        value = VCS_validation_functions.checkListElements(
            self,
            'varglist',
            value,
            VCS_validation_functions.checkCallable)
        self._varglist = value

    def _getvarglist(self):
        return self._varglist
    varglist = property(_getvarglist, _setvarglist)

    def _setcanvas(self, value):
        raise vcsError("Error, canvas is not an attribute you can set")

    def _getcanvas(self):
        return self._canvas
    canvas = property(_getcanvas, _setcanvas)

    def _setanimate(self, value):
        raise vcsError("Error, animate is not an attribute you can set")

    def _getanimate(self):
        return self._animate
    animate = property(_getanimate, _setanimate)

    def _setpausetime(self, value):
        value = VCS_validation_functions.checkInt(self, 'pause_time', value)
        self._pause_time = value

    def _getpausetime(self):
        return self._pause_time
    pause_time = property(_getpausetime, _setpausetime)

    def _setviewport(self, value):
        if not isinstance(value, list) and not len(value) == 4:
            raise vcsError(
                "viewport must be of type list and have four values ranging between [0,1].")
        for v in range(4):
            if not 0. <= value[v] <= 1.:
                raise vcsError(
                    "viewport must be of type list and have four values ranging between [0,1].")
        self._viewport = value

    def _getviewport(self):
        return self._viewport
    viewport = property(_getviewport, _setviewport)

    def _setworldcoordinate(self, value):
        if not isinstance(value, list) and not len(value) == 4:
            raise vcsError(
                "worldcoordinate must be of type list and have four values ranging between [0,1].")
        self._worldcoordinate = value

    def _getworldcoordinate(self):
        return self._worldcoordinate
    worldcoordinate = property(_getworldcoordinate, _setworldcoordinate)

    def _setisplottinggridded(self, value):
        if not isinstance(value, bool):
            raise vcsError("isplottinggridded must be boolean")
        self._isplottinggridded = value  # No check on this!

    def _getisplottinggridded(self):
        return self._isplottinggridded
    isplottinggridded = property(_getisplottinggridded, _setisplottinggridded)

    def _setanimate_info(self, value):
        self._animate_info = value  # No check on this!

    def _getanimate_info(self):
        return self._animate_info
    animate_info = property(_getanimate_info, _setanimate_info)

    def start(self, *args, **kargs):
        self.interact(*args, **kargs)

    def interact(self, *args, **kargs):
        """Puts the canvas into interactive mode.
        This allows the user to click on the canvas to add markers,
        add textboxes, configure settings, rotate 3d plots, and more.

        Press 'Q' with the Canvas selected to quit.

        :Example:

            .. code-block:: python

                a=vcs.init()
                b=a.getboxfill()
                array=[range(10) for _ in range(10)]
                a.plot(b,array)
                a.interact() # interactively configure Canvas

        .. pragma: skip-doctest Because testing interact() can't be handled in a doctest
        """
        self.configure()
        self.backend.interact(*args, **kargs)

    def _datawc_tv(self, tv, arglist):
        """The graphics method's data world coordinates (i.e., datawc_x1, datawc_x2,
        datawc_y1, and datawc_y2) will override the incoming variable's coordinates.
        tv equals arglist[0] and assumed to be the first Variable. arglist[1] is
        assumed to be the second variable."""

        # Determine the type of graphics method
        nvar = 1
        if arglist[3] == 'boxfill':
            gm = self.getboxfill(arglist[4])
        elif arglist[3] == 'isofill':
            gm = self.getisofill(arglist[4])
        elif arglist[3] == 'isoline':
            gm = self.getisoline(arglist[4])
        elif arglist[3] == 'scatter':
            nvar = 2
            gm = self.getscatter(arglist[4])
        elif arglist[3] == 'vector':
            nvar = 2
            gm = self.getvector(arglist[4])
        elif arglist[3] == 'xvsy':
            nvar = 2
            gm = self.getxvsy(arglist[4])
        elif arglist[3] == 'xyvsy':
            gm = self.getxyvsy(arglist[4])
        elif arglist[3] == 'yxvsx':
            gm = self.getyxvsx(arglist[4])
        elif arglist[3] == 'taylor':
            gm = self.gettaylor(arglist[4])
        elif arglist[3] == 'meshfill':
            gm = self.getmeshfill(arglist[4])
        else:
            return tv

        # Determine if the graphics method needs clipping
        f32 = numpy.array((1.e20), numpy.float32)
        set_new_x = 0
        set_new_y = 0
        if (gm.datawc_x1 != f32) and (gm.datawc_x2 != f32):
            set_new_x = 1
        if (gm.datawc_y1 != f32) and (gm.datawc_y2 != f32):
            set_new_y = 1

        try:
            if ((set_new_x == 1) and (set_new_y == 0)) or (
                    arglist[3] == 'yxvsx'):
                tv = tv(longitude=(gm.datawc_x1, gm.datawc_x2))
                if nvar == 2:
                    arglist[1] = arglist[1](
                        longitude=(
                            gm.datawc_x1,
                            gm.datawc_x2))
            elif ((set_new_x == 0) and (set_new_y == 1)) or (arglist[3] == 'xyvsy'):
                tv = tv(latitude=(gm.datawc_y1, gm.datawc_y2))
                if nvar == 2:
                    arglist[1] = arglist[1](
                        latitude=(
                            gm.datawc_y1,
                            gm.datawc_y2))
            elif (set_new_x == 1) and (set_new_y == 1):
                tv = tv(
                    latitude=(
                        gm.datawc_y1, gm.datawc_y2), longitude=(
                        gm.datawc_x1, gm.datawc_x2))
                if nvar == 2:
                    arglist[1] = arglist[1](
                        latitude=(
                            gm.datawc_y1, gm.datawc_y2), longitude=(
                            gm.datawc_x1, gm.datawc_x2))
        except Exception:
            pass

        return tv

    def savecontinentstype(self, value):
        self._savedcontinentstype = value

    def onClosing(self, cell):
        if self.configurator:
            self.endconfigure()
        self.backend.onClosing(cell)

    def _reconstruct_tv(self, arglist, keyargs):
        """Reconstruct a transient variable from the keyword arguments.
        Also select the default graphics method, depending on the grid type
        of the reconstructed variable. For meshfill, ravel the last two
        dimensions if necessary.
        arglist[0] is assumed to be a Variable."""

        ARRAY_1 = 0
        ARRAY_2 = 1
        # TEMPLATE = 2
        GRAPHICS_METHOD = 3
        GRAPHICS_OPTION = 4

        origv = arglist[ARRAY_1]

        # Create copies of domain and attributes
        variable = keyargs.get('variable')
        if variable is not None:
            origv = MV2.array(variable)
        tvdomain = origv.getDomain()
        attrs = copy.copy(origv.attributes)
        axislist = list([x[0].clone() for x in tvdomain])

        # Map keywords to dimension indices
        try:
            rank = origv.ndim
        except Exception:
            rank = len(origv.shape)

        dimmap = {}
        dimmap['x'] = xdim = rank - 1
        dimmap['y'] = ydim = rank - 2
        dimmap['z'] = rank - 3
        dimmap['t'] = rank - 4
        dimmap['w'] = rank - 5

        # Process grid keyword
        grid = keyargs.get('grid')
        if grid is not None and xdim >= 0 and ydim >= 0:
            if grid.getOrder() is None or grid.getOrder() == 'yx':
                axislist[xdim] = grid.getLongitude().clone()
                axislist[ydim] = grid.getLatitude().clone()
            else:
                axislist[xdim] = grid.getLatitude().clone()
                axislist[ydim] = grid.getLongitude().clone()

        # Process axis keywords
        for c in ['x', 'y', 'z', 't', 'w']:
            if dimmap[c] < 0:
                continue
            arg = keyargs.get(c + 'axis')
            if arg is not None:
                axislist[dimmap[c]] = arg.clone()

        # Process array keywords
        for c in ['x', 'y', 'z', 't', 'w']:
            if dimmap[c] < 0:
                continue
            arg = keyargs.get(c + 'array')
            if arg is not None:
                axis = axislist[dimmap[c]]
                axis = cdms2.createAxis(arg, id=axis.id)
                axis.setBounds(None)
                axislist[dimmap[c]] = axis

        # Process bounds keywords
        for c in ['x', 'y']:
            if dimmap[c] < 0:
                continue
            arg = keyargs.get(c + 'bounds')
            if arg is not None:
                axis = axislist[dimmap[c]]
                axis.setBounds(arg)

        # Process axis name keywords
        for c in ['x', 'y', 'z', 't', 'w']:
            if dimmap[c] < 0:
                continue
            arg = keyargs.get(c + 'name')
            if arg is not None:
                axis = axislist[dimmap[c]]
                axis.id = axis.name = arg

        # Create the internal tv
        tv = cdms2.createVariable(
            origv,
            copy=0,
            axes=axislist,
            attributes=attrs)
        grid = tv.getGrid()

        isgridded = (grid is not None)

        # Set the default graphics method if not already set.
        if arglist[GRAPHICS_METHOD] == "default" or\
                (arglist[GRAPHICS_METHOD] == 'boxfill' and arglist[GRAPHICS_METHOD + 1] == "default"):
                        # See _determine_arg_list

            if grid is None:
                if tv.ndim == 1:
                    arglist[GRAPHICS_METHOD] = 'yxvsx'
                else:
                    arglist[GRAPHICS_METHOD] = 'boxfill'
            elif isinstance(grid, AbstractRectGrid):
                arglist[GRAPHICS_METHOD] = 'boxfill'
            else:
                latbounds, lonbounds = grid.getBounds()
                if (latbounds is None) or (lonbounds is None):
                    if not isinstance(grid, cdms2.hgrid.AbstractCurveGrid):
                        # Plug in 'points' graphics method here, with:
                        #   arglist[GRAPHICS_METHOD] = 'points'
                        raise vcsError(
                            "Cell boundary data is missing, cannot plot nonrectangular gridded data.")
                    else:
                        arglist[GRAPHICS_METHOD] = 'boxfill'
                else:

                    # tv has a nonrectilinear grid with bounds defined,
                    # so use meshfill. Create another default meshobject to hang
                    # keywords on, since the true 'default' meshobject
                    # is immutable.
                    arglist[GRAPHICS_METHOD] = 'meshfill'

                    # Get the mesh from the grid.
                    try:
                        gridindices = tv.getGridIndices()
                    except Exception:
                        gridindices = None
                    mesh = grid.getMesh(transpose=gridindices)

                    # mesh array needs to be mutable, so make it a tv.
                    # Normally this is done up front in _determine_arg_list.
                    arglist[ARRAY_2] = cdms2.asVariable(mesh, 0)
                    meshobj = self.createmeshfill()
                    meshobj.wrap = [0.0, 360.0]  # Wraparound
                    arglist[GRAPHICS_OPTION] = '__d_meshobj'

        # IF Meshfill method and no mesh passed then try to get the mesh from
        # the object
        if arglist[GRAPHICS_METHOD] == 'meshfill' and arglist[ARRAY_2] is None:
            # Get the mesh from the grid.
            try:
                gridindices = tv.getGridIndices()
                mesh = grid.getMesh(transpose=gridindices)
            except Exception:
                gridindices = None
                mesh = grid.getMesh()

            # mesh array needs to be mutable, so make it a tv.
            # Normally this is done up front in _determine_arg_list.
            arglist[ARRAY_2] = cdms2.asVariable(mesh, 0)
            if arglist[GRAPHICS_OPTION] == 'default':
                meshobj = self.createmeshfill()
                meshobj.wrap = [0.0, 360.0]  # Wraparound
                arglist[GRAPHICS_OPTION] = meshobj.name

        # Ravel the last two dimensions for meshfill if necessary
        # value to know if we're plotting a grided meshfill
        self.isplottinggridded = False

        if isgridded and (arglist[GRAPHICS_METHOD] == 'meshfill'):
            self.isplottinggridded = True

        # Process variable attributes
        _process_keyword(tv, 'comment1', 'comment1', keyargs)
        _process_keyword(tv, 'comment2', 'comment2', keyargs)
        _process_keyword(tv, 'comment3', 'comment3', keyargs)
        _process_keyword(tv, 'comment4', 'comment4', keyargs)
        _process_keyword(tv, 'source', 'file_comment', keyargs)
        _process_keyword(tv, 'time', 'hms', keyargs)
        _process_keyword(tv, 'title', 'long_name', keyargs)
        _process_keyword(tv, 'name', 'name', keyargs, default=tv.id)
        tim = keyargs.get('time')
        if tim is not None:
            if isinstance(tim, str):
                ctime = cdtime.s2c(str(tim))
            else:
                ctime = tim.tocomp()
            tv.user_date = str(ctime)
        _process_keyword(tv, 'units', 'units', keyargs)
        _process_keyword(tv, 'date', 'ymd', keyargs)
        # If date has still not been set, try to get it from the first
        # time value if present
        if not hasattr(tv, 'user_date') and not hasattr(
                tv, 'date') and not hasattr(tv, 'time'):
            change_date_time(tv, 0)

        # Draw continental outlines if specified.
        contout = keyargs.get('continents', None)
        if contout is None:
            if (xdim >= 0 and ydim >= 0 and tv.getAxis(xdim).isLongitude() and tv.getAxis(ydim).isLatitude()) or\
                    (self.isplottinggridded):
                contout = self.getcontinentstype()
            else:
                contout = 0

        if (isinstance(arglist[GRAPHICS_METHOD], str) and (arglist[GRAPHICS_METHOD]) == 'meshfill') or (
                (xdim >= 0 and ydim >= 0 and (isinstance(contout, str) or contout >= 1))):
            self.setcontinentstype(contout)
            self.savecontinentstype(contout)
        else:
            self.setcontinentstype(0)
            self.savecontinentstype(0)

        # Reverse axis direction if necessary
        xrev = keyargs.get('xrev', 0)
        if xrev == 1 and xdim >= 0:
            tv = tv[..., ::-1]

        # By default, latitudes on the y-axis are plotted S-N
        # levels on the y-axis are plotted with decreasing pressure
        if ydim >= 0:
            yrev = keyargs.get('yrev', 0)
            if yrev == 1:
                tv = tv[..., ::-1, :].clone()

#  -- This s no longer needed since we are making a copy of the data.
#     We now apply the axes changes below in __plot. Dean and Charles keep
#     an eye opened for the errors concerning datawc in the VCS module.
#        tv = self._datawc_tv( tv, arglist )
        return tv

    def objecthelp(self, *arg):
        """Print out information on the VCS object. See example below on its use.

        :Example:

            .. doctest:: canvas_objecthelp

                >>> a=vcs.init()
                >>> ln=a.getline('red') # Get a VCS line object
                >>> a.objecthelp(ln) # This will print out information on how to use ln
                The Line object ...

        """
        for x in arg:
            print(getattr(x, "__doc__", ""))

    def __init__(self, mode=1, pause_time=0, call_from_gui=0, size=None,
                 backend="vtk", geometry=None, bg=None):
        self._canvas_id = vcs.next_canvas_id
        self.ParameterChanged = SIGNAL('ParameterChanged')
        vcs.next_canvas_id += 1
        self.colormap = None
        self.backgroundcolor = 255, 255, 255

        # displays plotted
        self.display_names = []
        ospath = os.environ["PATH"]
        found = False
        for p in ospath.split(":"):
            if p == os.path.join(sys.prefix, "bin"):
                found = True
                break
        if found is False:
            os.environ["PATH"] = os.environ["PATH"] + \
                ":" + os.path.join(sys.prefix, "bin")
        global gui_canvas_closed
        global canvas_closed

        self.winfo_id = -99
        self.varglist = []
        self.isplottinggridded = False

        if size is None:
            psize = 1.2941176470588236
        elif isinstance(size, (int, float)):
            psize = size
        elif isinstance(size, str):
            if size.lower() in ['letter', 'usletter']:
                psize = size = 1.2941176470588236
            elif size.lower() in ['a4', ]:
                psize = size = 1.4142857142857141
            else:
                raise Exception('Unknown size: %s' % size)
        else:
            raise Exception('Unknown size: %s' % size)

        self.size = psize

        self.mode = mode
        self._animate_info = []
        self.pause_time = pause_time
        self._canvas = vcs
        self.viewport = [0, 1, 0, 1]
        self.worldcoordinate = [0, 1, 0, 1]
        self._dotdir, self._dotdirenv = vcs.getdotdirectory()
        self.drawLogo = False
        self.enableLogo = True

        if geometry is not None:
            # Extract width and height, create dict
            if type(geometry) == dict:
                for key in geometry:
                    if key not in ("width", "height"):
                        raise ValueError("Unexpected key %s in geometry" % key)

                width = geometry.get("width", None)
                height = geometry.get("height", None)

                check_vals = [v for v in (width, height) if v is not None]
                VCS_validation_functions.checkListOfNumbers(self, 'geometry', check_vals,
                                                            minvalue=1, minelements=1, maxelements=2, ints=True)
            elif type(geometry) in (list, tuple):
                width, height = VCS_validation_functions.checkListOfNumbers(self, 'geometry', geometry,
                                                                            minvalue=1, minelements=2,
                                                                            maxelements=2, ints=True)
            else:
                raise ValueError("geometry should be list, tuple, or dict")

            self.width = width
            self.height = height
        else:
            w, h = 814, 606
            if size is not None:
                # What is the purpose of the 'size' argument?  Is it intended to forever
                # constrain the aspect ratio of the plot?  What if size and geometry are
                # both given, but are inconsistent?
                w = h * size
            self.width = w
            self.height = h

        if backend == "vtk":
            self.backend = VTKVCSBackend(self, bg=bg)
        elif isinstance(backend, vtk.vtkRenderWindow):
            self.backend = VTKVCSBackend(self, renWin=backend, bg=bg)
        else:
            warnings.warn(
                "Unknown backend type: '%s'\nAssiging 'as is' to "
                "backend, no warranty about anything working from this point on" %
                backend)
            self.backend = backend

        self._animate = self.backend.Animate(self)

        self.configurator = None
        self.setcontinentsline("default")
        self.setcontinentstype(1)

# Initial.attributes is being called in main.c, so it is not needed here!
# Actually it is for taylordiagram graphic methods....
#  Okay, then this is redundant since it is done in main.c. When time perments, put the
#  taylordiagram graphic methods attributes in main.c Because this is here we must check
#  to make sure that the initial attributes file is called only once for normalization
#  purposes....

        self.canvas_template_editor = None
        self.ratio = '0'
        self._user_actions_names = [
            'Clear Canvas',
            'Close Canvas',
            'Show arguments passsed to user action']
        self._user_actions = [self.clear, self.close, self.dummy_user_action]

    def configure(self):
        for display in self.display_names:
            d = vcs.elements["display"][display]
            if "3d" in d.g_type.lower():
                return
        if self.configurator is None:
            self.configurator = configurator.Configurator(self)
            self.configurator.update()
            self.configurator.show()

    def endconfigure(self):
        if self.configurator is not None:
            self.configurator.detach()
            self.configurator = None

    def processParameterChange(self, args):
        self.ParameterChanged(args)

    # Functions to set/querie drawing of UV-CDAT logo
    def drawlogoon(self):
        """Show UV-CDAT logo on the canvas

        :Example:

            .. doctest:: canvas_drawlogoon

                >>> a=vcs.init()
                >>> a.drawlogoon()
                >>> a.getdrawlogo()
                True
        """
        self.enableLogo = True

    def drawlogooff(self):
        """Hide UV-CDAT logo on the canvas

        :Example:

            .. doctest:: canvas_drawlogooff

                >>> a=vcs.init()
                >>> a.drawlogooff()
                >>> a.getdrawlogo()
                False
        """
        self.enableLogo = False

    def getdrawlogo(self):
        """Returns value of draw logo. By default, draw logo is set to True.

        :Example:

            .. doctest:: canvas_getdrawlogo

                >>> a=vcs.init()
                >>> a.getdrawlogo()
                True
                >>> a.drawlogooff()
                >>> a.getdrawlogo()
                False

        :returns: Boolean value of system variable which indicates whether logo will be drawn
        :rtype: bool
        """
        return self.enableLogo

    def initLogoDrawing(self):
        """Initializes logo drawing for the canvas.

        :Example:

            .. doctest:: canvas_initLogoDrawing

                >>> a=vcs.init()
                >>> a.initLogoDrawing() # will draw logo when plot is called
                >>> array=[range(10) for _ in range(10)]
                >>> a.plot(array) # should have logo in lower right corner
                <vcs.displayplot.Dp object at 0x...>

        """
        self.drawLogo = self.enableLogo

    def update(self, *args, **kargs):
        """If a series of commands are given to VCS and the Canvas Mode is
        set to manual, then use this function to update the plot(s)
        manually.

        :Example:

            .. doctest:: canvas_update

                >>> a=vcs.init()
                >>> import cdms2 # We need cdms2 to create a slab
                >>> f = cdms2.open(vcs.sample_data+'/clt.nc') # use cdms2 to open a data file
                >>> s = f('clt') # use the data file to create a slab
                >>> a.plot(s,'default','boxfill','quick')
                <vcs.displayplot.Dp ...>
                >>> a.mode = 0 # Go to manual mode
                >>> box=a.getboxfill('quick')
                >>> box.color_1=100
                >>> box.xticlabels('lon30','lon30')
                >>> box.xticlabels('','')
                >>> box.datawc(1e20,1e20,1e20,1e20)
                >>> box.datawc(-45.0, 45.0, -90.0, 90.0)
                >>> a.update() # Update the changes manually
        """

        return self.backend.update(*args, **kargs)

    def scriptobject(self, obj, script_filename=None, mode=None):
        """Save individual attributes sets (i.e., individual primary class
        objects and/or secondary objects). These attribute sets
        are saved in the user's current directory in one of two formats:
        Python script, or a Javascript Object.

        .. note::

            If the the filename has a ".py" at the end, it will produce a
            Python script. If the filename has a ".scr" at the end, it will
            produce a VCS script. If neither extensions are given, then by
            default a Javascript Object will be produced.

        .. attention::

            VCS does not allow the modification of 'default' attribute sets,
            it will not allow them to be saved as individual script files.
            However, a 'default' attribute set that has been copied under a
            different name can be saved as a script file.

        .. admonition:: VCS Scripts Deprecated

            SCR scripts are no longer generated by this function

        :Example:

            .. doctest:: canvas_scriptobject

                >>> a=vcs.init()
                >>> i=a.createisoline('dean') # default isoline object instance
                >>> a.scriptobject(i,'ex_isoline.py') # Save to 'isoline.py'
                >>> a.scriptobject(i,'ex_isoline2') # Save to 'isoline2.json'

        :param script_filename: Name of the output script file.
        :type script_filename: `str`_

        :param mode: Mode is either "w" for replace or "a" for append.
        :type mode: `str`_

        :param obj: Any VCS primary class or secondary object.
        :type obj: VCS object
        """
        if istemplate(obj):
            template.P.script(obj, script_filename, mode)
        elif isgraphicsmethod(obj):
            if (obj.g_name == 'Gfb'):
                boxfill.Gfb.script(obj, script_filename, mode)
            elif (obj.g_name == 'Gfi'):
                isofill.Gfi.script(obj, script_filename, mode)
            elif (obj.g_name == 'Gi'):
                isoline.Gi.script(obj, script_filename, mode)
            elif (obj.g_name == 'GXy'):
                xyvsy.GXy.script(obj, script_filename, mode)
            elif (obj.g_name == 'GYx'):
                yxvsx.GYx.script(obj, script_filename, mode)
            elif (obj.g_name == 'GXY'):
                xvsy.GXY.script(obj, script_filename, mode)
            elif (obj.g_name == 'Gv'):
                vector.Gv.script(obj, script_filename, mode)
            elif (obj.g_name == 'GSp'):
                scatter.GSp.script(obj, script_filename, mode)
            elif (obj.g_name == 'Gtd'):
                obj.script(script_filename, mode)
            elif (obj.g_name == 'Gfm'):
                obj.script(script_filename, mode)
            else:
                print('Could not find the correct graphics class object.')
        elif issecondaryobject(obj):
            if (obj.s_name == 'Tl'):
                line.Tl.script(obj, script_filename, mode)
            elif (obj.s_name == 'Tm'):
                marker.Tm.script(obj, script_filename, mode)
            elif (obj.s_name == 'Tf'):
                fillarea.Tf.script(obj, script_filename, mode)
            elif (obj.s_name == 'Tt'):
                texttable.Tt.script(obj, script_filename, mode)
            elif (obj.s_name == 'To'):
                textorientation.To.script(obj, script_filename, mode)
            elif (obj.s_name == 'Tc'):
                textcombined.Tc.script(obj, script_filename, mode)
            elif (obj.s_name == 'Proj'):
                obj.script(script_filename, mode)
            else:
                print('Could not find the correct secondary class object.')
        else:
            print('This is not a template, graphics method or secondary method object.')

    def removeobject(self, obj):
        return vcs.removeobject(obj)
    removeobject.__doc__ = vcs.manageElements.removeobject.__doc__  # noqa

    def removeP(self, *args):
        return vcs.removeP(*args)

    def clean_auto_generated_objects(self, type=None):
        """Cleans up all automatically generated VCS objects.

        This function will delete all references to objects that
        VCS created automatically in response to user actions but are
        no longer in use. This shouldn't be necessary most of the time,
        but if you're running into performance/memory issues, calling it
        periodically may help.

        :Example:

            .. doctest:: canvas_clean_auto_generated_objects

                >>> a=vcs.init()
                >>> clean=a.clean_auto_generated_objects # alias long name
                >>> clean() # clean possible old objects from vcs
                >>> txt=a.listelements('textorientation') # initial objects
                >>> array=[range(10) for _ in range(10)]
                >>> a.plot(array)
                <vcs.displayplot.Dp object at 0x...>
                >>> new_txt=a.listelements('textorientation') # has new names
                >>> txt == new_txt # should not be the same
                False
                >>> clean()
                >>> new_txt=a.listelements('textorientation') # back to initial
                >>> txt == new_txt # should have the same contents
                True


        :param type: Type of objects to remove. By default, will remove
            all object types.
        :type type: None, str, list/tuple (of str)
        """

        if type is None:
            type = self.listelements()
            type.remove("fontNumber")
        elif isinstance(type, str):
            type = [type, ]
        elif not isinstance(type, (list, tuple)):
            return
        for objtype in type:
            for obj in self.listelements(objtype):
                if obj[:2] == "__":
                    try:
                        loc = locals()
                        exec("o = self.get%s(obj)" % objtype)
                        o = loc["o"]
                        destroy = True
                        if objtype == 'template':
                            # print o.name
                            dnames = self.return_display_names()
                            for d in dnames:
                                dpy = self.getplot(d)
                                if o.name in [
                                        dpy.template, dpy._template_origin]:
                                    destroy = False
                                    break
                        if destroy:
                            self.removeobject(o)
                    except Exception:
                        pass

        return

    def check_name_source(self, name, source, typ):
        return vcs.check_name_source(name, source, typ)
    check_name_source.__doc__ = vcs.manageElements.check_name_source.__doc__

    def createtemplate(self, name=None, source='default'):
        return vcs.createtemplate(name, source)
    createtemplate.__doc__ = vcs.manageElements.createtemplate.__doc__

    def gettemplate(self, Pt_name_src='default'):
        return vcs.gettemplate(Pt_name_src)
    gettemplate.__doc__ = vcs.manageElements.gettemplate.__doc__

    def createprojection(self, name=None, source='default'):
        return vcs.createprojection(name, source)
    createprojection.__doc__ = vcs.manageElements.createprojection.__doc__

    def getprojection(self, Proj_name_src='default'):
        return vcs.getprojection(Proj_name_src)
    getprojection.__doc__ = vcs.manageElements.getprojection.__doc__

    def createboxfill(self, name=None, source='default'):
        return vcs.createboxfill(name, source)
    createboxfill.__doc__ = vcs.manageElements.createboxfill.__doc__

    def getboxfill(self, Gfb_name_src='default'):
        return vcs.getboxfill(Gfb_name_src)
    getboxfill.__doc__ = vcs.manageElements.getboxfill.__doc__

    def boxfill(self, *args, **parms):
        """Generate a boxfill plot given the data, boxfill graphics method, and
        template. If no boxfill object is given, then the 'default' boxfill
        graphics method is used. Similarly, if no template object is given,
        then the 'default' template is used.

        :Example:

            .. doctest:: canvas_boxfill

                >>> a=vcs.init()
                >>> a.show('boxfill') # Show all boxfills
                *******************Boxfill Names List**********************
                ...
                *******************End Boxfill Names List**********************
                >>> box=a.getboxfill('quick') # Create instance of 'quick'
                >>> arr=[range(10) for _ in range(10)] # data to plot
                >>> a.boxfill(arr, box) # Plot array w/ box; default template
                <vcs.displayplot.Dp ...>
                >>> t = a.gettemplate('quick') # get quick template
                >>> a.clear() # Clear VCS canvas
                >>> a.boxfill(arr, box, t) # Plot w/ box and 'quick' template
                <vcs.displayplot.Dp ...>
                >>> a.boxfill(box, arr, t) # Plot w/ box and 'quick' template
                <vcs.displayplot.Dp ...>
                >>> a.boxfill(t, arr, box) # Plot w/ box and 'quick' template
                <vcs.displayplot.Dp ...>
                >>> a.boxfill(t, box, arr) # Plot w/ box and 'quick' template
                <vcs.displayplot.Dp ...>
                >>> a.boxfill(arr, 'polar', 'polar') # 'polar' template/boxfill
                <vcs.displayplot.Dp ...>
                >>> a.boxfill('polar', arr, 'polar') # 'polar' template/boxfill
                <vcs.displayplot.Dp ...>
                >>> a.boxfill('polar', 'polar', arr) # 'polar' template/boxfill
                <vcs.displayplot.Dp ...>

            .. note::

                As shown above, the data, 'template', and 'box' parameters can be provided in any order.
                The 'template' and 'box' parameters can either be VCS template and boxfill objects,
                or string names of template and boxfill objects.

                The first string provided is assumed to be a template name. The second is assumed to be a
                boxfill name.

        %s
        %s
        %s
        %s
        %s
        """
        arglist = _determine_arg_list('boxfill', args)
        return self.__plot(arglist, parms)
    boxfill.__doc__ = boxfill.__doc__ % (
        plot_keywords_doc, graphics_method_core, axesconvert, plot_2D_input, plot_output)

    def createtaylordiagram(self, name=None, source='default'):
        return vcs.createtaylordiagram(name, source)
    createtaylordiagram.__doc__ = vcs.manageElements.createtaylordiagram.__doc__

    def gettaylordiagram(self, Gtd_name_src='default'):
        return vcs.gettaylordiagram(Gtd_name_src)
    gettaylordiagram.__doc__ = vcs.manageElements.gettaylordiagram.__doc__

    def taylordiagram(self, *args, **parms):
        """Generate a taylordiagram plot given the data, taylordiagram graphics method, and
        template. If no taylordiagram object is given, then the 'default' taylordiagram
        graphics method is used. Similarly, if no template object is given,
        then the 'default' template is used.

        :Example:

            .. doctest:: canvas_taylordiagram

                >>> a=vcs.init()
                >>> a.show('taylordiagram') # Show all the existing taylordiagram graphics methods
                *******************Taylordiagram Names List**********************
                ...
                *******************End Taylordiagram Names List**********************
                >>> td= a.gettaylordiagram() # Create instance of 'default'
                >>> array=[range(1, 11) for _ in range(1, 11)]
                >>> a.taylordiagram(array,td) # Plot array using specified iso and default template
                <vcs.displayplot.Dp ...>
                >>> a.clear() # Clear VCS canvas
                >>> template=a.gettemplate('hovmuller')
                >>> a.taylordiagram(array,td,template) # Plot array using specified iso and template
                <vcs.displayplot.Dp ...>

        :returns: A VCS displayplot object.
        :rtype: vcs.displayplot.Dp
        """
        arglist = _determine_arg_list('taylordiagram', args)
        return self.__plot(arglist, parms)

    def createmeshfill(self, name=None, source='default'):
        return vcs.createmeshfill(name, source)
    createmeshfill.__doc__ = vcs.manageElements.createmeshfill.__doc__

    def getmeshfill(self, Gfm_name_src='default'):
        return vcs.getmeshfill(Gfm_name_src)
    getmeshfill.__doc__ = vcs.manageElements.getmeshfill.__doc__

    def meshfill(self, *args, **parms):  # noqa
        """Generate a meshfill plot given the data, the mesh, a meshfill graphics method, and
        a template. If no meshfill object is given, then the 'default' meshfill
        graphics method is used. Similarly, if no template object is given,
        then the 'default' template is used.

        Format:
        This function expects 1D data (any extra dimension will be used for animation)
        In addition the mesh array must be of the same shape than data with 2 additional dimension
        representing the vertices coordinates for the Y (0) and X (1) dimension
        Let's say you want to plot a spatial assuming mesh containing 10,000 grid cell, then data must be shape (10000,)
        or (n1,n2,n3,...,10000) if additional dimensions exist (ex time,level), these dimensions would be used only
        for animation and will be ignored in the rest of this example.
        The shape of the mesh, assuming 4 vertices per grid cell, must be (1000,2,4), where the array [:,0,:]
        represent the Y coordinates of the vertices (clockwise or counterclockwise) and the array [:,1:]
        represents the X coordinates of the vertices (the same clockwise/counterclockwise than the Y coordinates)
        In brief you'd have:
        data.shape=(10000,)
        mesh.shape=(10000,2,4)

        :Example:

            .. doctest:: canvas_meshfill

                >>> a=vcs.init()
                >>> a.show('meshfill') # Show all meshfill graphics methods
                *******************Meshfill Names List**********************
                ...
                *******************End Meshfill Names List**********************
                >>> import cdms2 # Need cdms2 to create a slab
                >>> f = cdms2.open(vcs.sample_data+'/clt.nc') # open data file
                >>> slab = f('clt') # use data file to create a cdms2 slab
                >>> m=a.getmeshfill() # Create instance of 'default'
                >>> a.meshfill(slab,m) # Plot with default mesh & template
                <vcs.displayplot.Dp ...>
                >>> a.clear() # Clear VCS canvas
                >>> p='a_polar_meshfill' # will use this to plot
                >>> a.meshfill(slab,m,'quick', p) # polar mesh, quick template
                <vcs.displayplot.Dp ...>

        :returns: A VCS displayplot object.
        :rtype: vcs.displayplot.Dp
        """
        arglist = _determine_arg_list('meshfill', args)
        return self.__plot(arglist, parms)

    def create3d_scalar(self, name=None, source='default'):
        return vcs.create3d_scalar(name, source)

    create3d_scalar.__doc__ = vcs.manageElements.create3d_scalar.__doc__

    def get3d_scalar(self, Gfdv3d_name_src='default'):
        return vcs.get3d_scalar(Gfdv3d_name_src)
    get3d_scalar.__doc__ = vcs.manageElements.get3d_scalar.__doc__

    def scalar3d(self, *args, **parms):
        """Generate a 3d_scalar plot given the data, 3d_scalar
        graphics method, and template. If no 3d_scalar object is given,
        then the 'default' 3d_scalar graphics method is used.
        Similarly, if no template is given, the 'default' template is used.

        :Example:

            .. doctest:: canvas_scalar3d

                >>> a=vcs.init()
                >>> a.show('3d_scalar') # Show all 3d_scalars
                *******************3d_scalar Names List**********************
                ...
                *******************End 3d_scalar Names List**********************
                >>> ds=a.get3d_scalar() # default 3d_scalar
                >>> import cdms2 # Need cdms2 to create a slab
                >>> f = cdms2.open(vcs.sample_data+'/clt.nc') # get data file
                >>> s = f('clt') # use data file to create a cdms2 slab
                >>> # Plot slab with defaults
                >>> a.scalar3d(ds, s) # doctest:+SKIP
                initCamera: Camera => (...)
                <vcs.displayplot.Dp ...>
                >>> a.clear() # Clear VCS canvas
                >>> t = a.gettemplate('polar')
                >>> # Plot with 'polar' template
                >>> a.scalar3d(s, ds, t)  # doctest:+SKIP
                initCamera: Camera => (...)
                <vcs.displayplot.Dp ...>
        """
        arglist = _determine_arg_list('3d_scalar', args)
        return self.__plot(arglist, parms)

    def create3d_vector(self, name=None, source='default'):
        return vcs.create3d_vector(name, source)

    create3d_vector.__doc__ = vcs.manageElements.create3d_vector.__doc__

    def get3d_vector(self, Gfdv3d_name_src='default'):
        return vcs.get3d_vector(Gfdv3d_name_src)
    get3d_vector.__doc__ = vcs.manageElements.get3d_vector.__doc__

    def vector3d(self, *args, **parms):
        """Generate a 3d_vector plot given the data, 3d_vector
        graphics method, and template. If no 3d_vector object is given,
        then the 'default' 3d_vector graphics method is used.
        Similarly, if no template is given, the 'default' template is used.

        .. note::

            3d_vectors need 2 data objects (slabs) to plot.

            :Example:

                .. doctest:: canvas_vector3d

                    >>> a=vcs.init()
                    >>> a.show('3d_vector') # Show all 3d_vectors
                    *******************3d_vector Names List**********************
                    ...
                    *******************End 3d_vector Names List**********************
                    >>> dv3=a.get3d_vector() # default 3d_vector
                    >>> import cdms2 # Need cdms2 to create a slab
                    >>> f = cdms2.open(vcs.sample_data+'/clt.nc') # get data file
                    >>> s = f('u') # use data file to create a cdms2 slab
                    >>> s2 = f('v') # need two slabs, so get another
                    >>> # Plot slabs
                    >>> a.vector3d(dv3, s, s2)  # doctest:+SKIP
                    Sample rate: 6
                    Sample rate: 6
                    initCamera: Camera => (...)
                    <vcs.displayplot.Dp ...>
                    >>> a.clear() # Clear VCS canvas
                    >>> t = a.gettemplate('polar')
                    >>> # Plot with 'polar' template
                    >>> a.vector3d(s, s2, dv3, t)  # doctest:+SKIP
                    Sample rate: 6
                    Sample rate: 6
                    initCamera: Camera => (...)
                    <vcs.displayplot.Dp ...>
        """
        arglist = _determine_arg_list('3d_vector', args)
        return self.__plot(arglist, parms)

    def create3d_dual_scalar(self, name=None, source='default'):
        return vcs.create3d_dual_scalar(name, source)

    create3d_dual_scalar.__doc__ = vcs.manageElements.create3d_dual_scalar.__doc__

    def get3d_dual_scalar(self, Gfdv3d_name_src='default'):
        return vcs.get3d_dual_scalar(Gfdv3d_name_src)
    get3d_dual_scalar.__doc__ = vcs.manageElements.get3d_dual_scalar.__doc__

    def dual_scalar3d(self, *args, **parms):
        """Generate a 3d_dual_scalar plot given the data, 3d_dual_scalar
        graphics method, and template. If no 3d_dual_scalar object is given,
        then the 'default' 3d_dual_scalar graphics method is used.
        Similarly, if no template is given, the 'default' template is used.

        .. note::

            3d_dual_scalars need 2 data objects (slabs) to plot.

            :Example:

                .. doctest:: canvas_dual_scalar3d

                    >>> a=vcs.init()
                    >>> a.show('3d_dual_scalar') # Show all 3d_dual_scalars
                    *******************3d_dual_scalar Names List**********************
                    ...
                    *******************End 3d_dual_scalar Names List**********************
                    >>> ds3=a.get3d_dual_scalar() # default 3d_dual_scalar
                    >>> import cdms2 # Need cdms2 to create a slab
                    >>> f = cdms2.open(vcs.sample_data+'/clt.nc') # get data file
                    >>> s = f('clt') # use data file to create a cdms2 slab
                    >>> s2 = f('v') # need two slabs, so get another
                    >>> # Plot slabs
                    >>> a.dual_scalar3d(ds3, s, s2)  # doctest:+SKIP
                    initCamera: Camera => (...)
                    <vcs.displayplot.Dp ...>
                    >>> a.clear() # Clear VCS canvas
                    >>> t = a.gettemplate('polar')
                    >>> # Plot w/ 'polar' template
                    >>> a.dual_scalar3d(s,s2,ds3,t)  # doctest:+SKIP
                    initCamera: Camera => (...)
                    <vcs.displayplot.Dp ...>
        """
        arglist = _determine_arg_list('3d_dual_scalar', args)
        return self.__plot(arglist, parms)

    def createisofill(self, name=None, source='default'):
        return vcs.createisofill(name, source)
    createisofill.__doc__ = vcs.manageElements.createisofill.__doc__

    def getisofill(self, Gfi_name_src='default'):
        return vcs.getisofill(Gfi_name_src)
    getisofill.__doc__ = vcs.manageElements.getisofill.__doc__

    def isofill(self, *args, **parms):
        """Generate an isofill plot given the data, isofill graphics method, and
        template. If no isofill object is given, then the 'default' isofill
        graphics method is used. Similarly, if no template object is given,
        then the 'default' template is used.

        :Example:

            .. doctest:: canvas_isofill

                >>> a=vcs.init()
                >>> a.show('isofill') # Show all isofill graphics methods
                *******************Isofill Names List**********************
                ...
                *******************End Isofill Names List**********************
                >>> iso=a.getisofill('quick') # Create instance of 'quick'
                >>> import cdms2 # Need cdms2 to create a slab
                >>> f = cdms2.open(vcs.sample_data+'/clt.nc') # get data file
                >>> slab = f('clt') # use data file to create a cdms2 slab
                >>> a.isofill(slab,iso) # Plot slab with iso; default template
                <vcs.displayplot.Dp ...>
                >>> a.clear() # Clear VCS canvas
                >>> t = a.gettemplate('hovmuller')
                >>> a.isofill(slab,iso,t) # Plot with 'hovmuller' template
                <vcs.displayplot.Dp ...>

        %s
        %s
        %s
        %s
        %s
        """
        arglist = _determine_arg_list('isofill', args)
        return self.__plot(arglist, parms)
    isofill.__doc__ = isofill.__doc__ % (
        plot_keywords_doc, graphics_method_core, axesconvert, plot_2D_input, plot_output)

    def createisoline(self, name=None, source='default'):
        return vcs.createisoline(name, source)
    createisoline.__doc__ = vcs.manageElements.createisoline.__doc__

    def getisoline(self, Gi_name_src='default'):
        return vcs.getisoline(Gi_name_src)
    getisoline.__doc__ = vcs.manageElements.getisoline.__doc__

    def isoline(self, *args, **parms):
        """Generate a isoline plot given the data, isoline graphics method, and
        template. If no isoline object is given, then the 'default' isoline
        graphics method is used. Similarly, if no template object is given,
        then the 'default' template is used.

        :Example:

            .. doctest:: canvas_isoline

                >>> a=vcs.init()
                >>> a.show('isoline') # Show all the existing isoline graphics methods
                *******************Isoline Names List**********************
                ...
                *******************End Isoline Names List**********************
                >>> iso=a.getisoline('quick') # Create instance of 'quick'
                >>> array = [range(1, 11) for _ in range(1, 11)]
                >>> a.isoline(array,iso) # Plot array using specified iso and default template
                <vcs.displayplot.Dp ...>
                >>> a.clear() # Clear VCS canvas
                >>> template = a.gettemplate('hovmuller')
                >>> a.isoline(array,iso,template)  # Plot array using specified iso and template
                <vcs.displayplot.Dp ...>

        %s
        %s
        %s
        %s
        %s
        """
        arglist = _determine_arg_list('isoline', args)
        return self.__plot(arglist, parms)
    isoline.__doc__ = isoline.__doc__ % (
        plot_keywords_doc, graphics_method_core, axesconvert, plot_2D_input, plot_output)

    def create1d(self, name=None, source='default'):
        return vcs.create1d(name, source)
    create1d.__doc__ = vcs.manageElements.create1d.__doc__

    def get1d(self, name):
        return vcs.get1d(name)
    get1d.__doc__ = vcs.manageElements.get1d.__doc__

    def createxyvsy(self, name=None, source='default'):
        return vcs.createxyvsy(name, source)
    createxyvsy.__doc__ = vcs.manageElements.createxyvsy.__doc__

    def getxyvsy(self, GXy_name_src='default'):
        return vcs.getxyvsy(GXy_name_src)
    getxyvsy.__doc__ = vcs.manageElements.getxyvsy.__doc__

    def xyvsy(self, *args, **parms):
        """Generate a Xyvsy plot given the data, Xyvsy graphics method, and
        template. If no Xyvsy object is given, then the 'default' Xyvsy
        graphics method is used. Similarly, if no template object is given,
        then the 'default' template is used.

        :Example:

            .. doctest:: canvas_xyvsy

                >>> a=vcs.init()
                >>> a.show('xyvsy') # Show all the existing Xyvsy graphics methods
                *******************Xyvsy Names List**********************
                ...
                *******************End Xyvsy Names List**********************
                >>> xyy=a.getxyvsy('default_xyvsy_') # Create instance of default xyvsy
                >>> array=[range(1, 11) for _ in range(1, 11)]
                >>> a.xyvsy(array,xyy) # Plot array using specified xyy and default template
                <vcs.displayplot.Dp ...>
                >>> a.clear() # Clear VCS canvas
                >>> template=a.gettemplate('hovmuller')
                >>> a.xyvsy(array,xyy,template) # Plot array using specified xyy and template
                <vcs.displayplot.Dp ...>

        %s
        %s
        %s
        %s
        %s
        """
        arglist = _determine_arg_list('xyvsy', args)
        return self.__plot(arglist, parms)
    xyvsy.__doc__ = xyvsy.__doc__ % (
        plot_keywords_doc, graphics_method_core, xaxisconvert, plot_1D_input, plot_output)

    def createyxvsx(self, name=None, source='default'):
        return vcs.createyxvsx(name, source)
    createyxvsx.__doc__ = vcs.manageElements.createyxvsx.__doc__

    def getyxvsx(self, GYx_name_src='default'):
        return vcs.getyxvsx(GYx_name_src)
    getyxvsx.__doc__ = vcs.manageElements.getyxvsx.__doc__

    def yxvsx(self, *args, **parms):
        """Generate a Yxvsx plot given the data, Yxvsx graphics method, and
        template. If no Yxvsx object is given, then the 'default' Yxvsx
        graphics method is used. Simerly, if no template object is given,
        then the 'default' template is used.

        :Example:

            .. doctest:: canvas_yxvsx

                >>> a=vcs.init()
                >>> a.show('yxvsx') # Show all the existing Yxvsx graphics methods
                *******************Yxvsx Names List**********************
                ...
                *******************End Yxvsx Names List**********************
                >>> yxx=a.getyxvsx('default_yxvsx_') # Create instance of default yxvsx
                >>> array=[range(1, 11) for _ in range(1, 11)]
                >>> a.yxvsx(array,yxx) # Plot array using specified yxx and default template
                <vcs.displayplot.Dp ...>
                >>> a.clear() # Clear VCS canvas
                >>> template=a.gettemplate('hovmuller')
                >>> a.yxvsx(array,yxx,template) # Plot array using specified yxx and template
                <vcs.displayplot.Dp ...>

        %s
        %s
        %s
        %s
        %s
        """
        arglist = _determine_arg_list('yxvsx', args)
        return self.__plot(arglist, parms)
    yxvsx.__doc__ = yxvsx.__doc__ % (
        plot_keywords_doc, graphics_method_core, xaxisconvert, plot_1D_input, plot_output)

    def createxvsy(self, name=None, source='default'):
        return vcs.createxvsy(name, source)
    createxvsy.__doc__ = vcs.manageElements.createxvsy.__doc__

    def getxvsy(self, GXY_name_src='default'):
        return vcs.getxvsy(GXY_name_src)
    getxvsy.__doc__ = vcs.manageElements.getxvsy.__doc__

    def xvsy(self, *args, **parms):
        """Generate a XvsY plot given the data, XvsY graphics method, and
        template. If no XvsY object is given, then the 'default' XvsY
        graphics method is used. Similarly, if no template object is given,
        then the 'default' template is used.

        :Example:

            .. doctest:: canvas_xvsy

                >>> a=vcs.init()
                >>> a.show('xvsy') # Show all the existing XvsY graphics methods
                *******************Xvsy Names List**********************
                ...
                *******************End Xvsy Names List**********************
                >>> xy=a.getxvsy('default_xvsy_') # Create instance of default xvsy
                >>> import cdms2 # Need cdms2 to create a slab
                >>> f = cdms2.open(vcs.sample_data+'/clt.nc') # use cdms2 to open a data file
                >>> slab1 = f('u') # use the data file to create a cdms2 slab
                >>> slab2 = f('v') # use the data file to create a cdms2 slab
                >>> a.xvsy(slab1,slab2,xy) # Plot array using specified xy and default template
                <vcs.displayplot.Dp ...>
                >>> a.clear() # Clear VCS canvas
                >>> template=a.gettemplate('hovmuller')
                >>> a.xvsy(slab1,slab2,xy,template) # Plot array using specified xy and template
                <vcs.displayplot.Dp ...>

        %s
        %s
        %s
        %s
        %s
        """
        arglist = _determine_arg_list('xvsy', args)
        return self.__plot(arglist, parms)
    xvsy.__doc__ = xvsy.__doc__ % (plot_keywords_doc,
                                   graphics_method_core,
                                   axesconvert,
                                   plot_2_1D_input,
                                   plot_output)

    def createvector(self, name=None, source='default'):
        return vcs.createvector(name, source)
    createvector.__doc__ = vcs.manageElements.createvector.__doc__

    def getvector(self, Gv_name_src='default'):
        return vcs.getvector(Gv_name_src)
    getvector.__doc__ = vcs.manageElements.getvector.__doc__

    def vector(self, *args, **parms):
        """Generate a vector plot given the data, vector graphics method, and
        template. If no vector object is given, then the 'default' vector
        graphics method is used. Similarly, if no template object is given,
        then the 'default' template is used.

        :Example:

            .. doctest:: canvas_vector

                >>> a=vcs.init()
                >>> a.show('vector') # Show all the existing vector graphics methods
                *******************Vector Names List**********************
                ...
                *******************End Vector Names List**********************
                >>> import cdms2 # Need cdms2 to create a slab
                >>> f = cdms2.open(vcs.sample_data+'/clt.nc') # use cdms2 to open a data file
                >>> slab1 = f('u') # use the data file to create a cdms2 slab
                >>> slab2 = f('v') # vector needs 2 slabs, so get another
                >>> a.vector(slab1, slab2) # plot vector using slab and default vector
                <vcs.displayplot.Dp ...>
                >>> a.clear() # Clear VCS canvas
                >>> template=a.gettemplate('hovmuller')
                >>> a.vector(slab1, slab2, template) # Plot array using default vector and specified template
                <vcs.displayplot.Dp ...>

        :returns: A VCS displayplot object.
        :rtype: vcs.displayplot.Dp
        """
        arglist = _determine_arg_list('vector', args)
        return self.__plot(arglist, parms)

    def createstreamline(self, name=None, source='default'):
        return vcs.createstreamline(name, source)
    createstreamline.__doc__ = vcs.manageElements.createstreamline.__doc__

    def getstreamline(self, Gv_name_src='default'):
        return vcs.getstreamline(Gv_name_src)
    getstreamline.__doc__ = vcs.manageElements.getstreamline.__doc__

    def streamline(self, *args, **parms):
        """

        Generate a streamline plot given the data, streamline graphics method,
        and template. If no streamline class object is given, then the 'default'
        streamline graphics method is used. Similarly, if no template class
        object is given, then the 'default' template is used.

        :Example:

            .. doctest:: canvas_streamline

                >>> a=vcs.init()
                >>> a.show('streamline') # Show all the existing streamline graphics methods
                *******************Streamline Names List**********************
                ...
                *******************End Streamline Names List**********************
                >>> import cdms2 # Need cdms2 to create a slab
                >>> f = cdms2.open(vcs.sample_data+'/clt.nc') # open a data file
                >>> slab1 = f('u') # use the data file to create a cdms2 slab
                >>> slab2 = f('v') # streamline needs 2 slabs, so get another
                >>> # plot streamline using slab and default
                >>> # streamline
                >>> a.streamline(slab1, slab2)
                <vcs.displayplot.Dp ...>
                >>> a.clear() # Clear VCS canvas
                >>> template=a.gettemplate('hovmuller')
                >>> # Plot array using default streamline
                >>> # and specified template
                >>> a.streamline(slab1, slab2, template)
                <vcs.displayplot.Dp ...>

        :returns: A VCS displayplot object.
        :rtype: vcs.displayplot.Dp
        """
        arglist = _determine_arg_list('streamline', args)
        return self.__plot(arglist, parms)

    def createscatter(self, name=None, source='default'):
        return vcs.createscatter(name, source)
    createscatter.__doc__ = vcs.manageElements.createscatter.__doc__

    def getscatter(self, GSp_name_src='default'):
        return vcs.getscatter(GSp_name_src)
    getscatter.__doc__ = vcs.manageElements.getscatter.__doc__

    def scatter(self, *args, **parms):
        """Generate a scatter plot given the data, scatter graphics method, and
        template. If no scatter object is given, then the 'default' scatter
        graphics method is used. Similarly, if no template object is given,
        then the 'default' template is used.

        :Example:

            .. doctest:: canvas_scatter

                >>> a=vcs.init()
                >>> a.show('scatter') # Show all the existing scatter graphics methods
                *******************Scatter Names List**********************
                ...
                *******************End Scatter Names List**********************
                >>> import cdms2 # Need cdms2 to create a slab
                >>> f = cdms2.open(vcs.sample_data+'/clt.nc') # use cdms2 to open a data file
                >>> slab1 = f('u') # use the data file to create a cdms2 slab
                >>> slab2 = f('v') # need 2 slabs, so get another
                >>> a.scatter(slab1, slab2) # Plot array using specified sct and default template
                <vcs.displayplot.Dp ...>
                >>> a.clear() # Clear VCS canvas
                >>> template=a.gettemplate('hovmuller')
                >>> a.scatter(slab1, slab2, template) # Plot array using specified sct and template
                <vcs.displayplot.Dp ...>

        %s
        %s
        %s
        %s
        %s
        """

        arglist = _determine_arg_list('scatter', args)
        return self.__plot(arglist, parms)
    scatter.__doc__ = scatter.__doc__ % (
        plot_keywords_doc, graphics_method_core, axesconvert, plot_2_1D_input, plot_output)

    def createline(self, name=None, source='default', ltype=None,  # noqa
                   width=None, color=None, priority=None,
                   viewport=None, worldcoordinate=None,
                   x=None, y=None, projection=None):
        return vcs.createline(name, source, ltype, width, color,
                              priority, viewport, worldcoordinate, x, y, projection)
    createline.__doc__ = vcs.manageElements.createline.__doc__

    def getline(self, name='default', ltype=None, width=None, color=None,
                priority=None, viewport=None,
                worldcoordinate=None,
                x=None, y=None):
        return vcs.getline(
            name, ltype, width, color, priority, viewport, worldcoordinate, x, y)
    getline.__doc__ = vcs.manageElements.getline.__doc__

    def line(self, *args, **parms):
        """Plot a line segment on the Vcs Canvas. If no line class
        object is given, then an error will be returned.

        :Example:

            .. doctest:: canvas_line

                >>> a=vcs.init()
                >>> a.show('line')  # Show all the existing line objects
                *******************Line Names List**********************
                ...
                *******************End Line Names List**********************
                >>> ln=a.getline('red') # Create instance of 'red'
                >>> ln.width=4 # Set the line width
                >>> ln.color = 242 # Set the line color
                >>> ln.type = 4 # Set the line type
                >>> ln.x=[[0.0,2.0,2.0,0.0,0.0], [0.5,1.5]] # Set the x value points
                >>> ln.y=[[0.0,0.0,2.0,2.0,0.0], [1.0,1.0]] # Set the y value points
                >>> a.line(ln) # Plot using specified line object
                <vcs.displayplot.Dp ...>

        :returns: A VCS displayplot object.
        :rtype: vcs.displayplot.Dp
        """
        arglist = _determine_arg_list('line', args)
        return self.__plot(arglist, parms)

    def drawline(self, name=None, ltype='solid', width=1, color=241,  # noqa
                 priority=1, viewport=[0.0, 1.0, 0.0, 1.0],
                 worldcoordinate=[0.0, 1.0, 0.0, 1.0],
                 x=None, y=None, projection='default', bg=0):
        """Generate and draw a line object on the VCS Canvas.

        :Example:

            .. doctest:: canvas_drawline

                >>> a=vcs.init()
                >>> a.show('line') # Show all the existing line objects
                *******************Line Names List**********************
                ...
                *******************End Line Names List**********************
                >>> ln=a.drawline(name='red', ltype='dash', width=2,
                ...              color=242, priority=1, viewport=[0, 1.0, 0, 1.0],
                ...              worldcoordinate=[0,100, 0,50],
                ...              x=[0,20,40,60,80,100],
                ...              y=[0,10,20,30,40,50] )
                >>> a.line(ln) # Plot using specified line object
                <vcs.displayplot.Dp ...>

        %s

        :param ltype: One of "dash", "dash-dot", "solid", "dot", or "long-dash".
        :type ltype: `str`_

        :param width: Thickness of the line to be drawn
        :type width: `int`_

        %s
        %s
        %s
        %s
        %s
        %s

        :returns: A VCS line object
        :rtype: vcs.line.Tl
        """
        if (name is None) or (not isinstance(name, str)):
            raise vcsError('Must provide string name for the line.')
        else:
            lo = self.listelements('line')
            if name in lo:
                ln = self.getline(name)
            else:
                ln = self.createline(name)
        ln.type = ltype
        ln.width = width
        ln.color = color
        ln.priority = priority
        ln.viewport = viewport
        ln.worldcoordinate = worldcoordinate
        ln.x = x
        ln.y = y
        ln.projection = projection
        self.line(ln, bg=bg)

        return ln
    drawline.__doc__ = drawline.__doc__ % (xmldocs.name, xmldocs.color, xmldocs.priority, xmldocs.viewport,
                                           xmldocs.worldcoordinate, xmldocs.x_y_coords, xmldocs.projection)

    def createmarker(self, name=None, source='default', mtype=None,  # noqa
                     size=None, color=None, priority=1,
                     viewport=None, worldcoordinate=None,
                     x=None, y=None, projection=None):
        return vcs.createmarker(name, source, mtype, size, color, priority,
                                viewport, worldcoordinate, x, y, projection)
    createmarker.__doc__ = vcs.manageElements.createmarker.__doc__

    def getmarker(self, name='default', mtype=None, size=None, color=None,
                  priority=None, viewport=None,
                  worldcoordinate=None,
                  x=None, y=None):
        return vcs.getmarker(
            name, mtype, size, color, priority, viewport, worldcoordinate, x, y)
    getmarker.__doc__ = vcs.manageElements.getmarker.__doc__

    def marker(self, *args, **parms):
        """Plot a marker segment on the Vcs Canvas. If no marker class
        object is given, then an error will be returned.

        :Example:

            .. doctest:: canvas_marker

                >>> a=vcs.init()
                >>> a.show('marker') # Show all the existing marker objects
                *******************Marker Names List**********************
                ...
                *******************End Marker Names List**********************
                >>> mrk=a.getmarker('red') # Create instance of 'red'
                >>> mrk.size=4 # Set the marker size
                >>> mrk.color = 242 # Set the marker color
                >>> mrk.type = 4 # Set the marker type
                >>> mrk.x=[[0.0,2.0,2.0,0.0,0.0], [0.5,1.5]] # Set the x value points
                >>> mrk.y=[[0.0,0.0,2.0,2.0,0.0], [1.0,1.0]] # Set the y value points
                >>> a.marker(mrk) # Plot using specified marker object
                <vcs.displayplot.Dp ...>

        :returns: a VCS displayplot object
        :rtype: vcs.displayplot.Dp
        """
        arglist = _determine_arg_list('marker', args)
        return self.__plot(arglist, parms)

    def drawmarker(self, name=None, mtype='solid', size=1, color=241,
                   priority=1, viewport=[0.0, 1.0, 0.0, 1.0],
                   worldcoordinate=[0.0, 1.0, 0.0, 1.0],
                   x=None, y=None, bg=0):
        """Generate and draw a marker object on the VCS Canvas.

        :Example:

            .. doctest:: canvas_drawmarker

                >>> a=vcs.init()
                >>> a.show('marker')  # Show all the existing marker objects
                *******************Marker Names List**********************
                ...
                *******************End Marker Names List**********************
                >>> mrk=a.drawmarker(name='red', mtype='dot', size=2,
                ...              color=242, priority=1, viewport=[0, 1.0, 0, 1.0],
                ...              worldcoordinate=[0,100, 0,50],
                ...              x=[0,20,40,60,80,100],
                ...              y=[0,10,20,30,40,50] ) # Create instance of marker object 'red'
                >>> a.marker(mrk) # Plot using specified marker object
                <vcs.displayplot.Dp ...>

        %s

        :param mtype: Marker type, i.e. 'dot', 'plus', 'star, etc.
        :type mtype: `str`_

        :param size: Size of the marker to draw
        :type size: `int`_

        %s
        %s
        %s
        %s
        %s
        %s

        :returns: A drawmarker object
        :rtype: vcs.marker.Tm
        """
        if (name is None) or (not isinstance(name, str)):
            raise vcsError('Must provide string name for the marker.')
        else:
            lo = self.listelements('marker')
            if name in lo:
                mrk = self.getmarker(name)
            else:
                mrk = self.createmarker(name)
        mrk.type = mtype
        mrk.size = size
        mrk.color = color
        mrk.priority = priority
        mrk.viewport = viewport
        mrk.worldcoordinate = worldcoordinate
        mrk.x = x
        mrk.y = y
        self.marker(mrk, bg=bg)

        return mrk

    drawmarker.__doc__ = drawmarker.__doc__ % (xmldocs.name, xmldocs.color, xmldocs.priority, xmldocs.viewport,
                                               xmldocs.worldcoordinate, xmldocs.x_y_coords, xmldocs.bg)

    def createfillarea(self, name=None, source='default', style=None,
                       index=None, color=None, priority=1,
                       viewport=None, worldcoordinate=None,
                       x=None, y=None):
        return vcs.createfillarea(
            name, source, style, index, color, priority, viewport, worldcoordinate, x, y)
    createfillarea.__doc__ = vcs.manageElements.createfillarea.__doc__

    def getfillarea(self, name='default', style=None,
                    index=None, color=None,
                    priority=None, viewport=None,
                    worldcoordinate=None,
                    x=None, y=None):
        return vcs.getfillarea(
            name, style, index, color, priority, viewport, worldcoordinate, x, y)
    getfillarea.__doc__ = vcs.manageElements.getfillarea.__doc__

    def fillarea(self, *args, **parms):
        """Generate a fillarea plot

        Plot a fillarea segment on the Vcs Canvas. If no fillarea class
        object is given, then an error will be returned.

        :Example:

            .. doctest:: canvas_fillarea

                    >>> a=vcs.init()
                    >>> a.show('fillarea') # Show all fillarea objects
                    *******************Fillarea Names List**********************
                    ...
                    *******************End Fillarea Names List**********************
                    >>> fa=a.createfillarea() # instance of default fillarea
                    >>> fa.style=1 # Set fillarea style
                    >>> fa.index=4 # Set fillarea index
                    >>> fa.color = 242 # Set fillarea color
                    >>> fa.x=[0.25,0.75] # Set x value points
                    >>> fa.y=[0.2,0.5] # Set y value points
                    >>> a.fillarea(fa) # Plot using specified fillarea object
                    <vcs.displayplot.Dp ...>

        :returns: A fillarea object
        :rtype: vcs.displayplot.Dp
        """
        arglist = _determine_arg_list('fillarea', args)
        return self.__plot(arglist, parms)

    def drawfillarea(self, name=None, style=1, index=1, color=241,
                     priority=1, viewport=[0.0, 1.0, 0.0, 1.0],
                     worldcoordinate=[0.0, 1.0, 0.0, 1.0],
                     x=None, y=None, bg=0):
        """Generate and draw a fillarea object on the VCS Canvas.

        :Example:

            .. doctest:: canvas_drawfillarea

                >>> a=vcs.init()
                >>> a.show('fillarea') # Show all the existing fillarea objects
                *******************Fillarea Names List**********************
                ...
                *******************End Fillarea Names List**********************
                >>> fa=a.drawfillarea(name='red', style=1, color=242,
                ...              priority=1, viewport=[0, 1.0, 0, 1.0],
                ...              worldcoordinate=[0,100, 0,50],
                ...              x=[0,20,40,60,80,100],
                ...              y=[0,10,20,30,40,50], bg=0 ) # Create instance of fillarea object 'red'
                >>> a.fillarea(fa) # Plot using specified fillarea object
                <vcs.displayplot.Dp ...>

        %s

        :param style: One of "hatch", "solid", or "pattern".
        :type style: `str`_

        :param index: Specifies which `pattern`_ to fill the fillarea with.
            Accepts ints from 1-20.

        :type index: `int`_

        %s
        %s
        %s
        %s
        %s
        %s


        :returns: A fillarea object
        :rtype: vcs.fillarea.Tf

        .. _pattern: http://uvcdat.llnl.gov/gallery/fullsize/pattern_chart.png
        """
        if (name is None) or (not isinstance(name, str)):
            raise vcsError('Must provide string name for the fillarea.')
        else:
            lo = self.listelements('fillarea')
            if name in lo:
                fa = self.getfillarea(name)
            else:
                fa = self.createfillarea(name)
        fa.style = style
        fa.index = index
        fa.color = color
        fa.priority = priority
        fa.viewport = viewport
        fa.worldcoordinate = worldcoordinate
        fa.x = x
        fa.y = y
        self.fillarea(fa, bg=bg)

        return fa

    drawfillarea.__doc__ = drawfillarea.__doc__ % (xmldocs.name, xmldocs.color, xmldocs.priority, xmldocs.viewport,
                                                   xmldocs.worldcoordinate, xmldocs.x_y_coords, xmldocs.bg)

    def createtexttable(self, name=None, source='default', font=None,
                        spacing=None, expansion=None, color=None, priority=None,
                        viewport=None, worldcoordinate=None,
                        x=None, y=None):
        return vcs.createtexttable(name, source, font, spacing, expansion, color, priority,
                                   viewport, worldcoordinate, x, y)
    createtexttable.__doc__ = vcs.manageElements.createtexttable.__doc__

    def gettexttable(self, name='default', font=None,
                     spacing=None, expansion=None, color=None,
                     priority=None, viewport=None,
                     worldcoordinate=None,
                     x=None, y=None):
        return vcs.gettexttable(name, font, spacing, expansion, color, priority,
                                viewport, worldcoordinate, x, y)
    gettexttable.__doc__ = vcs.manageElements.gettexttable.__doc__

    def createtextorientation(self, name=None, source='default'):
        return vcs.createtextorientation(name, source)
    createtextorientation.__doc__ = vcs.manageElements.createtextorientation.__doc__

    def gettextorientation(self, To_name_src='default'):
        return vcs.gettextorientation(To_name_src)
    gettextorientation.__doc__ = vcs.manageElements.gettextorientation.__doc__

    def createtextcombined(self, Tt_name=None, Tt_source='default', To_name=None, To_source='default',  # noqa
                           font=None, spacing=None, expansion=None, color=None,
                           priority=None, viewport=None, worldcoordinate=None, x=None, y=None,
                           height=None, angle=None, path=None, halign=None, valign=None, projection=None):
        return vcs.createtextcombined(Tt_name, Tt_source, To_name, To_source,
                                      font, spacing, expansion, color, priority, viewport, worldcoordinate,
                                      x, y, height, angle, path, halign, valign, projection)
    createtextcombined.__doc__ = vcs.manageElements.createtextcombined.__doc__
    #
    # Set alias for the secondary createtextcombined.
    createtext = createtextcombined

    def gettextcombined(self, Tt_name_src='default', To_name_src=None, string=None,
                        font=None, spacing=None, expansion=None, color=None,
                        priority=None, viewport=None, worldcoordinate=None, x=None, y=None,
                        height=None, angle=None, path=None, halign=None, valign=None):
        return vcs.gettextcombined(Tt_name_src, To_name_src, string,
                                   font, spacing, expansion, color,
                                   priority, viewport, worldcoordinate,
                                   x, y, height, angle, path, halign, valign)
    gettextcombined.__doc__ = vcs.manageElements.gettextcombined.__doc__
    #
    # Set alias for the secondary gettextcombined.
    gettext = gettextcombined

    def textcombined(self, *args, **parms):
        """Plot a textcombined segment on the Vcs Canvas. If no textcombined class
        object is given, then an error will be returned.

        :Example:

        .. doctest:: canvas_textcombined

            >>> a=vcs.init()
            >>> a.clean_auto_generated_objects()
            >>> a.show('texttable') # Show all the existing texttable objects
            *******************Texttable Names List**********************
            ...
            *******************End Texttable Names List**********************
            >>> a.show('textorientation') # Show all the existing textorientation objects
            *******************Textorientation Names List**********************
            ...
            *******************End Textorientation Names List**********************
            >>> if "qa_tta" in vcs.listelements("texttable"): vcs.reset()
            ...
            >>> if "7left_tto" in vcs.listelements("textorientation"): vcs.reset()
            ...
            >>> vcs.createtext('qa_tta', 'qa', '7left_tto', '7left') # Create instance of 'qa_tt' and '7left_to'
            <vcs.textcombined.Tc object at ...>
            >>> tc=a.gettext('qa_tta', '7left_tto')
            >>> tc.string='Text1' # Show the string "Text1" on the VCS Canvas
            >>> tc.font=2 # Set the text size
            >>> tc.color=242 # Set the text color
            >>> tc.angle=45 # Set the text angle
            >>> tc.x=[0.5]
            >>> tc.y=[0.5]
            >>> a.textcombined(tc) # Plot using specified text object
            <vcs.displayplot.Dp ...>

        :returns: A fillarea object
        :rtype: vcs.displayplot.Dp
        """
        # First check if color is a string
        if 'color' in list(parms.keys()):
            if isinstance(parms['color'], type('')):
                parms['color'] = self.match_color(parms['color'])

        if not isinstance(args[0], vcs.textcombined.Tc):
            args = list(args)
            # Ok we have a user passed text object let's first create a random text combined
# icont=1
# while icont:
# n=random.randint(0,100000)
# try:
# t=self.createtextcombined('__'+str(n),'default','__'+str(n),'default')
# icont=0
# except Exception:
# pass
            t = self.createtextcombined()
            t.string = [args.pop(0)]
            t.x = [args.pop(0)]
            t.y = [args.pop(0)]
            # t.list()
            for k in list(parms.keys()):
                setattr(t, k, parms[k])
                del(parms[k])
            args.insert(0, t)
        arglist = _determine_arg_list('text', args)
        return self.__plot(arglist, parms)
    #
    # Set alias for the secondary textcombined.
    text = textcombined

    def gettextextent(self, textobject, angle=None):
        """Returns the coordinate of the box surrounding a text object once printed

        :Example:

            .. doctest:: canvas_gettextextent

                >>> a=vcs.init()
                >>> t=a.createtext()
                >>> t.x=[.5]
                >>> t.y=[.5]
                >>> t.string=['Hello World']
                >>> a.gettextextent(t)
                [[...]]

        :param textobject: A VCS text object
        :param angle: If not None overwrites the textobject's angle (in degrees)
        :type textobject: vcs.textcombined.Tc

        :returns: list of floats containing the coordinates of the text object's bounding box.
        coordinates are appropriate within the same viewport and worldcoordinate as the input textobject
        :rtype: `list`_
        """
        if not vcs.istext(textobject):
            raise vcsError('You must pass a text object')
        To = textobject.To_name
        Tt = textobject.Tt_name
        return self.backend.gettextextent(To, Tt, angle)

    def gettextbox(self, textobject):
        """Returns the coordinate of the exact and rotated box surrounding a text object once printed

        :Example:

            .. doctest:: canvas_gettextbox

                >>> a=vcs.init()
                >>> t=a.createtext()
                >>> t.x=[.5]
                >>> t.y=[.5]
                >>> t.string=['Hello World']
                >>> a.gettextbox(t)
                [[...]]

        :param textobject: A VCS text object
        :type textobject: vcs.textcombined.Tc

        :returns: 2 list of floats containing the coordinates of the text object's box. One for xs one for ys
        coordinates are appropriate within the same viewport and worldcoordinate as the input textobject
        :rtype: `list`_
        """
        if not vcs.istext(textobject):
            raise vcsError('You must pass a text object')

        # for rotation we need to normalize coordinates
        text2 = vcs.createtext(Tt_source=textobject.Tt_name, To_source=textobject.To_name)
        xs = numpy.array(textobject.x) / (text2.worldcoordinate[1] - text2.worldcoordinate[0])
        ys = numpy.array(textobject.y) / (text2.worldcoordinate[3] - text2.worldcoordinate[2])
        text2.x = xs.tolist()
        text2.y = ys.tolist()

        text2.worldcoordinate = [0, 1, 0, 1]

        boundings = self.gettextextent(textobject)
        noangles = self.gettextextent(text2, 0.)
        out = []
        for bounding, noangle in zip(boundings, noangles):
            bxmid = (bounding[0] + bounding[1])/2.
            bymid = (bounding[2] + bounding[3]) / 2.

            xmid = (noangle[0] + noangle[1])/2.
            ymid = (noangle[2] + noangle[3])/2.

            slim = []
            # first corner
            slim.append(rotate(noangle[0], noangle[2], xmid, ymid, -textobject.angle))
            # second corner
            slim.append(rotate(noangle[1], noangle[2], xmid, ymid, -textobject.angle))
            # third corner
            slim.append(rotate(noangle[1], noangle[3], xmid, ymid, -textobject.angle))
            # fourth corner
            slim.append(rotate(noangle[0], noangle[3], xmid, ymid, -textobject.angle))
            # Ok now we need to translte in the middle of the bounding box
            xs = [p[0] for p in slim]
            ys = [p[1] for p in slim]
            outx = [bxmid + (x - xmid)*(textobject.worldcoordinate[1]-textobject.worldcoordinate[0]) for x in xs]
            outy = [bymid + (y - ymid)*(textobject.worldcoordinate[3]-textobject.worldcoordinate[2]) for y in ys]
            out.append([outx, outy])
        return out

    def match_color(self, color, colormap=None):  # noqa
        return vcs.match_color(color, colormap)
    match_color.__doc__ = vcs.utils.match_color.__doc__

    def drawtextcombined(self, Tt_name=None, To_name=None, string=None,
                         font=1, spacing=2, expansion=100, color=241,
                         height=14, angle=0, path='right', halign='left',
                         valign='half',
                         priority=1, viewport=[0.0, 1.0, 0.0, 1.0],
                         worldcoordinate=[0.0, 1.0, 0.0, 1.0],
                         x=None, y=None, bg=0):
        """Draw a textcombined object on the VCS Canvas.

        :Example:

            .. doctest:: canvas_drawtextcombined

                >>> a=vcs.init()
                >>> drawtc=a.drawtextcombined # alias long function name
                >>> a.show('texttable') # Show all the existing texttable objects
                *******************Texttable Names List**********************
                ...
                *******************End Texttable Names List**********************
                >>> if "draw_tt" in vcs.listelements("texttable"): vcs.reset()
                >>> if "draw_tto" in vcs.listelements("textorientation"): vcs.reset()
                >>> vcs.createtextcombined('draw_tt','qa', 'draw_tto', '7left')
                <vcs.textcombined.Tc object at 0x...>
                >>> msg=["Hello", "drawtextcombined!"]
                >>> tc=drawtc(Tt_name='draw_tt',To_name='draw_tto',string=msg)

        :param Tt_name: String name of a texttable object
        :type Tt_name: `str`_

        :param To_name: String name of a textorientation object
        :type To_name: `str`_

        :param string: String to put onto the new textcombined
        :type string: `str`_

        %s
        %s
        %s
        %s
        %s

        :returns: A texttable object
        :rtype: vcs.texttable.Tt
        """
        if (Tt_name is None) or (not isinstance(Tt_name, str)):
            raise vcsError('Must provide string name for the texttable.')
        else:
            lot = self.listelements('texttable')
            if Tt_name not in lot:
                self.createtexttable(Tt_name)
            loo = self.listelements('textorientation')
            if To_name not in loo:
                self.createtextorientation(To_name)
            t = self.gettextcombined(Tt_name, To_name)

        # Set the Text Table (Tt) members
        t.string = string

        # Set the Text Table (Tt) members
        t.font = font
        t.spacing = spacing
        t.expansion = expansion
        t.color = color
        t.priority = priority
        t.viewport = viewport
        t.worldcoordinate = worldcoordinate
        t.x = x
        t.y = y

        # Set the Text Orientation (To) members
        t.height = height
        t.angle = angle
        t.path = path
        t.halign = halign
        t.valign = valign

        self.text(t, bg=bg)

        return t
    #
    # Set alias for the secondary drawtextcombined.
    drawtext = drawtextcombined
    drawtextcombined.__doc__ = drawtextcombined.__doc__ % (xmldocs.color, xmldocs.viewport, xmldocs.worldcoordinate,
                                                           xmldocs.x_y_coords, xmldocs.bg)

    _plot_keywords_ = ['variable', 'grid', 'xaxis', 'xarray',  'xrev', 'yaxis', 'yarray', 'yrev', 'continents',
                       'xbounds', 'ybounds', 'zaxis', 'zarray', 'taxis', 'tarray', 'waxis', 'warray', 'bg', 'ratio',
                       'donotstoredisplay', 'render', 'continents_line', "display_name"]

    _deprecated_plot_keywords_ = ["time", "units", "file_comment", "xname", "yname", "zname", "tname", "wname",
                                  "xunits", "yunits", "zunits", "tunits", "wunits", "comment1", "comment2", "comment3",
                                  "comment4", "long_name"]
    # def replot(self):
    #    """ Clears and plots with last used plot arguments
    #    """
    #    self.clear()
    #    self.plot(*self.__last_plot_actual_args, **self.__last_plot_keyargs)

    def plot(self, *actual_args, **keyargs):
        """Plot an array(s) of data given a template and graphics method.

        The VCS template is used to define where the data and variable
        attributes will  be displayed on the VCS Canvas.

        The VCS graphics method is used to define how the array(s) will be
        shown on the VCS Canvas.

        .. describe:: Plot Usage:

            .. doctest:: canvas_plot_usage

                >>> import numpy
                >>> a=vcs.init()
                >>> a.show('template') # list vcs template types
                *******************Template Names List**********************
                ...
                *******************End Template Names List**********************
                >>> a.show('boxfill') # one of many graphics method types
                *******************Boxfill Names List**********************
                ...
                *******************End Boxfill Names List**********************
                >>> array1 = numpy.array([range(10) for _ in range(10)]) # data
                >>> a.plot(variable=array1)
                <vcs.displayplot.Dp ...>
                >>> a.plot(array1,'ASD',gm='boxfill')  # boxfill, ASD template
                <vcs.displayplot.Dp ...>

        .. describe:: Plot attribute keywords:

            .. note:: **Attribute Precedence**

                Specific attributes take precedence over general attributes.
                In particular, specific attributes override variable object
                attributes, dimension attributes and arrays override axis
                objects, which override grid objects, which override variable
                objects.

                For example, if both 'file_comment' and 'variable' keywords are
                specified, the value of 'file_comment' is used instead of the
                file comment in the parent of variable. Similarly, if both
                'xaxis' and 'grid' keywords are specified, the value of 'xaxis'
                takes precedence over the x-axis of grid.

            *  ratio [default is None]

                * None: let the self.ratio attribute decide
                *  0, 'off': overwrite self.ratio and do nothing about the ratio
                * 'auto': computes an automatic ratio
                * '3', 3: y dim will be 3 times bigger than x dim (restricted
                    to original template.data area)
                * Adding a 't' at the end of the ratio, makes the tickmarks and
                    boxes move along.

            * Dimension attribute keys (dimension length=n):

                * x or y Dimension values

                    .. code-block:: python

                        [x|y|z|t|w]array = NumPy array of length n
                        [x|y|z|t|w]array = NumPy array of length n

                * x or y Dimension boundaries

                    .. code-block:: python

                        [x|y]bounds = NumPy array of shape (n,2)

            * CDMS object:

                * x or y Axis

                    .. code-block:: python

                        [x|y|z|t|w]axis = CDMS axis object

                * Grid object (e.g. grid=var.getGrid())

                    .. code-block:: python

                        grid = CDMS grid object

                * Variable object

                    .. code-block:: python

                        variable = CDMS variable object

            * Other:

                * Reverse the direction of the x or y axis:

                    .. code-block:: python

                        [x|y]rev = 0|1

                    .. note::

                        For example, xrev = 1 would reverse the
                        direction of the x-axis

                * Continental outlines:

                    .. code-block:: python

                        continents = 0,1,2,3,4,5,6,7,8,9,10,11
                        # VCS line object to define continent appearance
                        continents_line = vcs.getline("default")

                    .. note::

                        If continents >=1, plot continental outlines.
                        By default: plot of xaxis is longitude, yaxis is latitude
                        -OR- xname is 'longitude' and yname is 'latitude'

                    * List of continents-type values (integers from 0-11)

                        * 0 signifies "No Continents"
                        * 1 signifies "Fine Continents"
                        * 2 signifies "Coarse Continents"
                        * 3 signifies "United States"
                        * 4 signifies "Political Borders"
                        * 5 signifies "Rivers"

                    .. note::

                        Values 6 through 11 signify the line type defined by
                        the files data_continent_other7 through data_continent_other12.

                * To set whether the displayplot object generated by this plot is stored

                    .. code-block:: python

                        donotstoredisplay = True|False

                * Whether to actually render the plot or not (useful for doing a bunch of plots in a row)

                    .. code-block:: python

                        render = True|False

                * VCS Display plot name (used to prevent duplicate display plots)

                    .. code-block:: python

                        display_name = "__display_123"

                * Ratio of height/width for the plot; autot and auto will choose a "good" ratio for you.

                    .. code-block:: python

                        ratio = 1.5|"autot"|"auto"

                * Plot the actual grid or the dual grid

                    .. code-block:: python

                        plot_based_dual_grid = True | False

                    .. note::

                        This is based on what is needed by the plot: isofill, isoline, vector need
                        point attributes, boxfill and meshfill need cell attributes
                        the default is True (if the parameter is not specified).

                * Graphics Output in Background Mode:

                    .. code-block:: python

                        # if 1, create images in the background (not on canvas)
                        bg = 0|1

        :Example:

            .. doctest:: canvas_plot

                >>> a=vcs.init()
                >>> import cdms2 # Need cdms2 to create a slab
                >>> f = cdms2.open(vcs.sample_data+'/clt.nc') # open data file
                >>> slab1 = f('u') # use the data file to create a cdms2 slab
                >>> slab2 = f('v') # need 2 slabs, so get another
                >>> a.plot(slab1) # default settings for template and boxfill
                <vcs.displayplot.Dp ...>
                >>> a.plot(slab1,'polar','isofill','polar') # specify template and graphics method
                <vcs.displayplot.Dp ...>
                >>> t=a.gettemplate('polar') # get the polar template
                >>> vec=a.getvector() # get default vector
                >>> a.plot(slab1, slab2, t, vec) # plot data as vector using polar template
                <vcs.displayplot.Dp ...>
                >>> a.clear() # clear the VCS Canvas of all plots
                >>> box=a.getboxfill() # get default boxfill graphics method
                >>> a.plot(box,t,slab2) # plot data with boxfill and polar
                <vcs.displayplot.Dp ...>

        %s
        %s
        %s
        %s
        %s
        %s

        :returns: A VCS display plot object
        :rtype: vcs.displayplot.Dp
        """
        self.__last_plot_actual_args = actual_args
        self.__last_plot_keyargs = keyargs
        passed_var = keyargs.get("variable", None)
        arglist = _determine_arg_list(None, actual_args)
        if passed_var is not None:
            arglist[0] = cdms2.asVariable(passed_var)

        try:
            pfile = actual_args[0].parent
            keyargs['cdmsfile'] = pfile.uri if hasattr(
                pfile,
                'uri') else pfile.id
        except Exception:
            pass

        if "continents_line" in keyargs:
            # Stash the current line type
            old_line = self.getcontinentsline()
            self.setcontinentsline(keyargs["continents_line"])

        # Plot the data
        a = self.__plot(arglist, keyargs)

        if "continents_line" in keyargs:
            # Restore the canvas line type
            self.setcontinentsline(old_line)
        return a
    plot.__doc__ = plot.__doc__ % (plot_2_1D_options,
                                   plot_keywords_doc,
                                   graphics_method_core,
                                   axesconvert,
                                   plot_2_1D_input,
                                   plot_output)

    def plot_filledcontinents(
            self, slab, template_name, g_type, g_name, bg, ratio):
        cf = cdutil.continent_fill.Gcf()
        if g_type.lower() == 'boxfill':
            g = self.getboxfill(g_name)
        lons = slab.getLongitude()
        lats = slab.getLatitude()

        if lons is None or lats is None:
            return
        if g.datawc_x1 > 9.9E19:
            cf.datawc_x1 = lons[0]
        else:
            cf.datawc_x1 = g.datawc_x1
        if g.datawc_x2 > 9.9E19:
            cf.datawc_x2 = lons[-1]
        else:
            cf.datawc_x2 = g.datawc_x2
        if g.datawc_y1 > 9.9E19:
            cf.datawc_y1 = lats[0]
        else:
            cf.datawc_y1 = g.datawc_y1
        if g.datawc_y2 > 9.9E19:
            cf.datawc_y2 = lats[-1]
        else:
            cf.datawc_y2 = g.datawc_y2
        try:
            self.gettemplate(template_name)
            cf.plot(x=self, template=template_name, ratio=ratio)
        except Exception as err:
            print(err)

    def __new_elts(self, original, new):
        for e in list(vcs.elements.keys()):
            for k in list(vcs.elements[e].keys()):
                if k not in original[e]:
                    new[e].append(k)
        return new

    def __plot(self, arglist, keyargs):

            # This routine has five arguments in arglist from _determine_arg_list
            # It adds one for bg and passes those on to Canvas.plot as its sixth
            # arguments.

            # First of all let's remember which elets we have before comin in here
            # so that anything added (temp objects) can be removed at clear
            # time
        original_elts = {}
        new_elts = {}
        for k in list(vcs.elements.keys()):
            original_elts[k] = list(vcs.elements[k].keys())
            new_elts[k] = []
        # First of all try some cleanup
        assert len(arglist) == 6
        xtrakw = arglist.pop(5)
        for k in list(xtrakw.keys()):
            if k in list(keyargs.keys()):
                raise vcsError('Multiple Definition for ' + str(k))
            else:
                keyargs[k] = xtrakw[k]
        assert arglist[0] is None or cdms2.isVariable(arglist[0])
        assert arglist[1] is None or cdms2.isVariable(arglist[1])
        assert isinstance(arglist[2], str)
        if hasVCSAddons and not isinstance(arglist[3], vcsaddons.core.VCSaddon):
            assert isinstance(arglist[3], str)
        assert isinstance(arglist[4], str)

        if self.animate.is_playing():
            self.animate.stop()
            while self.animate.is_playing():
                pass
        # reset animation
        self.animate.create_flg = 0

        # Store the origin template. The template used to plot may be changed below by the
        # _create_random_template function, which copies templates for
        # modifications.
        template_origin = arglist[2]
        tmptmpl = self.gettemplate(arglist[2])
        tmptmpl.data.ratio = -999

        copy_mthd = None
        copy_tmpl = None
        if arglist[2] in ['default', 'default_dud']:
            if arglist[3] == 'taylordiagram':
                arglist[2] = "deftaylor"
                # copy_tmpl=self.createtemplate(source='deftaylor')
            # else:
            #    copy_tmpl=self.createtemplate(source=arglist[2])
        check_mthd = vcs.getgraphicsmethod(arglist[3], arglist[4])
        check_tmpl = vcs.gettemplate(arglist[2])
        # By defalut do the ratio thing for lat/lon and linear projection
        # but it can be overwritten by keyword
        doratio = str(keyargs.get('ratio', self.ratio)).strip().lower()
        if doratio[-1] == 't' and doratio[0] == '0':
            if float(doratio[:-1]) == 0.:
                doratio = '0'

        # Check for curvilinear grids, and wrap options !
        if arglist[0] is not None:
            inGrid = arglist[0].getGrid()
        else:
            inGrid = None
        if arglist[0] is not None and arglist[
                1] is None and arglist[3] == "meshfill":
            if isinstance(
                    inGrid, (cdms2.gengrid.AbstractGenericGrid, cdms2.hgrid.AbstractCurveGrid)):
                g = self.getmeshfill(arglist[4])
                if 'wrap' not in keyargs and g.wrap == [0., 0.]:
                    keyargs['wrap'] = [0., 360.]
            else:
                if arglist[0].ndim < 2:
                    arglist[3] = 'yxvsx'
                    arglist[4] = 'default'
                else:
                    xs = arglist[0].getAxis(-1)
                    ys = arglist[0].getAxis(-2)
                    if xs.isLongitude() and ys.isLatitude() and isinstance(
                            inGrid, cdms2.grid.TransientRectGrid):
                        arglist[1] = MV2.array(inGrid.getMesh())
                        if 'wrap' not in keyargs:
                            keyargs['wrap'] = [0., 360.]
                    elif ys.isLongitude() and xs.isLatitude() and isinstance(inGrid, cdms2.grid.TransientRectGrid):
                        arglist[1] = MV2.array(inGrid.getMesh())
                        if "wrap" not in keyargs:
                            keyargs['wrap'] = [360., 0.]
                    else:
                        arglist[3] = 'boxfill'
                        copy_mthd = vcs.creategraphicsmethod(
                            'boxfill',
                            'default')
                        check_mthd = copy_mthd
                        m = self.getmeshfill(arglist[4])
                        md = self.getmeshfill()
                        if md.levels != m.levels:
                            copy_mthd.boxfill_type = 'custom'
                            copy_mthd.levels = m.levels
                            copy_mthd.fillareacolors = m.fillareacolors
                        for att in ['projection',
                                    'xticlabels1',
                                    'xticlabels2',
                                    'xmtics1',
                                    'xmtics2',
                                    'yticlabels1',
                                    'yticlabels2',
                                    'ymtics1',
                                    'ymtics2',
                                    'datawc_x1',
                                    'datawc_x2',
                                    'datawc_y1',
                                    'datawc_y2',
                                    'xaxisconvert',
                                    'yaxisconvert',
                                    'legend',
                                    'ext_1',
                                    'ext_2',
                                    'missing']:
                            setattr(copy_mthd, att, getattr(m, att))
        elif arglist[0] is not None \
                and arglist[0].rank() < 2 \
                and arglist[3] in ['boxfill', 'default'] \
                and not isinstance(inGrid, cdms2.gengrid.AbstractGenericGrid):
            arglist[3] = '1d'
            try:
                tmp = self.getyxvsx(arglist[4])
                # tmp.list()
            except Exception:
                arglist[4] = 'default'
        elif inGrid is not None and arglist[0] is not None and\
                isinstance(arglist[0], cdms2.avariable.AbstractVariable) and\
                not isinstance(inGrid, cdms2.grid.AbstractRectGrid) and\
                arglist[3] in ["boxfill", "default"] and arglist[4] == "default":
            arglist[3] = "meshfill"

# arglist[4]=copy_mthd.name
        # Ok let's check for meshfill needed
        if inGrid is not None and arglist[0] is not None and\
                isinstance(arglist[0], cdms2.avariable.AbstractVariable) and\
                not isinstance(arglist[0].getGrid(), cdms2.grid.AbstractRectGrid) and\
                arglist[3] not in ["meshfill", ]:
            raise RuntimeError("You are attempting to plot unstructured grid" +
                               "with a method that is not meshfill")
        # preprocessing for extra keyword (at-plotting-time options)
        cmds = {}
        # First of all a little preprocessing for legend !
        if 'legend' in list(keyargs.keys()) and arglist[3] == 'boxfill':
            # we now have a possible problem since it can be legend for the
            # graphic method or the template!
            k = keyargs['legend']
            isboxfilllegend = 0
            if isinstance(k, type({})):
                #                print k.keys()
                # ok it's a dictionary if the key type is string then it's for
                # template, else it's for boxfill
                if not isinstance(list(k.keys())[0], type('')):
                    # not a string, therefore it's boxfill !
                    isboxfilllegend = 1
            elif type(k) in [type([]), type(())]:
                # ok it's a list therefore if the length is not 4 we have a
                # boxfill legend
                if len(k) != 4 and len(k) != 5:
                    isboxfilllegend = 1
                elif len(k) == 5:
                    if not type(k[4]) in [type({}), type(0), type(0.)]:
                        raise vcsError(
                            "Error, at-plotting-time argument 'legend' is ambiguous in this context\n"
                            "Cannot determine if it is template or boxfill keyword,\n tips to solve that:\n"
                            "\tif you aim at boxfill keyword, pass legend as a dictionary, \n"
                            "\tif your aim at template, add {'priority':1} at the end of the list\n"
                            "Currently legend is passed as:" +
                            repr(k))
                    elif not isinstance(k[4], type({})):
                        isboxfilllegend = 1
                else:
                    # ok it's length 4, now the only hope left is that not all
                    # values are between 0 and 1
                    for i in range(4):
                        if k[i] > 1. or k[i] < 0.:
                            isboxfilllegend = 1
                    if isboxfilllegend == 0:
                        raise vcsError(
                            "Error, at-plotting-time argument 'legend' is ambiguous"
                            "in this context\nCannot determine if it is template or boxfill keyword,\n "
                            "tips to solve that:\n\tif you aim at boxfill keyword, pass legend as a dictionary, \n"
                            "\tif your aim at template, add {'priority':1} at the end of the list\n"
                            "Currently legend is passed as:" +
                            repr(k))

            # ok it is for the boxfill let's do it
            if isboxfilllegend:
                if copy_mthd is None:
                    try:
                        copy_mthd = vcs.creategraphicsmethod(
                            arglist[3],
                            arglist[4])
                    except Exception:
                        pass
                copy_mthd.legend = k
                del(keyargs['legend'])
                check_mthd = copy_mthd

        # There is no way of knowing if the template has been called prior to this plot command.
        # So it is done here to make sure that the template coordinates are normalized. If already
        # normalized, then no change will to the template.
        try:
            self.gettemplate(template_origin)
        except Exception:
            pass

        # Creates dictionary/list to remember what we changed
        slab_changed_attributes = {}
        axes_changed = {}
        axes_changed2 = {}

        # loops through possible keywords for graphic method
        for p in list(keyargs.keys()):
            if p in [
                'projection',
                'xticlabels1',
                'xticlabels2',
                'xmtics1',
                'xmtics2',
                'yticlabels1',
                'yticlabels2',
                'ymtics1',
                'ymtics2',
                'datawc_x1',
                'datawc_y1',
                'datawc_x2',
                'datawc_y2',
                'xaxisconvert',
                'yaxisconvert',
                'label',
                'labelskipdistance',
                'line',
                'linewidth',
                'linecolors',
                'text',
                'textcolors',
                'level',
                'level_1',
                'level_2',
                'ext_1',
                'ext_2',
                'missing',
                'color_1',
                'color_2',
                'fillareastyle',
                'fillareacolors',
                'fillareaindices',
                'levels',
                'mesh',
                'wrap',
                'marker',
                'markercolor',
                'markersize',
                'linecolor',
                'detail',
                'max',
                'quadrans',
                'skillValues',
                'skillColor',
                'skillCoefficient',
                'referencevalue',
                'arrowlength',
                'arrowangle',
                'arrowbase',
                'scale',
                'alignement',
                'type',
                'reference',
                # Now the "special" keywords
                'worldcoordinate',
            ]:
                if p not in ['worldcoordinate', ]:  # not a special keywords
                    if copy_mthd is None:
                        try:
                            copy_mthd = vcs.creategraphicsmethod(
                                arglist[3],
                                arglist[4])
                        except Exception:
                            pass
                        check_mthd = copy_mthd
                    setattr(copy_mthd, p, keyargs[p])
                elif p == 'worldcoordinate':
                    if copy_mthd is None:
                        try:
                            copy_mthd = vcs.creategraphicsmethod(
                                arglist[3],
                                arglist[4])
                        except Exception:
                            pass
                        check_mthd = copy_mthd
                    setattr(copy_mthd, 'datawc_x1', keyargs[p][0])
                    setattr(copy_mthd, 'datawc_x2', keyargs[p][1])
                    setattr(copy_mthd, 'datawc_y1', keyargs[p][2])
                    setattr(copy_mthd, 'datawc_y2', keyargs[p][3])
                del(keyargs[p])
            # Now template settings keywords
            elif p in [
                'viewport',
            ]:
                if copy_tmpl is None:
                    copy_tmpl = vcs.createtemplate(source=arglist[2])
                    check_tmpl = copy_tmpl
                copy_tmpl.reset(
                    'x',
                    keyargs[p][0],
                    keyargs[p][1],
                    copy_tmpl.data.x1,
                    copy_tmpl.data.x2)
                copy_tmpl.reset(
                    'y',
                    keyargs[p][2],
                    keyargs[p][3],
                    copy_tmpl.data.y1,
                    copy_tmpl.data.y2)
                del(keyargs[p])
            # Now template and x/y related stuff (1 dir only)
            elif p[1:] in [
                'label1',
                'label2',
            ]:
                if copy_tmpl is None:
                    copy_tmpl = vcs.createtemplate(source=arglist[2])
                    check_tmpl = copy_tmpl
                k = keyargs[p]
                # not a list means only priority set
                if not isinstance(k, type([])):
                    if not isinstance(k, type({})):
                        setattr(getattr(copy_tmpl, p), 'priority', k)
                    elif isinstance(k, type({})):
                        for kk in list(k.keys()):
                            setattr(getattr(copy_tmpl, p), kk, k[kk])
                else:
                    if p[0] == 'x':
                        setattr(getattr(copy_tmpl, p), 'y', k[0])
                    else:
                        setattr(getattr(copy_tmpl, p), 'x', k[0])
                    if isinstance(k[-1], type({})):
                        for kk in list(k[-1].keys()):
                            setattr(getattr(copy_tmpl, p), kk, k[-1][kk])

                del(keyargs[p])
            # Now template and x1 and x2/y1 and y2 related stuff (1 dir only)
            elif p[1:] in [
                'mintic1',
                'mintic2',
                'tic1',
                'tic2',
            ]:
                if copy_tmpl is None:
                    copy_tmpl = vcs.createtemplate(source=arglist[2])
                    check_tmpl = copy_tmpl

                k = keyargs[p]
                # not a list means only priority set
                if not isinstance(k, type([])):
                    if not isinstance(k, type({})):
                        setattr(getattr(copy_tmpl, p), 'priority', k)
                    elif isinstance(k, type({})):
                        for kk in list(k.keys()):
                            setattr(getattr(copy_tmpl, p), kk, k[kk])
                else:
                    if p[0] == 'x':
                        setattr(getattr(copy_tmpl, p), 'y1', k[0])
                        setattr(getattr(copy_tmpl, p), 'y2', k[1])
                    else:
                        setattr(getattr(copy_tmpl, p), 'x1', k[0])
                        setattr(getattr(copy_tmpl, p), 'x2', k[1])
                    if isinstance(k[-1], type({})):
                        for kk in list(k[-1].keys()):
                            setattr(getattr(copy_tmpl, p), kk, k[-1][kk])

                del(keyargs[p])
            # Now template with x1, x2, x3, x4, x5
            elif p in [
                'box1', 'box2', 'box3', 'box4',
                'line1', 'line2', 'line3', 'line4',
                'data', 'legend',
            ]:
                if copy_tmpl is None:
                    copy_tmpl = vcs.createtemplate(source=arglist[2])
                    check_tmpl = copy_tmpl
                k = keyargs[p]
                # not a list means only priority set
                if not isinstance(k, type([])):
                    if not isinstance(k, type({})):
                        setattr(getattr(copy_tmpl, p), 'priority', k)
                    elif isinstance(k, type({})):
                        for kk in list(k.keys()):
                            setattr(getattr(copy_tmpl, p), kk, k[kk])
                else:
                    setattr(getattr(copy_tmpl, p), 'x1', k[0])
                    setattr(getattr(copy_tmpl, p), 'x2', k[1])
                    setattr(getattr(copy_tmpl, p), 'y1', k[2])
                    setattr(getattr(copy_tmpl, p), 'y2', k[3])
                    if isinstance(k[-1], type({})):
                        for kk in list(k[-1].keys()):
                            setattr(getattr(copy_tmpl, p), kk, k[-1][kk])

                del(keyargs[p])
            # Now MV2 related keywords
            # Charles note: It's here that we need to remember what changed so
            # i can unset it later
            elif p in [
                'title',
                'comment1',
                'comment2',
                'comment3',
                'comment4',
                'source',
                'crdate',
                'crtime',
                'dataname',
                'file',
                'function',
                'transformation',
                'units',
                'id',
            ]:
                k = keyargs[p]
                if copy_tmpl is None:
                    copy_tmpl = vcs.createtemplate(source=arglist[2])
                    check_tmpl = copy_tmpl
                if getattr(getattr(check_tmpl, p), 'priority') == 0:
                    setattr(getattr(copy_tmpl, p), 'priority', 1)
                if not isinstance(
                        k, list):  # not a list means only priority set
                    if isinstance(k, dict):
                        for kk in list(k.keys()):
                            setattr(getattr(copy_tmpl, p), kk, k[kk])
                    elif isinstance(k, int):
                        setattr(getattr(copy_tmpl, p), 'priority', k)
                    elif isinstance(k, str):
                        slab_changed_attributes[p] = k
                else:
                    # if hasattr(arglist[0],p):
                    # slab_changed_attributes[p]=getattr(arglist[0],p)
                    # else:
                    # slab_created_attributes.append(p)
                    # setattr(arglist[0],p,k[0])
                    slab_changed_attributes[p] = k[0]
                    setattr(getattr(copy_tmpl, p), 'x', k[1])
                    setattr(getattr(copy_tmpl, p), 'y', k[2])
                    if isinstance(k[-1], type({})):
                        for kk in list(k[-1].keys()):
                            setattr(getattr(copy_tmpl, p), kk, k[-1][kk])

                del(keyargs[p])
            # Now Axis related keywords
            elif p[1:] in [
                'name',
                'value',
                'units',
            ]:
                if p[0] == 'x':
                    ax = arglist[0].getAxis(-1)
                    if ax is not None:
                        ax = ax.clone()
                    if 'xaxis' in keyargs:
                        ax = keyargs['xaxis'].clone()
                        keyargs['xaxis'] = ax
                    g = arglist[0].getGrid()
                    if isinstance(g, (cdms2.gengrid.AbstractGenericGrid, cdms2.hgrid.AbstractCurveGrid)) or arglist[
                            3].lower() == 'meshfill':
                        ax = None
                        del(g)
                elif p[0] == 'y':
                    ax = arglist[0].getAxis(-2)
                    if ax is not None:
                        ax = ax.clone()
                    if 'yaxis' in keyargs:
                        ax = keyargs['yaxis'].clone()
                        keyargs['yaxis'] = ax
                    g = arglist[0].getGrid()
                    if isinstance(g, (cdms2.gengrid.AbstractGenericGrid, cdms2.hgrid.AbstractCurveGrid)) or arglist[
                            3].lower() == 'meshfill':
                        ax = None
                        del(g)
                elif p[0] == 'z':
                    ax = arglist[0].getLevel()
                    if ax is not None:
                        ax = ax.clone()
                elif p[0] == 't':
                    ax = arglist[0].getTime()
                    if ax is not None:
                        ax = ax.clone()
                if ax is not None:
                    ids = arglist[0].getAxisIds()
                    for i in range(len(ids)):
                        if ax.id == ids[i]:
                            if i not in axes_changed:
                                axes_changed[i] = ax
                    if arglist[1] is not None:
                        ids2 = arglist[1].getAxisIds()
                        for i in range(len(ids2)):
                            if ax.id == ids2[i]:
                                if i not in axes_changed2:
                                    axes_changed2[i] = ax
                if copy_tmpl is None:
                    check_tmpl = copy_tmpl = vcs.createtemplate(
                        source=arglist[2])
                k = keyargs[p]
                if getattr(getattr(copy_tmpl, p), 'priority') == 0:
                    setattr(getattr(copy_tmpl, p), 'priority', 1)
                # not a list means only priority set
                if not isinstance(k, type([])):
                    if isinstance(k, type({})):
                        for kk in list(k.keys()):
                            setattr(getattr(copy_tmpl, p), kk, k[kk])
                    elif isinstance(k, type(0)):
                        setattr(getattr(copy_tmpl, p), 'priority', k)
                    elif isinstance(k, str):
                        if p[1:] != 'name':
                            setattr(ax, p[1:], k)
                        else:
                            try:
                                setattr(ax, 'id', k)
                            except Exception:
                                # print err
                                pass
                    elif k is None:
                        if p[1:] != 'name':
                            setattr(ax, p[1:], '')
                        else:
                            setattr(ax, 'id', '')

                else:
                    if p[1:] != 'name':
                        setattr(ax, p[1:], k[0])
                    else:
                        setattr(ax, 'id', k)
                    setattr(getattr(copy_tmpl, p), 'x', k[1])
                    setattr(getattr(copy_tmpl, p), 'y', k[2])
                    if isinstance(k[-1], type({})):
                        for kk in list(k[-1].keys()):
                            setattr(getattr(copy_tmpl, p), kk, k[-1][kk])

                del(keyargs[p])
            # Finally take care of commands
            elif p in [
                'pdf', 'ps', 'postscript', 'gif', 'ras',
            ]:
                cmds[p] = keyargs[p]
                del(keyargs[p])

        if (hasattr(check_mthd, 'datawc_x1') and hasattr(check_mthd, 'datawc_x2')) \
                and arglist[0].getAxis(-1).isTime() \
                and check_mthd.xticlabels1 == '*' \
                and check_mthd.xticlabels2 == '*' \
                and check_mthd.xmtics1 in ['*', ''] \
                and check_mthd.xmtics2 in ['*', ''] \
                and not (check_mthd.g_name in ['G1d'] and
                         (check_mthd.flip is True or arglist[1] is not None) and
                         arglist[0].ndim == 1):  # used to be GXy GX
            ax = arglist[0].getAxis(-1).clone()
            ids = arglist[0].getAxisIds()
            for i in range(len(ids)):
                if ax.id == ids[i]:
                    if i not in axes_changed:
                        ax = ax.clone()
                        axes_changed[i] = ax
                    break
            if arglist[1] is not None:
                ids2 = arglist[1].getAxisIds()
                for i in range(len(ids2)):
                    if ax.id == ids2[i]:
                        if i not in axes_changed2:
                            axes_changed2[i] = ax
            try:
                ax.toRelativeTime(
                    check_mthd.datawc_timeunits,
                    check_mthd.datawc_calendar)
                convertedok = True
            except Exception:
                convertedok = False
            # and check_mthd.g_name not in ["G1d",]: #used to be Gsp
            if (check_mthd.xticlabels1 ==
                    '*' or check_mthd.xticlabels2 == '*') and convertedok:
                convert_datawc = False
                for cax in list(axes_changed.keys()):
                    if axes_changed[cax] == ax:
                        convert_datawc = True
                        break
                if convert_datawc:
                    oax = arglist[0].getAxis(cax).clone()
                    t = type(check_mthd.datawc_x1)
                    if t not in [type(cdtime.reltime(0, 'months since 1900')), type(
                            cdtime.comptime(1900))]:
                        if copy_mthd is None:
                            try:
                                copy_mthd = vcs.creategraphicsmethod(
                                    arglist[3],
                                    arglist[4])
                            except Exception:
                                pass
                            check_mthd = copy_mthd
                        if check_mthd.datawc_x1 > 9.E19:
                            copy_mthd.datawc_x1 = cdtime.reltime(
                                oax[0],
                                oax.units).tocomp(
                                oax.getCalendar()).torel(
                                copy_mthd.datawc_timeunits,
                                copy_mthd.datawc_calendar)
                        else:
                            copy_mthd.datawc_x1 = cdtime.reltime(
                                copy_mthd.datawc_x1,
                                oax.units).tocomp(
                                oax.getCalendar()).torel(
                                copy_mthd.datawc_timeunits,
                                copy_mthd.datawc_calendar)
                        if copy_mthd.datawc_x2 > 9.E19:
                            copy_mthd.datawc_x2 = cdtime.reltime(oax[-1], oax.units).tocomp(
                                oax.getCalendar()).torel(copy_mthd.datawc_timeunits, copy_mthd.datawc_calendar)
                        else:
                            copy_mthd.datawc_x2 = cdtime.reltime(
                                copy_mthd.datawc_x2,
                                oax.units).tocomp(
                                oax.getCalendar()).torel(
                                copy_mthd.datawc_timeunits,
                                copy_mthd.datawc_calendar)
                if copy_mthd.xticlabels1 == '*':
                    if copy_mthd is None:
                        try:
                            copy_mthd = vcs.creategraphicsmethod(
                                arglist[3],
                                arglist[4])
                        except Exception:
                            pass
                        check_mthd = copy_mthd
                    copy_mthd.xticlabels1 = vcs.generate_time_labels(
                        copy_mthd.datawc_x1,
                        copy_mthd.datawc_x2,
                        copy_mthd.datawc_timeunits,
                        copy_mthd.datawc_calendar)
                if copy_mthd.xticlabels2 == '*':
                    if copy_mthd is None:
                        try:
                            copy_mthd = vcs.creategraphicsmethod(
                                arglist[3],
                                arglist[4])
                        except Exception:
                            pass
                        check_mthd = copy_mthd
                    copy_mthd.xticlabels2 = vcs.generate_time_labels(
                        copy_mthd.datawc_x1,
                        copy_mthd.datawc_x2,
                        copy_mthd.datawc_timeunits,
                        copy_mthd.datawc_calendar)
        elif not (getattr(check_mthd, 'g_name', '') == 'Gfm' and
                  isinstance(arglist[0].getGrid(), (cdms2.gengrid.AbstractGenericGrid, cdms2.hgrid.AbstractCurveGrid))):
            try:
                if arglist[0].getAxis(-1).isTime():  # used to GXy
                    if check_mthd.xticlabels1 == '*' and check_mthd.xticlabels2 == '*' and\
                            not (check_mthd.g_name == 'G1d' and check_mthd.flip) and\
                            check_mthd.g_name not in ['G1d']:  # used to be GSp
                        if copy_mthd is None:
                            try:
                                copy_mthd = vcs.creategraphicsmethod(
                                    arglist[3],
                                    arglist[4])
                            except Exception:
                                pass
                            check_mthd = copy_mthd
                        t = arglist[0].getAxis(-1).clone()
                        timeunits = t.units
                        calendar = t.getCalendar()
                        t0 = cdtime.reltime(t[0], timeunits)
                        t1 = cdtime.reltime(t[-1], timeunits)
                        copy_mthd.xticlabels1 = vcs.generate_time_labels(
                            t0,
                            t1,
                            timeunits,
                            calendar)
            except Exception:
                pass

        if (hasattr(check_mthd, 'datawc_y1') and hasattr(check_mthd, 'datawc_y2'))\
                and check_mthd.yticlabels1 == '*' \
                and check_mthd.yticlabels2 == '*' \
                and check_mthd.ymtics1 in ['*', ''] \
                and check_mthd.ymtics2 in ['*', ''] \
                and arglist[0].getAxis(-2).isTime() \
                and (arglist[0].ndim > 1 or (check_mthd.g_name == 'G1d' and check_mthd.flip)) \
                and not (check_mthd.g_name == 'Gfm' and
                         isinstance(arglist[0].getGrid(),
                                    (cdms2.gengrid.AbstractGenericGrid, cdms2.hgrid.AbstractCurveGrid))):  # GXy
            ax = arglist[0].getAxis(-2).clone()
            # used to be  Sp
            if check_mthd.g_name == "G1d" and check_mthd.linewidth == 0:
                ax = arglist[1].getAxis(-2).clone()
                axes_changed2 = {}
            ids = arglist[0].getAxisIds()
            for i in range(len(ids)):
                if ax.id == ids[i]:
                    if i not in axes_changed:
                        ax = ax.clone()
                        axes_changed[i] = ax
                    break
            if arglist[1] is not None:
                ids2 = arglist[1].getAxisIds()
                for i in range(len(ids2)):
                    if ax.id == ids2[i]:
                        if i not in axes_changed2:
                            axes_changed2[i] = ax
                        break
            try:
                ax.toRelativeTime(
                    check_mthd.datawc_timeunits,
                    check_mthd.datawc_calendar)
                convertedok = True
            except Exception:
                convertedok = False
            if (check_mthd.yticlabels1 ==
                    '*' or check_mthd.yticlabels2 == '*') and convertedok:
                convert_datawc = False
                A = axes_changed
                # GSp
                if check_mthd.g_name == "G1d" and check_mthd.linewidth == 0:
                    A = axes_changed2
                for cax in list(A.keys()):
                    if A[cax] is ax:
                        convert_datawc = True
                        break
                if convert_datawc:
                    oax = arglist[0].getAxis(cax).clone()
                    if copy_mthd is None:
                        try:
                            copy_mthd = vcs.creategraphicsmethod(
                                arglist[3],
                                arglist[4])
                        except Exception:
                            pass
                        check_mthd = copy_mthd
                    if copy_mthd.datawc_y1 > 9.E19:
                        copy_mthd.datawc_y1 = cdtime.reltime(
                            oax[0],
                            oax.units).tocomp(
                            oax.getCalendar()).torel(
                            copy_mthd.datawc_timeunits,
                            copy_mthd.datawc_calendar)
                    else:
                        copy_mthd.datawc_y1 = cdtime.reltime(
                            copy_mthd.datawc_y1,
                            oax.units).tocomp(
                            oax.getCalendar()).torel(
                            copy_mthd.datawc_timeunits,
                            copy_mthd.datawc_calendar)
                    if copy_mthd.datawc_y2 > 9.E19:
                        copy_mthd.datawc_y2 = cdtime.reltime(oax[-1], oax.units).tocomp(
                            oax.getCalendar()).torel(copy_mthd.datawc_timeunits, copy_mthd.datawc_calendar)
                    else:
                        copy_mthd.datawc_y2 = cdtime.reltime(
                            copy_mthd.datawc_y2,
                            oax.units).tocomp(
                            oax.getCalendar()).torel(
                            copy_mthd.datawc_timeunits,
                            copy_mthd.datawc_calendar)
                if check_mthd.yticlabels1 == '*':
                    if copy_mthd is None:
                        try:
                            copy_mthd = vcs.creategraphicsmethod(
                                arglist[3],
                                arglist[4])
                        except Exception:
                            pass
                        check_mthd = copy_mthd
                    copy_mthd.yticlabels1 = vcs.generate_time_labels(
                        copy_mthd.datawc_y1,
                        copy_mthd.datawc_y2,
                        copy_mthd.datawc_timeunits,
                        copy_mthd.datawc_calendar)
                if check_mthd.yticlabels2 == '*':
                    if copy_mthd is None:
                        try:
                            copy_mthd = vcs.creategraphicsmethod(
                                arglist[3],
                                arglist[4])
                        except Exception:
                            pass
                        check_mthd = copy_mthd
                    copy_mthd.yticlabels2 = vcs.generate_time_labels(
                        copy_mthd.datawc_y1,
                        copy_mthd.datawc_y2,
                        copy_mthd.datawc_timeunits,
                        copy_mthd.datawc_calendar)
        elif not (getattr(check_mthd, 'g_name', '') == 'Gfm' and
                  isinstance(arglist[0].getGrid(),
                             (cdms2.gengrid.AbstractGenericGrid, cdms2.hgrid.AbstractCurveGrid))):
            try:
                # ['GYx','GXy','GXY','GSp']:
                if arglist[
                        0].getAxis(-2).isTime() and arglist[0].ndim > 1 and copy_mthd.g_name not in ["G1d", ]:
                    if check_mthd.yticlabels1 == '*' and check_mthd.yticlabels2 == '*':
                        if copy_mthd is None:
                            try:
                                copy_mthd = vcs.creategraphicsmethod(
                                    arglist[3],
                                    arglist[4])
                            except Exception:
                                pass
                            check_mthd = copy_mthd
                        t = arglist[0].getAxis(-2).clone()
                        timeunits = t.units
                        calendar = t.getCalendar()
                        t0 = cdtime.reltime(t[0], timeunits)
                        t1 = cdtime.reltime(t[-1], timeunits)
                        copy_mthd.yticlabels1 = vcs.generate_time_labels(
                            t0,
                            t1,
                            timeunits,
                            calendar)
            except Exception:
                pass

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

        def set_convert_labels(copy_mthd, test=0):
            did_something = False
            for axc in ['x', 'y']:
                try:
                    mthd = getattr(copy_mthd, axc + 'axisconvert')
                    if mthd != 'linear':
                        for num in ['1', '2']:
                            if getattr(
                                    copy_mthd, axc + 'ticlabels' + num) == '*':
                                if axc == 'x':
                                    axn = -1
                                else:
                                    axn = -2
                                dic = mkdic(mthd, arglist[0].getAxis(axn)[:])
                                if test == 0:
                                    setattr(
                                        copy_mthd,
                                        axc +
                                        'ticlabels' +
                                        num,
                                        dic)
                                did_something = True
                except Exception:
                    pass
            return did_something

        if set_convert_labels(check_mthd, test=1):
            if copy_mthd is None:
                try:
                    copy_mthd = vcs.creategraphicsmethod(arglist[3], arglist[4])
                except Exception:
                    pass
                check_mthd = copy_mthd
                set_convert_labels(copy_mthd)
        if copy_mthd is None:
            try:
                copy_mthd = vcs.creategraphicsmethod(arglist[3], arglist[4])
            except Exception:
                pass
            check_mthd = copy_mthd

        x = None
        y = None
        try:
            if arglist[0].getAxis(-1).isLongitude():
                x = "longitude"
            elif arglist[0].getAxis(-1).isLatitude():
                x = "latitude"
            # in ["GXy","GXY"]:
            if check_mthd.g_name == "G1d" and (
                    check_mthd.flip or arglist[1] is not None):
                datawc_x1 = MV2.minimum(arglist[0])
                datawc_x2 = MV2.maximum(arglist[0])
                x = None
            else:
                try:
                    if arglist[0].getAxis(-1).isCircularAxis():
                        datawc_x1 = arglist[0].getAxis(-1)[0]
                    else:
                        datawc_x1 = arglist[0].getAxis(-1).getBounds()[0][0]
                except Exception:
                    datawc_x1 = arglist[0].getAxis(-1)[0]
                try:
                    if arglist[0].getAxis(-1).isCircularAxis():
                        datawc_x2 = arglist[0].getAxis(-1)[-1]
                    else:
                        datawc_x2 = arglist[0].getAxis(-1).getBounds()[-1][1]
                except Exception:
                    datawc_x2 = arglist[0].getAxis(-1)[-1]
            if arglist[0].getAxis(-2).isLongitude():
                y = "longitude"
            elif arglist[0].getAxis(-2).isLatitude():
                y = "latitude"

            if check_mthd.g_name == "G1d" and not check_mthd.flip and arglist[
                    1] is None:  # in ["GYx",]:
                datawc_y1 = MV2.minimum(arglist[0])
                datawc_y2 = MV2.maximum(arglist[0])
                y = None
            # in ["GYX",]:
            elif check_mthd.g_name == "G1d" and arglist[1] is not None:
                datawc_y1 = MV2.minimum(arglist[1])
                datawc_y2 = MV2.maximum(arglist[1])
                y = None
            else:
                try:
                    datawc_y1 = arglist[0].getAxis(-2).getBounds()[0][0]
                except Exception:
                    datawc_y1 = arglist[0].getAxis(-2)[0]
                try:
                    datawc_y2 = arglist[0].getAxis(-2).getBounds()[-1][1]
                except Exception:
                    datawc_y2 = arglist[0].getAxis(-2)[-1]
            if isinstance(arglist[0].getGrid(
            ), (cdms2.gengrid.AbstractGenericGrid, cdms2.hgrid.AbstractCurveGrid)):
                x = "longitude"
                y = "latitude"
        except Exception:
            pass
        try:
            copy_mthd = vcs.setTicksandLabels(
                check_mthd,
                copy_mthd,
                datawc_x1,
                datawc_x2,
                datawc_y1,
                datawc_y2,
                x=x,
                y=y)
        except Exception:
            pass

        if copy_mthd is not None:
            arglist[4] = copy_mthd.name
        if copy_tmpl is not None:
            arglist[2] = copy_tmpl.name

        # End of preprocessing !

        # get the background value
        bg = keyargs.get('bg', 0)

        if isinstance(arglist[3], str) and arglist[
                3].lower() == 'taylordiagram':
            for p in list(slab_changed_attributes.keys()):
                if hasattr(arglist[0], p):
                    tmp = getattr(arglist[0], p)
                else:
                    tmp = (None, None)
                setattr(arglist[0], p, slab_changed_attributes[p])
                slab_changed_attributes[p] = tmp
            # first look at the extra arguments and make sure there is no
            # duplicate
            for k in list(keyargs.keys()):
                if k not in ['template', 'skill', 'bg']:
                    del(keyargs[k])
                if k == 'template':
                    arglist[2] = keyargs[k]
                    del(keyargs[k])
            # look through the available taylordiagram methods and use the plot
            # function
            t = vcs.elements["taylordiagram"].get(arglist[4], None)
            if t is None:
                raise ValueError(
                    "unknown taylordiagram graphic method: %s" %
                    arglist[4])
            t.plot(arglist[0], canvas=self, template=arglist[2], **keyargs)

            dname = keyargs.get("display_name")
            if dname is not None:
                dn = vcs.elements["display"][dname]
            else:
                nm, src = self.check_name_source(None, "default", "display")
                dn = displayplot.Dp(nm)
            dn.continents = self.getcontinentstype()
            dn.continents_line = self.getcontinentsline()
            dn.template = arglist[2]
            dn.g_type = arglist[3]
            dn.g_name = arglist[4]
            dn.array = arglist[:2]
            dn.extradisplays = t.displays
            for p in list(slab_changed_attributes.keys()):
                tmp = slab_changed_attributes[p]
                if tmp == (None, None):
                    delattr(arglist[0], p)
                else:
                    setattr(arglist[0], p, tmp)
            dn.newelements = self.__new_elts(original_elts, new_elts)
            dn._parent = self

            return dn
        else:  # not taylor diagram
            if hasVCSAddons and isinstance(arglist[3], vcsaddons.core.VCSaddon):
                gm = arglist[3]
            else:
                tp = arglist[3]
                if tp == "text":
                    tp = "textcombined"
                elif tp == "default":
                    tp = "boxfill"
                elif tp in ("xvsy", "xyvsy", "yxvsx", "scatter"):
                    tp = "1d"
                gm = vcs.elements[tp][arglist[4]]
                if hasattr(gm, "priority") and gm.priority == 0:
                    return
            p = self.getprojection(gm.projection)
            if p.type in no_deformation_projections and (
                    doratio == "0" or doratio[:4] == "auto"):
                doratio = "1t"
            for keyarg in list(keyargs.keys()):
                if keyarg not in self.__class__._plot_keywords_ + self.backend._plot_keywords:
                    if keyarg in self.__class__._deprecated_plot_keywords_:
                        warnings.warn("Deprecation Warning: Keyword '%s' will be removed in the next version"
                                      "of UV-CDAT." % keyarg, vcs.VCSDeprecationWarning)
                    else:
                        warnings.warn(
                            'Unrecognized vcs plot keyword: %s, assuming backend (%s) keyword' %
                            (keyarg, self.backend.type))

            if arglist[0] is not None or 'variable' in keyargs:
                arglist[0] = self._reconstruct_tv(arglist, keyargs)
                # Now applies the attributes change
                for p in list(slab_changed_attributes.keys()):
                    if hasattr(arglist[0], p):
                        tmp = getattr(arglist[0], p)
                    else:
                        tmp = (None, None)
                    setattr(arglist[0], p, slab_changed_attributes[p])
                    slab_changed_attributes[p] = tmp
                # Now applies the axes changes
                for i in list(axes_changed.keys()):
                    arglist[0].setAxis(i, axes_changed[i])
                for i in list(axes_changed2.keys()):
                    arglist[1].setAxis(i, axes_changed2[i])
            # Check to make sure that you have at least 2 dimensions for the follow graphics methods
            # Flipping the order to avoid the tv not exist problem
            if (arglist[3] in ['boxfill', 'isofill', 'isoline', 'vector']) and (
                    len(arglist[0].shape) < 2):
                raise vcsError(
                    'Invalid number of dimensions for %s' %
                    arglist[3])

            # Ok now does the linear projection for lat/lon ratio stuff
            if arglist[3] in ['marker', 'line', 'fillarea', 'text']:
                # fist create a dummy template
                t = self.createtemplate()
                # Now creates a copy of the primitives, in case it's used on
                # other canvases with diferent ratios
                if arglist[3] == 'text':
                    nms = arglist[4].split(":::")
                    p = self.createtext(Tt_source=nms[0], To_source=nms[1])
                elif arglist[3] == 'marker':
                    p = self.createmarker(source=arglist[4])
                elif arglist[3] == 'line':
                    p = self.createline(source=arglist[4])
                elif arglist[3] == 'fillarea':
                    p = self.createfillarea(source=arglist[4])
                t.data.x1 = p.viewport[0]
                t.data.x2 = p.viewport[1]
                t.data.y1 = p.viewport[2]
                t.data.y2 = p.viewport[3]

                proj = self.getprojection(p.projection)
                if proj.type in no_deformation_projections and (
                        doratio == "0" or doratio[:4] == "auto"):
                    doratio = "1t"

                if proj.type == 'linear' and doratio[:4] == 'auto':
                    lon1, lon2, lat1, lat2 = p.worldcoordinate
                    t.ratio_linear_projection(
                        lon1,
                        lon2,
                        lat1,
                        lat2,
                        None,
                        box_and_ticks=box_and_ticks)
                    p.viewport = [t.data.x1, t.data.x2, t.data.y1, t.data.y2]
                    arglist[4] = p.name
                elif doratio not in ['0', 'off', 'none', 'auto', 'autot']:
                    if doratio[-1] == 't':
                        doratio = doratio[:-1]
                    Ratio = float(doratio)
                    t.ratio(Ratio)
                    p.viewport = [t.data.x1, t.data.x2, t.data.y1, t.data.y2]
                    if arglist[3] == 'text':
                        arglist[4] = p.Tt_name + ':::' + p.To_name
                    else:
                        arglist[4] = p.name
                else:
                    if arglist[3] == 'text' and keyargs.get(
                            "donotstoredisplay", False) is True:
                        sp = p.name.split(":::")
                        del(vcs.elements["texttable"][sp[0]])
                        del(vcs.elements["textorientation"][sp[1]])
                        del(vcs.elements["textcombined"][p.name])
                    elif arglist[3] == 'marker':
                        del(vcs.elements["marker"][p.name])
                    elif arglist[3] == 'line':
                        del(vcs.elements["line"][p.name])
                    elif arglist[3] == 'fillarea':
                        del(vcs.elements["fillarea"][p.name])
                # cleanup temp template
                del(vcs.elements["template"][t.name])
            elif (arglist[3] in ['boxfill', 'isofill', 'isoline',
                                 'vector', 'meshfill'] or
                  (hasVCSAddons and isinstance(arglist[3], vcsaddons.core.VCSaddon))) and \
                    doratio in ['auto', 'autot'] and not (doratio == 'auto' and arglist[2] == 'ASD'):
                box_and_ticks = 0
                if doratio[-1] == 't' or template_origin == 'default':
                    box_and_ticks = 1

                if hasVCSAddons and isinstance(arglist[3], vcsaddons.core.VCSaddon):
                    gm = arglist[3]
                else:
                    tp = arglist[3]
                    if tp == "text":
                        tp = "textcombined"
                    gm = vcs.elements[tp][arglist[4]]
                p = self.getprojection(gm.projection)
                if p.type in no_deformation_projections:
                    doratio = "1t"
                if p.type == 'linear':
                    if gm.g_name == 'Gfm':
                        if self.isplottinggridded:
                            # TODO: This computation is wrong as a meshfill can be wrapped.
                            # this means that we have to create the VTK dataset before
                            # we know the actual lon1, lon2.
                            lon1, lon2 = vcs.minmax(arglist[1][..., :, 1, :])
                            lat1, lat2 = vcs.minmax(arglist[1][..., :, 0, :])
                            if lon2 - lon1 > 360:
                                lon1, lon2 = 0., 360.
                            if gm.datawc_x1 < 9.99E19:
                                lon1 = gm.datawc_x1
                            if gm.datawc_x2 < 9.99E19:
                                lon2 = gm.datawc_x2
                            if gm.datawc_y1 < 9.99E19:
                                lat1 = gm.datawc_y1
                            if gm.datawc_y2 < 9.99E19:
                                lat2 = gm.datawc_y2
                            if copy_tmpl is None:
                                copy_tmpl = vcs.createtemplate(
                                    source=arglist[2])
                                arglist[2] = copy_tmpl.name
                            copy_tmpl.ratio_linear_projection(
                                lon1,
                                lon2,
                                lat1,
                                lat2,
                                None,
                                box_and_ticks=box_and_ticks)
                    elif arglist[0].getAxis(-1).isLongitude() and arglist[0].getAxis(-2).isLatitude():
                        if copy_tmpl is None:
                            copy_tmpl = vcs.createtemplate(source=arglist[2])
                        if gm.datawc_x1 < 9.99E19:
                            lon1 = gm.datawc_x1
                        else:
                            lon1 = min(arglist[0].getAxis(-1))
                        if gm.datawc_x2 < 9.99E19:
                            lon2 = gm.datawc_x2
                        else:
                            lon2 = max(arglist[0].getAxis(-1))
                        if gm.datawc_y1 < 9.99E19:
                            lat1 = gm.datawc_y1
                        else:
                            lat1 = min(arglist[0].getAxis(-2))
                        if gm.datawc_y2 < 9.99E19:
                            lat2 = gm.datawc_y2
                        else:
                            lat2 = max(arglist[0].getAxis(-2))
                        copy_tmpl.ratio_linear_projection(
                            lon1,
                            lon2,
                            lat1,
                            lat2,
                            None,
                            box_and_ticks=box_and_ticks,
                            x=self)
                        arglist[2] = copy_tmpl.name
            elif not (doratio in ['0', 'off', 'none', 'auto', 'autot']) or\
                (arglist[3] in ['boxfill', 'isofill', 'isoline', 'vector', 'meshfill'] and
                 str(doratio).lower() in ['auto', 'autot']) and arglist[2] != 'ASD':
                box_and_ticks = 0
                if doratio[-1] == 't' or template_origin == 'default':
                    box_and_ticks = 1
                    if doratio[-1] == 't':
                        doratio = doratio[:-1]
                try:
                    Ratio = float(doratio)
                except Exception:
                    Ratio = doratio
                if copy_tmpl is None:
                    copy_tmpl = vcs.createtemplate(source=arglist[2])
                    arglist[2] = copy_tmpl.name
                copy_tmpl.ratio(Ratio, box_and_ticks=box_and_ticks, x=self)

            if hasattr(self, '_isplottinggridded'):
                del(self._isplottinggridded)
            # Get the continents for animation generation
            self.animate.continents_value = self._continentspath()

            # Get the option for doing graphics in the background.
            if bg:
                arglist.append(True)
            else:
                arglist.append(False)
            if arglist[3] == 'scatter':
                if not (
                        numpy.equal(arglist[0].getAxis(-1)[:], arglist[1].getAxis(-1)[:]).all()):
                    raise vcsError(
                        'Error - ScatterPlot requires X and Y defined in the same place')
            if arglist[3] == 'vector':
                if not (numpy.equal(arglist[0].getAxis(-1)[:], arglist[1].getAxis(-1)[:]).all()) or not(
                        numpy.equal(arglist[0].getAxis(-2)[:], arglist[1].getAxis(-2)[:]).all()):
                    raise vcsError(
                        'Error - VECTOR components must be on the same grid.')
            if "bg" in keyargs:
                del(keyargs["bg"])
            if hasVCSAddons and isinstance(arglist[3], vcsaddons.core.VCSaddon):
                if arglist[1] is None:
                    dn = arglist[3].plot(
                        arglist[0],
                        template=arglist[2],
                        bg=bg,
                        x=self,
                        **keyargs)
                else:
                    dn = arglist[3].plot(
                        arglist[0],
                        arglist[1],
                        template=arglist[2],
                        bg=bg,
                        x=self,
                        **keyargs)
            else:
                returned_kargs = self.backend.plot(*arglist, **keyargs)
                if not keyargs.get("donotstoredisplay", False):
                    dname = keyargs.get("display_name")
                    if dname is not None:
                        dn = vcs.elements['display'][dname]
                    else:
                        nm, src = self.check_name_source(
                            None, "default", "display")
                        dn = displayplot.Dp(nm, parent=self)
                    dn.template = arglist[2]
                    dn.g_type = arglist[3]
                    dn.g_name = arglist[4]
                    dn.array = arglist[:2]
                    dn.backend = returned_kargs
                else:
                    dn = None

                if dn is not None:
                    dn._template_origin = template_origin
                    dn.ratio = keyargs.get("ratio", None)
                    dn.continents = self.getcontinentstype()
                    dn.continents_line = self.getcontinentsline()
                    dn.newelements = self.__new_elts(original_elts, new_elts)

            if self.mode != 0:
                # self.update()
                pass

        result = dn
        if isinstance(arglist[3], str):
            # Pointer to the plotted slab of data and the VCS Canas display infomation.
            # This is needed to find the animation min and max values and the number of
            # displays on the VCS Canvas.
            if dn is not None:
                self.animate_info.append((result, arglist[:2]))

        # Now executes output commands
        for cc in list(cmds.keys()):
            c = cc.lower()
            if not isinstance(cmds[cc], type('')):
                args = tuple(cmds[cc])
            else:
                args = (cmds[cc],)
            if c == 'ps' or c == 'postscript':
                self.postscript(*args)
            elif c == 'pdf':
                self.pdf(*args)
            elif c == 'gif':
                self.gif(*args)
            elif c == 'eps':
                self.eps(*args)
            elif c == 'cgm':
                self.cgm(*args)
            elif c == 'ras':
                self.ras(*args)

        # self.clean_auto_generated_objects("template")
        for p in list(slab_changed_attributes.keys()):
            tmp = slab_changed_attributes[p]
            if tmp == (None, None):
                delattr(arglist[0], p)
            else:
                setattr(arglist[0], p, tmp)
        if dn is not None and not isinstance(dn, (list, tuple)):
            self.display_names.append(result.name)
            if result.g_type in (
                    "3d_scalar", "3d_vector") and self.configurator is not None:
                self.endconfigure()
            if self.backend.bg is False and self.configurator is not None:
                self.configurator.update()

        return result

    def setAnimationStepper(self, stepper):
        self.backend.setAnimationStepper(stepper)

    def return_display_names(self, *args):
        """Show the list of display names associated with all active plots
        on the canvas.

        :Example:

            .. doctest:: canvas_return_display_name

                >>> a=vcs.init()
                >>> a.return_display_names() # new canvas should have none
                []
                >>> array=[range(10) for _ in range(10)]
                >>> a.plot(array)
                <vcs.displayplot.Dp ...>
                >>> a.return_display_names() # has display name for new plot
                [...]

        :return: A list of the display names of images currently plotted
            on the canvas.
        :rtype: `list`_
        """
        return self.display_names

    def remove_display_name(self, *args):
        """Removes a plotted item from the canvas.

        :Example:

            .. doctest:: canvas_remove_display_name

                >>> a=vcs.init()
                >>> a.return_display_names() # new canvas should have none
                []
                >>> array=[range(10) for _ in range(10)]
                >>> plot=a.plot(array) # store plot for reference to plot name
                >>> a.return_display_names() # has display name for new plot
                [...]
                >>> a.remove_display_name(plot.name)
                >>> a.return_display_names() # should be empty again
                []

        :param args: Any number of display names to remove.
        :type args: list of `str`_
        """
        for a in args:
            if a in self.display_names:
                self.display_names.remove(a)
        self.update()

    def cgm(self, file, mode='w'):
        """
        .. deprecated:: 2.6.1

            Exporting images to CGM format is no longer supported.
            To generate an image from the canvas, see
            :py:func:`vcs.Canvas.Canvas.png` or :py:func:`vcs.Canvas.Canvas.svg`

        Export an image in CGM format.

        :param file: Filename to save
        :param mode: Ignored.

        .. pragma: skip-doctest REMOVE WHEN IT WORKS AGAIN!
        """

        if mode != 'w':
            warnings.warn(
                "cgm only supports 'w' mode ignoring your mode ('%s')" %
                mode)
        return self.backend.cgm(file)

    def clear(self, *args, **kargs):
        """Clears all the VCS displays on a page (i.e., the VCS Canvas object).

        :Example:

            .. doctest:: canvas_clear

                >>> a=vcs.init()
                >>> array = [range(1, 11) for _ in range(1, 11)]
                >>> a.plot(array,'default','isofill','quick')
                <vcs.displayplot.Dp ...>
                >>> a.clear() # clear VCS displays from the page

        """
        if self.animate.created():
            self.animate.close()
        if self.configurator is not None:
            self.configurator.stop_animating()
        self.animate_info = []
        self.animate.update_animate_display_list()

        preserve_display = kargs.get("preserve_display", False)
        if "preserve_display" in kargs:
            del kargs["preserve_display"]
        self.backend.clear(*args, **kargs)
        for nm in self.display_names:
            # Lets look at elements created by dispaly production
            # Apparently when updating we shouldn't be clearing these elemnts
            # yet
            if kargs.get("render", True):
                dn = vcs.elements["display"][nm]
                new_elts = getattr(dn, "newelements", {})
                for e in list(new_elts.keys()):
                    if e == "display":
                        continue
                    for k in new_elts[e]:
                        if k in list(vcs.elements[e].keys()):
                            del(vcs.elements[e][k])
            if not preserve_display:
                del(vcs.elements["display"][nm])
        self.display_names = []
        return

    def close(self, *args, **kargs):
        """Close the VCS Canvas. It will not deallocate the VCS Canvas object.
        To deallocate the VCS Canvas, use the destroy method.

        :Example:

            .. doctest:: canvas_close

                >>> a=vcs.init()
                >>> array = [range(1, 11) for _ in range(1, 11)]
                >>> a.plot(array,'default','isofill','quick')
                <vcs.displayplot.Dp ...>
                >>> a.close() #close the vcs canvas

        """
        if self.configurator:
            self.endconfigure()
        a = self.backend.close(*args, **kargs)
        self.animate_info = []

        return a

    def destroy(self):
        """Destroy the VCS Canvas. It will deallocate the VCS Canvas object.

        :Example:

            .. doctest:: canvas_destroy

                >>> a=vcs.init()
                >>> array = [range(1, 11) for _ in range(1, 11)]
                >>> a.plot(array,'default','isofill','quick')
                <vcs.displayplot.Dp ...>
                >>> a.destroy()

        """
        import gc

        del self
        gc.garbage
        gc.collect()

    def change_display_graphic_method(self, display, type, name):
        """Changes the type and graphic method of a plot.

        :Example:

            .. doctest:: canvas_change_display_graphic_method

                >>> a=vcs.init()
                >>> cdgm=a.change_display_graphic_method # alias long name
                >>> array=[range(10) for _ in range(10)]
                >>> disp=a.plot(array)
                >>> a.show('boxfill') # list boxfill names
                *******************Boxfill Names List**********************
                ...
                *******************End Boxfill Names List**********************
                >>> cdgm(disp, 'boxfill', 'polar') # change graphics method

        :param display: Display to change.
        :param type: New graphics method type.
        :param name: Name of new graphics method.
        :type display: `str`_ or vcs.displayplot.Dp
        :type name: `str`_
        :type type: `str`_
        """

        if isinstance(display, str):
            display = vcs.elements["display"][display]
        display.g_type = type
        display.g_name = name
        self.update()

    def get_selected_display(self):
        """
        .. attention::

            This function does not currently work.
            It will be implemented in the future.

        .. pragma: skip-doctest REMOVE WHEN IT WORKS AGAIN!
        """
        return self.canvas.get_selected_display(*())

    def plot_annotation(self, *args):
        self.canvas.plot_annotation(*args)

    def flush(self, *args):
        """The flush command executes all buffered X events in the queue.

        :Example:

            .. doctest:: canvas_flush

                >>> a=vcs.init()
                >>> array = [range(1, 11) for _ in range(1, 11)]
                >>> a.plot(array,'default','isofill','quick')
                <vcs.displayplot.Dp ...>
                >>> a.flush()
        """
        return self.backend.flush(*args)

    def geometry(self, *args):
        """The geometry command is used to set the size and position of the VCS canvas.

        :Example:

            .. doctest:: canvas_geometry

                >>> a=vcs.init()
                >>> array = [range(1, 11) for _ in range(1, 11)]
                >>> a.plot(array,'default','isofill','quick')
                <vcs.displayplot.Dp ...>
                >>> a.geometry(450,337)
        """
        if len(args) == 0:
            return self.backend.geometry()

        if (args[0] <= 0) or (args[1] <= 0):
            raise ValueError(
                'Error -  The width and height values must be an integer greater than 0.')

        a = self.backend.geometry(*args)
        self.flush()  # update the canvas by processing all the X events

        return a

    def canvasinfo(self, *args, **kargs):
        """Obtain the current attributes of the VCS Canvas window.

        :Example:

            .. doctest:: canvas_canvasinfo

                >>> a=vcs.init()
                >>> ci=a.canvasinfo()
                >>> keys=sorted(a.canvasinfo().keys())
                >>> for key in keys:
                ...     print(key, str(ci[key]))
                depth ...
                height ...
                mapstate ...
                width ...
                x ...
                y ...

        :returns: Dictionary with keys: "mapstate" (whether the canvas is opened),
            "height", "width", "depth", "x", "y"
        :rtype: dict
        """
        return self.backend.canvasinfo(*args, **kargs)

    def getcontinentstype(self, *args):
        """Retrieve continents type from VCS; either an integer between 0 and 6 or the
        path to a custom continentstype.

        :Example:

            .. doctest:: canvas_getcontinentstype

                >>> a=vcs.init()
                >>> a.setcontinentstype(6)
                >>> a.getcontinentstype() # Get the continents type
                6

        :returns An int between 0 and 6, or the path to a custom continentstype
        :rtype: `int`_ or system filepath
        """
        try:
            return self._continents
        except Exception:
            return None

    def landscape(self, width=-99, height=-99, x=-99, y=-99, clear=0):
        """Change the VCS Canvas orientation to Landscape.

        .. note::

            The (width, height) and (x, y) arguments work in pairs. That is, you must
            set (width, height) or (x, y) together to see any change in the VCS Canvas.

            If the portrait method is called  with arguments before displaying a VCS Canvas,
            then the arguments (width, height, x, y, and clear) will have no effect on the
            canvas.

        .. warning::

            If the visible plot on the VCS Canvas is not adjusted properly, then resize
            the screen with the point. Some X servers are not handling the threads properly
            to keep up with the demands of the X client.

        :Example:

            .. doctest:: canvas_landscape

                >>> a=vcs.init()
                >>> array = [range(1, 11) for _ in range(1, 11)]
                >>> a.plot(array)
                <vcs.displayplot.Dp ...>
                >>> a.landscape() # Change the VCS Canvas orientation and set object flag to landscape
                >>> a.landscape(clear=1) # Change the VCS Canvas to landscape and clear the page
                >>> a.landscape(width = 400, height = 337) # Change to landscape and set the window size
                >>> a.landscape(x=100, y = 200) # Change to landscape and set the x and y screen position
                >>> a.landscape(width = 400, height = 337, x=100, y = 200, clear=1) # landscape with more settings

        %s
        %s

        :param x: Unused
        :type x: `int`_

        :param y: Unused
        :type y: `int`_
        %s
        """
        if (self.orientation() == 'landscape'):
            return

        if (((not isinstance(width, int))) or ((not isinstance(height, int))) or
                ((not isinstance(x, int))) or ((not isinstance(y, int))) or
                ((width != -99) and (width < 0)) or ((height != -99) and (height < 0)) or
                ((x != -99) and (x < 0)) or ((y != -99) and (y < 0))):
            raise ValueError(
                'If specified, width, height, x, and y must be integer values greater than or equal to 0.')
        if (((not isinstance(clear, int))) and (clear not in [0, 1])):
            raise ValueError(
                "clear must be: 0 - 'the default value for not clearing the canvas' or 1 - 'for clearing the canvas'.")

        if ((width == -99) and (height == -99) and (x == -99) and (y == -99) and (clear == 0)):
            cargs = ()
            try:
                dict = self.canvasinfo(*cargs)
            except Exception:
                dict = {}
            height = dict.get('width', -99)
            width = dict.get('height', -99)
            x = dict.get('x', -99)
            y = dict.get('y', -99)
        self.flush()  # update the canvas by processing all the X events

        args = (width, height, x, y, clear)
        return self.backend.landscape(*args)
    landscape.__doc__ = landscape.__doc__ % (xmldocs.canvas_width, xmldocs.canvas_height, xmldocs.canvas_clear)

    def listelements(self, *args):
        """Returns a sorted Python list of all VCS object names, or a list of
        names of objects of the given type.

        :Example:

            .. doctest:: canvas_listelements

                >>> a=vcs.init()
                >>> a.listelements()
                ['1d', '3d_dual_scalar', '3d_scalar', ...]

        :param args: A string containing the name of a VCS object type, or None
        :type args: `str`_ or `None`_

        :returns: If args is None, returns a list of string names of all VCS objects.
            If args is a string name of a VCS object
        :rtype: `list`_
        """
        f = vcs.listelements
        L = sorted(f(*args))

        return L

    def updateorientation(self, *args):
        """Takes a string 'portrait' or 'landscape' and updates a Canvas object's
        orientation accordingly.

        :param args: String with value 'landscape' or 'portrait'
        :type args: `str`_

        .. attention::

            This function does not currently work.
            It will be implemented in the future.

            Use :func:`landscape` or :func:`portrait` instead.

        .. pragma: skip-doctest REMOVE WHEN IT WORKS AGAIN!
        """
        a = self.canvas.updateorientation(*args)

        return a

    def open(self, width=None, height=None, **kargs):
        """Open VCS Canvas object. This routine really just manages the VCS canvas.
        It can be used to display the VCS Canvas.

        :Example:

            .. doctest:: canvas_open

                >>> a=vcs.init()
                >>> a.open()
                >>> a.open(800,600)

        %s
        %s
        """

        a = self.backend.open(width, height, **kargs)

        return a
    open.__doc__ = open.__doc__ % (xmldocs.canvas_width, xmldocs.canvas_height)

    def canvasid(self, *args):
        """Get the ID of this canvas.
        This ID number is found at the top of the VCS Canvas,
        as part of its title.

        :Example:

            .. doctest:: canvas_canvasid

                >>> a=vcs.init()
                >>> cid = a.canvasid() # store the canvas id

        :returns: The ID of the canvas on which canvasid() is called.
        :rtype: int
        """
        return self._canvas_id

    def portrait(self, width=-99, height=-99, x=-99, y=-99, clear=0):
        """Change the VCS Canvas orientation to Portrait.

        .. note::

            If the current orientation of the canvas is already portrait, nothing happens.

        :Example:

            .. doctest:: canvas_portrait

                >>> a=vcs.init()
                >>> array = [range(1, 11) for _ in range(1, 11)]
                >>> a.plot(array)
                <vcs.displayplot.Dp ...>
                >>> a.portrait()  # Change the VCS Canvas orientation and set object flag to portrait
                >>> a.portrait(clear=1) # Change the VCS Canvas to portrait and clear the page
                >>> a.portrait(width = 337, height = 400) # Change to portrait and set the window size
                >>> a.portrait(x=100, y = 200) # Change to portrait and set the x and y screen position
                >>> a.portrait(width = 337, height = 400, x=100, y = 200, clear=1) # portrait, with more specifications

        %s
        %s

        :param x: Unused.
        :type x: None

        :param y: Unused.
        :type y: None

        %s
        """
        if (self.orientation() == 'portrait'):
            return

        if (((not isinstance(width, int))) or ((not isinstance(height, int))) or
                ((not isinstance(x, int))) or ((not isinstance(y, int))) or
                ((width != -99) and (width < 0)) or ((height != -99) and (height < 0)) or
                ((x != -99) and (x < 0)) or ((y != -99) and (y < 0))):
            raise ValueError(
                'If specified, width, height, x, and y must be integer values greater than or equal to 0.')
        if (((not isinstance(clear, int))) and (clear not in [0, 1])):
            raise ValueError(
                "clear must be: 0 - 'the default value for not clearing the canvas' or 1 - 'for clearing the canvas'.")

        if ((width == -99) and (height == -99) and (x == -99) and (y == -99) and (clear == 0)):
            cargs = ()
            try:
                dict = self.canvasinfo(*cargs)
            except Exception:
                dict = {}
            height = dict.get('width', -99)
            width = dict.get('height', -99)
            x = dict.get('x', -99)
            y = dict.get('y', -99)
        self.flush()  # update the canvas by processing all the X events

        args = (width, height, x, y, clear)
        p = self.backend.portrait(*args)

        return p

    portrait.__doc__ = portrait.__doc__ % (xmldocs.canvas_width, xmldocs.canvas_height, xmldocs.canvas_clear)

    def ffmpeg(self, movie, files, bitrate=1024, rate=None, options=None):
        """MPEG output from a list of valid files.
        Can output to more than just mpeg format.

        .. note::

            ffmpeg ALWAYS overwrites the output file

        .. admonition:: Audio configuration

            via the options arg you can add audio file to your movie (see ffmpeg help)

        :Example:

            .. doctest:: canvas_ffmpeg

                >>> a=vcs.init()
                >>> import cdms2
                >>> f = cdms2.open(vcs.sample_data+'/clt.nc')
                >>> v = f('v') # use the data file to create a cdms2 slab
                >>> u = f('u') # use the data file to create a cdms2 slab
                >>> png_files = [] # for saving file names to make the mpeg
                >>> for i in range(10): # create a number of pngs to use for an mpeg
                ...     a.clear()
                ...     if (i%2):
                ...         a.plot(u,v)
                ...     else:
                ...         a.plot(v,u)
                ...     a.png('my_png__%i' % i)
                ...     png_files.append('my_png__%i.png' % i)
                <vcs.displayplot.Dp object at 0x...>
                <vcs.displayplot.Dp object at 0x...>
                <vcs.displayplot.Dp object at 0x...>
                <vcs.displayplot.Dp object at 0x...>
                <vcs.displayplot.Dp object at 0x...>
                <vcs.displayplot.Dp object at 0x...>
                <vcs.displayplot.Dp object at 0x...>
                <vcs.displayplot.Dp object at 0x...>
                <vcs.displayplot.Dp object at 0x...>
                <vcs.displayplot.Dp object at 0x...>
                >>> a.ffmpeg('m1.mpeg',png_files) # using list of files
                <vcs.Canvas.JupyterFFMPEG object at 0x...>
                >>> a.ffmpeg('m2.mpeg',png_files,bitrate=512) # 512kbit rate
                <vcs.Canvas.JupyterFFMPEG object at 0x...>
                >>> a.ffmpeg('m3.mpeg',png_files,rate=50) # 50 frames/second
                <vcs.Canvas.JupyterFFMPEG object at 0x...>

        :param movie: Output video file name
        :type movie: `str`_

        :param files: String name of a file,
            or a list or tuple of multiple file names
        :type files: `str`_, `list`_, or :py:class:`tuple`

        :param rate: Desired output framerate
        :type rate: `str`_

        :param options: Additional FFMPEG arguments
        :type options: `str`_

        :returns: A object that Jupyter notebook can display
        :rtype: JupyterFFMPEG

        """
        args = ["ffmpeg", "-y"]

        if rate is not None:
            args.extend(("-framerate", str(rate)))

        if isinstance(files, (list, tuple)):
            test_file = files[0]

            rnd = "%s/.uvcdat/__uvcdat_%i" % (
                os.path.expanduser("~"), numpy.random.randint(600000000))
            Files = []
            for i, f in enumerate(files):
                fnm = "%s_%i.png" % (rnd, i)
                shutil.copy(f, fnm)
                Files.append(fnm)
            args.extend(("-i", "%s_%%d.png" % rnd))
        elif isinstance(files, str):
            # Extract formatter
            percent_re = re.compile(r"(%0*d)")
            str_format = percent_re.search(files)
            if str_format is not None:
                prefix, group, suffix = percent_re.split(files, maxsplit=1)
                numeric_length = len(str_format.group(0).split("0")) - 1
                path, pre = os.path.split(prefix)
                if path == '':
                    path = "."
                file_names = os.listdir(path)
                for f in file_names:
                    # Make sure it starts with the "before number" part
                    if not f.startswith(pre):
                        continue

                    # Make sure the length is correct
                    if len(f) != len(pre) + numeric_length + len(suffix):
                        continue

                    # Iterate the numeric section
                    for i in range(len(pre), len(pre) + numeric_length):
                        try:
                            int(f[i])
                        except ValueError:
                            # Invalid character found, exit the loop
                            break
                    else:
                        # Make sure the ending is correct
                        if f.endswith(suffix):
                            test_file = os.path.join(path, f)
                            # We found a test file, we can stop now
                            break
                else:
                    test_file = False

            args.extend(('-i', files))

        args.extend(("-pix_fmt", "yuv420p"))

        if test_file is not False:
            # H264 requires even numbered heights and widths
            width, height = self.backend.png_dimensions(test_file)
            if width % 2 == 1:
                width = width + 1
            if height % 2 == 1:
                height = height + 1
            args.extend(("-vf", "scale=%d:%d" % (width, height)))

        if options is not None:
            args.append(options)

        args.append(movie)

        result = subprocess.call(args)

        if isinstance(files, (list, tuple)):
            for f in Files:
                os.remove(f)

        return JupyterFFMPEG(movie, result)

    def getantialiasing(self):
        """Returns the current antialiasing rate for the canvas.

        :Example:

            .. doctest:: canvas_getantialiasing

                >>> a=vcs.init()
                >>> a.setantialiasing(0) # turn off antialiasing
                >>> a.getantialiasing() # will return current antialiasing rate
                0

        :return: antialiasing rate for the canvas
        :rtype: int
        """
        return self.backend.getantialiasing()

    def setantialiasing(self, antialiasing):
        """Sets the antialiasing rate for the canvas.

        :Example:

            .. doctest:: canvas_setantialiasing

                >>> a=vcs.init()
                >>> a.setantialiasing(20)
                >>> a.getantialiasing()
                20

        :param antialiasing: Integer from 0-64, representing the antialising
            rate (0 means no antialiasing).
        :type antialiasing: `int`_
        """
        self.backend.setantialiasing(antialiasing)

    def setbgoutputdimensions(self, width=None, height=None, units='inches'):
        """Sets dimensions for output in bg mode.

        :Example:

            .. doctest:: canvas_setbgoutputdimensions

                >>> a=vcs.init()
                >>> a.setbgoutputdimensions(width=11.5, height= 8.5) # US Legal
                >>> a.setbgoutputdimensions(width=21, height=29.7, units='cm') # A4

        %s
        %s
        %s
        """
        if units not in [
                'inches', 'in', 'cm', 'mm', 'pixel', 'pixels', 'dot', 'dots']:
            raise Exception(
                "units must be on of inches, in, cm, mm, pixel(s) or dot(s)")

        W, H = self._compute_width_height(
            width, height, units)

        # in pixels?
        self.width = W
        self.height = H
        return
    # display ping
    setbgoutputdimensions.__doc__ = setbgoutputdimensions.__doc__ % (xmldocs.output_width, xmldocs.output_height,
                                                                     xmldocs.output_units)

    def put_png_on_canvas(
            self, filename, zoom=1, xOffset=0, yOffset=0,
            units="percent", fitToHeight=True, *args, **kargs):
        """Display a PNG file on the canvas

        :Example:

            .. doctest:: manageElements_put_png_on_canvas

                >>> a=vcs.init()
                >>> array=[range(10) for i in range(10)]
                >>> a.plot(array)
                <vcs.displayplot.Dp ...>
                >>> a.png("bars.png") # make a png named 'bars.png'
                >>> a.clear() # clear the bars off the canvas
                >>> a.put_png_on_canvas("bars.png") # put 'bars.png' on canvas

        :param file: Input image filename
        :type file: `str`_

        :param zoom: scale factor
        :type zoom: `int`_

        :param xOffset: Horizontal Offset
        :type xOffset: float

        :param yOffset: Vertical Offset
        :type yOffset: float

        :param units: Specifies the units used for x and y Offsets.
            One of ['percent','pixels'].
        :type units: `str`_

        :param fitToHeight: If True, fits the picture (before scaling) to the canvas full height,
            if False then use png original size.
        :type fitToHeight: bool
        """
        self.backend.put_png_on_canvas(
            filename,
            zoom,
            xOffset,
            yOffset,
            units,
            fitToHeight,
            *args,
            **kargs)

    def png(self, file, width=None, height=None,
            units=None, draw_white_background=True, **args):
        """PNG output, dimensions set via setbgoutputdimensions

        :Example:

            .. doctest:: canvas_png

                >>> a=vcs.init()
                >>> array = [range(1, 11) for _ in range(1, 11)]
                >>> a.plot(array)
                <vcs.displayplot.Dp ...>
                >>> a.png('example') # Overwrite a png file

        %s
        %s
        %s
        %s

        :param draw_white_background: Boolean value indicating if the
            background should be white. Defaults to True.
        :type draw_white_background: bool
        """
        base = os.path.dirname(file)
        if base != "" and not os.path.exists(base):
            raise vcsError("Output path: %s does not exist" % base)
        if units not in [
                'inches', 'in', 'cm', 'mm',
                None, 'pixel', 'pixels', 'dot', 'dots']:
            raise Exception(
                "units must be on of inches, in, cm, mm, pixel(s) or dot(s)")

        W, H = self._compute_width_height(
            width, height, units, background=True)
        return self.backend.png(
            file, W, H, units, draw_white_background, **args)
    png.__doc__ = png.__doc__ % (xmldocs.output_file, xmldocs.output_width, xmldocs.output_height, xmldocs.output_units)

    def pdf(self, file, width=None, height=None, units='inches',
            textAsPaths=True):
        """PDF output is another form of vector graphics.

        .. note::

            The textAsPaths parameter preserves custom fonts, but text can no longer be edited in the file

        :Example:

            .. doctest:: canvas_pdf

                >>> a=vcs.init()
                >>> array = [range(1, 11) for _ in range(1, 11)]
                >>> a.plot(array)
                <vcs.displayplot.Dp ...>
                >>> a.pdf('example') # Overwrite a postscript file
                >>> a.pdf('example', width=11.5, height= 8.5) # US Legal
                >>> a.pdf('example', width=21, height=29.7, units='cm') # A4

        %s
        %s
        %s
        %s

        :param textAsPaths: Specifies whether to render text objects as paths.
        :type textAsPaths: bool
        """
        if units not in [
                'inches', 'in', 'cm', 'mm', 'pixel', 'pixels', 'dot', 'dots']:
            raise Exception(
                "units must be on of inches, in, cm, mm, pixel(s) or dot(s)")

        W, H = self._compute_width_height(
            width, height, units, background=True)

        if not file.split('.')[-1].lower() in ['pdf']:
            file += '.pdf'
        return self.backend.pdf(file, width=W, height=H, units=units, textAsPaths=textAsPaths)
    pdf.__doc__ = pdf.__doc__ % (xmldocs.output_file, xmldocs.output_width, xmldocs.output_height, xmldocs.output_units)

    def svg(self, file, width=None, height=None, units='inches',
            textAsPaths=True):
        """SVG output is another form of vector graphics.

        .. note::

            The textAsPaths parameter preserves custom fonts, but text can no longer be edited in the file

        :Example:

            .. doctest:: canvas_svg

                >>> a=vcs.init()
                >>> array = [range(1, 11) for _ in range(1, 11)]
                >>> a.plot(array)
                <vcs.displayplot.Dp ...>
                >>> a.svg('example') # Overwrite a postscript file
                >>> a.svg('example', width=11.5, height= 8.5) # US Legal
                >>> a.svg('example', width=21, height=29.7, units='cm') # A4

        %s
        %s
        %s
        %s

        :param textAsPaths: Specifies whether to render text objects as paths.
        :type textAsPaths: bool
        """
        if units not in [
                'inches', 'in', 'cm', 'mm', 'pixel', 'pixels', 'dot', 'dots']:
            raise Exception(
                "units must be on of inches, in, cm, mm, pixel(s) or dot(s)")

        W, H = self._compute_width_height(
            width, height, units, background=True)

        if not file.split('.')[-1].lower() in ['svg']:
            file += '.svg'
        return self.backend.svg(file, width=W, height=H, units=units, textAsPaths=textAsPaths)
    svg.__doc__ = svg.__doc__ % (xmldocs.output_file, xmldocs.output_width, xmldocs.output_height, xmldocs.output_units)

    def _compute_margins(
            self, W, H, top_margin, bottom_margin, right_margin, left_margin, dpi):
        try:
            ci = self.canvasinfo()
            height = ci['height']
            width = ci['width']
            factor = 1. / 72
            size = float(width) / float(height)
        except Exception:
            factor = 1.
            if self.size is None:
                size = 1.2941176470588236
            else:
                size = self.size
        if bottom_margin is not None:
            bottom_margin = bottom_margin * factor
        if left_margin is not None:
            left_margin = left_margin * factor
        if right_margin is not None:
            right_margin = right_margin * factor
        if top_margin is not None:
            top_margin = top_margin * factor

        # now for sure factor is 1.
        factor = 1.
        if left_margin is None and right_margin is None and top_margin is None and bottom_margin is None:
            # default margins
            left_margin = .25
            right_margin = .25
            top_margin = .25
            twidth = W - (left_margin + right_margin) * dpi
            bottom_margin = (H - twidth / size) / dpi - top_margin
            bottom_margin = (top_margin + bottom_margin) / 2.
            top_margin = bottom_margin
        # bottom_defined
        elif left_margin is None and right_margin is None and top_margin is None:
            left_margin = .25
            right_margin = .25
            twidth = W - (left_margin + right_margin) * dpi
            top_margin = (H - twidth / size) / dpi - bottom_margin
        # top_defined
        elif left_margin is None and right_margin is None and bottom_margin is None:
            left_margin = .25
            right_margin = .25
            twidth = W - (left_margin + right_margin) * dpi
            bottom_margin = (H) / dpi - top_margin
        # right defined
        elif top_margin is None and bottom_margin is None and left_margin is None:
            left_margin = .25
            top_margin = .25
            twidth = W - (left_margin + right_margin) * dpi
            bottom_margin = (H - twidth / size) / dpi - top_margin
        # left defined
        elif top_margin is None and bottom_margin is None and right_margin is None:
            right_margin = .25
            top_margin = .25
            twidth = W - (left_margin + right_margin) * dpi
            bottom_margin = (H - twidth / size) / dpi - top_margin
        # left defined and bottom
        elif top_margin is None and right_margin is None:
            right_margin = .25
            twidth = W - (left_margin + right_margin) * dpi
            top_margin = (H - twidth / size) / dpi - bottom_margin
        # right defined and bottom
        elif top_margin is None and left_margin is None:
            left_margin = .25
            twidth = W - (left_margin + right_margin) * dpi
            top_margin = (H - twidth / size) / dpi - bottom_margin
        # right defined and top
        elif bottom_margin is None and left_margin is None:
            left_margin = .25
            twidth = W - (left_margin + right_margin) * dpi
            bottom_margin = (H - twidth / size) / dpi - top_margin
        # left defined and top
        elif bottom_margin is None and right_margin is None:
            right_margin = .25
            twidth = W - (left_margin + right_margin) * dpi
            bottom_margin = (H - twidth / size) / dpi - top_margin
        # all but bottom
        elif bottom_margin is None:
            twidth = W - (left_margin + right_margin) * dpi
            bottom_margin = (H - twidth / size) / dpi - top_margin
        # all but top
        elif top_margin is None:
            twidth = W - (left_margin + right_margin) * dpi
            top_margin = (H - twidth / size) / dpi - bottom_margin
        # all but right
        elif right_margin is None:
            theight = H - (top_margin + bottom_margin) * dpi
            right_margin = (W - theight * size) / dpi + left_margin
        # all but left
        elif left_margin is None:
            theight = H - (top_margin + bottom_margin) * dpi
            left_margin = (W - theight * size) / dpi + right_margin

        return top_margin, bottom_margin, right_margin, left_margin

    def isopened(self):
        """Returns a boolean value indicating whether the canvas is opened or not.

        :Example:

            .. doctest:: convas_isopened

                >>> a=vcs.init()
                >>> a.isopened() # canvas defaults to being closed
                False
                >>> array=[range(10) for _ in range(10)]
                >>> a.plot(array)
                <vcs.displayplot.Dp object at 0x...>
                >>> a.isopened() # plotting opened the canvas
                True

        :returns: A boolean value indicating whether the Canvas is opened (1), or closed (0)
        :rtype: bool
        """
        return self.backend.isopened()

    def _compute_width_height(self, width, height, units, ps=False, background=False):
        dpi = 72.  # dot per inches
        if units in ["in", "inches"]:
            factor = 1.
        elif units == 'cm':
            factor = 0.393700787
        elif units == 'mm':
            factor = 0.0393700787
        else:
            factor = 1. / 72
        sfactor = factor
        if width is None and height is None:
            if self.isopened() and not background:
                try:
                    ci = self.canvasinfo()
                    height = ci['height']
                    width = ci['width']
                    sfactor = 1. / 72.
                    if ps is True:
                        ratio = width / float(height)
                        if self.size == 1.4142857142857141:
                            # A4 output
                            width = 29.7
                            sfactor = 0.393700787
                            height = 21.
                        elif self.size == 1. / 1.4142857142857141:
                            width = 21.
                            sfactor = 0.393700787
                            height = 29.7
                        else:
                            sfactor = 1.
                            if ratio > 1:
                                width = 11.
                                height = width / ratio
                            else:
                                height = 11.
                                width = height * ratio
                except Exception:  # canvas never opened
                    if self.size is None:
                        sfactor = 1.
                        height = 8.5
                        width = 11.
                    elif self.size == 1.4142857142857141:
                        sfactor = 0.393700787
                        width = 29.7
                        height = 21.
                    else:
                        sfactor = 1.
                        height = 8.5
                        width = self.size * height
            else:
                width = self.width
                height = self.height
        elif width is None:
            if self.size is None:
                width = 1.2941176470588236 * height
            else:
                width = self.size * height
        elif height is None:
            if self.size is None:
                height = width / 1.2941176470588236
            else:
                height = width / self.size
        W = int(width * dpi * sfactor)
        H = int(height * dpi * sfactor)
        if (self.isportrait() and W > H) \
                or (self.islandscape() and H > W):
            tmp = W
            W = H
            H = tmp
        return W, H

    def postscript(self, file, mode='r', orientation=None, width=None, height=None, units='inches', textAsPaths=True):
        """Postscript output is another form of vector graphics. It is larger than its CGM output
        counter part, because it is stored out in ASCII format.

        There are two modes for saving a postscript file: 'Append' (a) mode appends postscript
        output to an existing postscript file; and 'Replace' (r) mode overwrites an existing
        postscript file with new postscript output. The default mode is to overwrite an existing
        postscript file.

        .. note::

            The textAsPaths parameter preserves custom fonts, but text can no
            longer be edited in the file

        :Example:

            .. doctest:: canvas_postscript

                >>> a=vcs.init()
                >>> array = [range(1, 11) for _ in range(1, 11)]
                >>> a.plot(array)
                <vcs.displayplot.Dp ...>
                >>> a.postscript('example') # Overwrite a postscript file
                >>> a.postscript('example', 'a') # Append postscript to an existing file
                >>> a.postscript('example', 'r') # Overwrite an existing file
                >>> a.postscript('example', mode='a') # Append postscript to an existing file
                >>> a.postscript('example', width=11.5, height= 8.5) # US Legal (default)
                >>> a.postscript('example', width=21, height=29.7, units='cm') # A4

        %s
        :param mode: The mode in which to open the file. One of 'r' or 'a'.
            When mode is 'r', file will be opened in replace mode.
            When mode is 'a', file will be opened in append mode.
        :type mode: `str`_

        %s
        %s
        %s

        :param textAsPaths: Specifies whether to render text objects as paths.
        :type textAsPaths: bool
        """
        if units not in [
                'inches', 'in', 'cm', 'mm', 'pixel', 'pixels', 'dot', 'dots']:
            raise Exception(
                "units must be on of inches, in, cm, mm, pixel(s) or dot(s)")

        # figures out width/height
        W, H = self._compute_width_height(
            width, height, units, ps=True, background=True)

        # orientation keyword is useless left for backward compatibility
        if not file.split('.')[-1].lower() in ['ps', 'eps']:
            file += '.ps'
        if mode == 'r':
            return self.backend.postscript(file, W, H, units="pixels", textAsPaths=textAsPaths)
        else:
            n = random.randint(0, 10000000000000)
            psnm = '/tmp/' + '__VCS__tmp__' + str(n) + '.ps'
            self.backend.postscript(psnm, W, H, units="pixels")
            if os.path.exists(file):
                f = open(file, 'r+')
                f.seek(0, 2)  # goes to end of file
                f2 = open(psnm)
                f.writelines(f2.readlines())
                f2.close()
                f.close()
                os.remove(psnm)
            else:
                shutil.move(psnm, file)
    postscript.__doc__ = postscript.__doc__ % (xmldocs.output_file, xmldocs.output_width, xmldocs.output_height,
                                               xmldocs.output_units)

    def _scriptrun(self, *args):
        return vcs._scriptrun(*args)

    def scriptrun(self, aFile, *args, **kargs):
        """
        Given the path to a script containing a VCS object, scriptrun
        runs that script to build the object.

        :Example:

            .. doctest:: canvas_scriptrun

                >>> b=vcs.createboxfill('new_box')
                >>> b.script('new_box') # json representation of 'new_box'
                >>> bfs=vcs.listelements('boxfill') # list all boxfills
                >>> i=bfs.index('new_box')
                >>> bfs[i] # shows 'new_box' exists
                'new_box'
                >>> vcs.removeobject(b) # remove new_box
                'Removed boxfill object new_box'
                >>> bfs=vcs.listelements('boxfill') # list all boxfills
                >>> try:
                ...     bfs.index('new_box')
                ... except Exception:
                ...     print ("boxfill 'new_box' doesn't exist")
                boxfill 'new_box' doesn't exist
                >>> vcs.scriptrun('new_box.json') # re-creates 'new_box'
                >>> bfs=vcs.listelements('boxfill') # list all boxfills
                >>> i=bfs.index('new_box')
                >>> bfs[i]  # shows 'new_box' exists (again)
                'new_box'

        :param aFile: String representing the path to a the script.
        :type aFile: str
        """
        vcs.scriptrun(aFile, *args, **kargs)

    def setcolormap(self, name):
        """It is necessary to change the colormap. This routine will change the VCS
        color map.

        If the the visual display is 16-bit, 24-bit, or 32-bit TrueColor, then a redrawing
        of the VCS Canvas is made every time the colormap is changed.

        :Example:

            .. doctest:: canvas_setcolormap

                >>> a=vcs.init()
                >>> array = [range(1, 11) for _ in range(1, 11)]
                >>> a.plot(array,'default','isofill','quick')
                <vcs.displayplot.Dp ...>
                >>> a.setcolormap("AMIP")
                >>> a.plot(array,'default','isofill','quick')
                <vcs.displayplot.Dp ...>

        :param name: Name of the colormap to use
        :type name: `str`_
        """
        # Don't update the VCS segment if there is no Canvas. This condition
        # happens in the initalize function for VCDAT only. This will cause a
        # core dump is not checked.
        # try:
        #   updateVCSsegments_flag = args[1]
        # except Exception:
        #   updateVCSsegments_flag = 1

        self.colormap = name
        self.update()
        return

    def setcolorcell(self, *args):
        """Set a individual color cell in the active colormap. If default is
        the active colormap, then return an error string.

        If the the visul display is 16-bit, 24-bit, or 32-bit TrueColor, then a redrawing
        of the VCS Canvas is made evertime the color cell is changed.

        Note, the user can only change color cells 0 through 239 and R,G,B
        value must range from 0 to 100. Where 0 represents no color intensity
        and 100 is the greatest color intensity.

        :Example:

            .. doctest:: canvas_setcolorcell

                >>> a=vcs.init()
                >>> array = [range(1, 11) for _ in range(1, 11)]
                >>> a.plot(array,'default','isofill','quick')
                <vcs.displayplot.Dp ...>
                >>> a.setcolormap("AMIP")
                >>> a.setcolorcell(11,0,0,0)
                >>> a.setcolorcell(21,100,0,0)
                >>> a.setcolorcell(31,0,100,0)
                >>> a.setcolorcell(41,0,0,100)
                >>> a.setcolorcell(51,100,100,100)
                >>> a.setcolorcell(61,70,70,70)
                >>> a.plot(array,'default','isofill','quick')
                <vcs.displayplot.Dp ...>
        """
        a = vcs.setcolorcell(self.colormap, *args)
        return a

    def setcontinentsline(self, line="default"):
        """One has the option of configuring the appearance of the lines used to
        draw continents by providing a VCS Line object.

        :Example:

            .. doctest:: canvas_setcontinentsline

                >>> a = vcs.init()
                >>> line = vcs.createline()
                >>> line.width = 5
                >>> a.setcontinentsline(line) # Use custom continents line
                >>> a.setcontinentsline("default") # Use default line

        :param line: Line to use for drawing continents. Can be a string name of a line, or a VCS line object
        :type line: `str`_ or :py:class:`vcs.line.Tl`
        """
        linename = VCS_validation_functions.checkLine(self, "continentsline", line)
        line = vcs.getline(linename)
        self._continents_line = line

    def getcontinentsline(self):
        """Returns the continents line associated with the canvas.

        :Example:

            .. doctest:: canvas_getcontinentsline

                >>> a=vcs.init()
                >>> cl=a.getcontinentsline() # should be the default
                >>> cl.name
                'default'

        :return: The line object associated with the canvas's continents_line
            property
        :rtype: vcs.line.Tl
        """
        if self._continents_line is None:
            return vcs.getline("default")
        else:
            return self._continents_line

    def setcontinentstype(self, value):
        """One has the option of using continental maps that are predefined or that
        are user-defined. Predefined continental maps are either internal to VCS
        or are specified by external files. User-defined continental maps are
        specified by additional external files that must be read as input.

        The continents-type values are integers ranging from 0 to 11, where:

            * 0 signifies "No Continents"

            * 1 signifies "Fine Continents"

            * 2 signifies "Coarse Continents"

            * 3 signifies "United States" (with "Fine Continents")

            * 4 signifies "Political Borders" (with "Fine Continents")

            * 5 signifies "Rivers" (with "Fine Continents")

            * 6 uses a custom continent set

        You can also pass a file by path.

        :Example:

            .. doctest:: canvas_setcontinentstype

                >>> a=vcs.init()
                >>> a.setcontinentstype(4) # "Political Borders"
                >>> import cdms2 # We need cdms2 to create a slab
                >>> f = cdms2.open(vcs.sample_data+'/clt.nc') # open data file
                >>> v = f('v') # use the data file to create a slab
                >>> a.plot(v,'default','isofill','quick') # map with borders
                <vcs.displayplot.Dp ...>

        :param value: Integer representing continent type, as specified in function description
        :type value: `int`_
        """
        continent_path = VCS_validation_functions.checkContinents(self, value)
        self._continents = value
        if continent_path is not None and not os.path.exists(
                continent_path):
            warnings.warn(
                "Continents file not found: %s, substituing with fine continents" %
                continent_path)
            self._continents = 1
            return

    def _continentspath(self):
        try:
            path = VCS_validation_functions.checkContinents(self, self._continents)
            if path is None and self._continents != 0:
                return VCS_validation_functions.checkContinents(self, 1)
            else:
                return path
        except Exception:
            return VCS_validation_functions.checkContinents(self, 1)

    def gif(self, filename='noname.gif', merge='r', orientation=None,
            geometry='1600x1200'):
        """In some cases, the user may want to save the plot out as a gif image. This
        routine allows the user to save the VCS canvas output as a SUN gif file.
        This file can be converted to other gif formats with the aid of xv and other
        such imaging tools found freely on the web.

        By default, the page orientation is in Landscape mode (l). To translate the page
        orientation to portrait mode (p), set the orientation = 'p'.

        The GIF command is used to create or append to a gif file. There are two modes
        for saving a gif file: 'Append' mode (a) appends gif output to an existing gif
        file; 'Replace' (r) mode overwrites an existing gif file with new gif output.
        The default mode is to overwrite an existing gif file (i.e. mode (r)).

        .. attention::

            This function does not currently work.
            It will be implemented in the future.

        .. pragma: skip-doctest REMOVE WHEN IT WORKS AGAIN!
        """
        if orientation is None:
            orientation = self.orientation()[0]
        g = geometry.split('x')
        f1 = f1 = float(g[0]) / 1100.0 * 100.0
        f2 = f2 = float(g[1]) / 849.85 * 100.0
        geometry = "%4.1fx%4.1f" % (f2, f1)
        nargs = ('gif', filename, merge, orientation, geometry)
        return self.backend.gif(nargs)

    def gs(self, filename='noname.gs', device='png256',
           orientation=None, resolution='792x612'):

        warnings.warn("Export to GhostScript is no longer supported", vcs.VCSDeprecationWarning)

    def eps(self, file, mode='r', orientation=None, width=None, height=None, units='inches', textAsPaths=True):
        """In some cases, the user may want to save the plot out as an Encapsulated
        PostScript image. This routine allows the user to save the VCS canvas output
        as an Encapsulated PostScript file.
        This file can be converted to other image formats with the aid of xv and other
        such imaging tools found freely on the web.

        :Example:

            .. doctest:: canvas_eps

                >>> a=vcs.init()
                >>> array = [range(10) for _ in range(10)]
                >>> a.plot(array)
                <vcs.displayplot.Dp ...>
                >>> a.postscript('example') # Overwrite a postscript file
                >>> a.postscript('example', 'a') # Append postscript to an existing file
                >>> a.postscript('example', 'r') # Overwrite an existing file
                >>> a.postscript('example', mode='a') # Append postscript to an existing file
                >>> a.postscript('example', width=11.5, height= 8.5) # US Legal (default)
                >>> a.postscript('example', width=21, height=29.7, units='cm') # A4

        %s

        :param mode: The mode in which to open the file. One of 'r' or 'a'.
        :type mode: `str`_

        %s
        %s
        %s
        """
        ext = file.split(".")[-1]
        if ext.lower() != 'eps':
            file = file + '.eps'
        num = numpy.random.randint(100000000000)
        tmpfile = "/tmp/vcs_tmp_eps_file_%i.ps" % num
        if mode == 'a' and os.path.exists(file):
            os.rename(file, tmpfile)
        self.postscript(
            tmpfile,
            mode,
            orientation,
            width,
            height,
            units,
            textAsPaths)

        os.popen("ps2epsi %s %s" % (tmpfile, file)).readlines()
        os.remove(tmpfile)
    eps.__doc__ = eps.__doc__ % (xmldocs.output_file, xmldocs.output_width, xmldocs.output_height, xmldocs.output_units)

    def show(self, *args):
        return vcs.show(*args)
    show.__doc__ = vcs.utils.show.__doc__

    def saveinitialfile(self):
        """At start-up, VCS reads a script file named initial.attributes that
        defines the initial appearance of the VCS Interface. Although not
        required to run VCS, this initial.attributes file contains many
        predefined settings to aid the beginning user of VCS.

        :Example:

            .. code-block:: python

                a=vcs.init()
                box=vcs.createboxfill('m_box')
                line=vcs.createline('m_line')
                a.saveinitialfile() # m_line, m_box saved for future sessions

        .. warning::

            This removes first ALL objects generated automatically (i.e. whose
            name starts with '__'). To preserve these, rename objects first
            e.g.:

            .. doctest:: canvas_saveinitial_warning

                >>> b=vcs.createboxfill()
                >>> b.rename('MyBoxfill') # graphic method is now preserved
        """
        self.clean_auto_generated_objects()
        return vcs.saveinitialfile()

    def raisecanvas(self, *args):
        """Raise the VCS Canvas to the top of all open windows.

        :Example:

            .. doctest:: canvas_raisecanvas

                >>> a=vcs.init()
                >>> a.open()
                >>> a.raisecanvas() # canvas should now be at the top

        """
        return self.backend.raisecanvas(*args)

    def islandscape(self):
        """Indicates if VCS's orientation is landscape.

        Returns a 1 if orientation is landscape.
        Otherwise, it will return a 0, indicating false (not in landscape mode).

        :Example:

            .. doctest:: canvas_islandscape

                >>> a=vcs.init()
                >>> array = [range(10) for _ in range(10)]
                >>> a.plot(array)
                <vcs.displayplot.Dp ...>
                >>> if a.islandscape():
                ...     a.portrait() # Set VCS's orientation to portrait mode

        :returns: Integer indicating VCS is in landscape mode (1), or not (0)
        :rtype: `int`_
        """
        if (self.orientation() == 'landscape'):
            return 1
        else:
            return 0

    def isportrait(self):
        """Indicates if VCS's orientation is portrait.


        :Example:

            .. doctest:: canvas_isportrait

                >>> a=vcs.init()
                >>> array = [range(10) for _ in range(10)]
                >>> a.plot(array)
                <vcs.displayplot.Dp ...>
                >>> if a.isportrait():
                ...     a.landscape() # Set VCS's orientation to landscape mode

        :returns: Returns a 1 if orientation is portrait, or 0 if not in portrait mode
        :rtype: bool
        """
        if (self.orientation() == 'portrait'):
            return 1
        else:
            return 0

    def getplot(self, Dp_name_src='default', template=None):
        """This function will create a display plot object from an existing display
        plot object from an existing VCS plot. If no display plot name
        is given, then None is returned.


        :param Dp_name_src: String name of an existing display plot object
        :type Dp_name_src: `str`_

        :param template: The displayplot template to inherit from
        :type template:

        :returns: A VCS displayplot object
        :rtype: vcs.displayplot.Dp

        .. attention::

            This function does not currently work.
            It will be implemented in the future.

        .. pragma: skip-doctest REMOVE WHEN IT WORKS AGAIN!
        """
        if not isinstance(Dp_name_src, str):
            raise ValueError('Error -  The argument must be a string.')

        Dp_name = None
        display = displayplot.Dp(self, Dp_name, Dp_name_src, 1)
        if template is not None:
            display._template_origin = template
        return display

    def createcolormap(self, Cp_name=None, Cp_name_src='default'):
        return vcs.createcolormap(Cp_name, Cp_name_src)
    createcolormap.__doc__ = vcs.manageElements.createcolormap.__doc__

    def getcolormap(self, Cp_name_src='default'):
        return vcs.getcolormap(Cp_name_src)
    getcolormap.__doc__ = vcs.manageElements.getcolormap.__doc__

    def addfont(self, path, name=""):
        """Add a font to VCS.

        :param path: Path to the font file you wish to add (must be .ttf)
        :type path: `str`_

        :param name: Name to use to represent the font.
        :type name: `str`_

        .. pragma: skip-doctest If you can reliably test it, please do.
        """
        if not os.path.exists(path):
            raise ValueError('Error -  The font path does not exists')
        if os.path.isdir(path):
            dir_files = []
            files = []
            if name == "":
                subfiles = os.listdir(path)
                for file in subfiles:
                    dir_files.append(os.path.join(path, file))
            elif name == 'r':
                for root, dirs, subfiles in os.walk(path):
                    for file in subfiles:
                        dir_files.append(os.path.join(root, file))
            for f in dir_files:
                if f.lower()[-3:]in ['ttf', 'pfa', 'pfb']:
                    files.append([f, ""])
        else:
            files = [[path, name], ]

        nms = []
        for f in files:
            fnm, name = f
            i = max(vcs.elements["fontNumber"].keys()) + 1
            vcs.elements["font"][name] = fnm
            vcs.elements["fontNumber"][i] = name
        if len(nms) == 0:
            raise vcsError('No font Loaded')
        elif len(nms) > 1:
            return nms
        else:
            return nms[0]

    def getfontnumber(self, name):
        return vcs.getfontnumber(name)
    getfontnumber.__doc__ = vcs.utils.getfontnumber.__doc__

    def getfontname(self, number):
        return vcs.getfontname(number)
    getfontname.__doc__ = vcs.utils.getfontname.__doc__

    def getfont(self, font):
        """Get the font name/number associated with a font number/name

        :Example:

            .. doctest:: canvas_getfont

                >>> a=vcs.init()
                >>> font_names=[]
                >>> for i in range(1,17):
                ...     font_names.append(str(a.getfont(i))) # font_names is now filled with all font names
                >>> font_names
                ['default', ...]
                >>> font_numbers = []
                >>> for name in font_names:
                ...     font_numbers.append(a.getfont(name)) # font_numbers is now filled with all font numbers
                >>> font_numbers
                [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]

        :param font: The font name/number
        :type font: `int`_ or `str`_

        :returns: If font parameter was a string, will return the integer
            associated with that string.
            If font parameter was an integer, will return the string
            associated with that integer.
        :rtype: `int`_ or str
        """
        if isinstance(font, int):
            return self.getfontname(font)
        elif isinstance(font, str):
            return self.getfontnumber(font)
        else:
            raise vcsError("Error you must pass a string or int")

    def switchfonts(self, font1, font2):
        """Switch the font numbers of two fonts.

        :Example:

            .. doctest:: canvas_switchfonts

                >>> a=vcs.init()
                >>> maths1 = a.getfontnumber('Maths1') # store font number
                >>> maths2 = a.getfontnumber('Maths2') # store font number
                >>> a.switchfonts('Maths1','Maths2') # switch font numbers
                >>> new_maths1 = a.getfontnumber('Maths1')
                >>> new_maths2 = a.getfontnumber('Maths2')
                >>> maths1 == new_maths2 and maths2 == new_maths1 # check
                True

        :param font1: The first font
        :type font1: `int`_ or str

        :param font2: The second font
        :type font2: `int`_ or str
        """
        if isinstance(font1, str):
            index1 = self.getfont(font1)
        elif isinstance(font1, (int, float)):
            index1 = int(font1)
            self.getfont(index1)  # make sure font exists
        else:
            raise vcsError(
                "Error you must pass either a number or font name!, you passed for font 1: %s" %
                font1)
        if isinstance(font2, str):
            index2 = self.getfont(font2)
        elif isinstance(font2, (int, float)):
            index2 = int(font2)
            self.getfont(index2)  # make sure font exists
        else:
            raise vcsError(
                "Error you must pass either a number or font name!, you passed for font 2: %s" %
                font2)
        tmp = vcs.elements['fontNumber'][index1]
        vcs.elements['fontNumber'][index1] = vcs.elements['fontNumber'][index2]
        vcs.elements['fontNumber'][index2] = tmp

    def copyfontto(self, font1, font2):
        """Copy 'font1' into 'font2'.

        :param font1: Name/number of font to copy
        :type font1: `str`_ or int

        :param font2: Name/number of destination
        :type font2: `str`_ or `int`_

        .. attention::

            This function does not currently work.
            It will be added in the future.

        .. pragma: skip-doctest REMOVE WHEN IT WORKS AGAIN!
        """
        if isinstance(font1, str):
            index1 = self.getfont(font1)
        elif isinstance(font1, (int, float)):
            index1 = int(font1)
            self.getfont(index1)  # make sure font exists
        else:
            raise vcsError(
                "Error you must pass either a number or font name!, you passed for font 1: %s" %
                font1)
        if isinstance(font2, str):
            index2 = self.getfont(font2)
        elif isinstance(font2, (int, float)):
            index2 = int(font2)
            self.getfont(index2)  # make sure font exists
        else:
            raise vcsError(
                "Error you must pass either a number or font name!, you passed for font 2: %s" %
                font2)
        return self.canvas.copyfontto(*(index1, index2))

    def setdefaultfont(self, font):
        """Sets the passed/def show font as the default font for vcs

        :param font: Font name or index to use as default
        :type font: `str`_ or `int`_

        .. attention::

            This function does not currently work.
            It will be implemented in the future.

        .. pragma: skip-doctest REMOVE WHEN IT WORKS AGAIN!
        """
        if isinstance(font, str):
            font = self.getfont(font)
        return self.copyfontto(font, 1)

    def orientation(self, *args, **kargs):
        """Return canvas orientation.

        The current implementation does not use any args or kargs.

        :Example:

            .. doctest:: canvas_orientation

                >>> a=vcs.init()
                >>> a.orientation() # Show current orientation of the canvas
                'landscape'

        :returns: A string indicating the orientation of the canvas, i.e. 'landscape' or 'portrait'
        :rtype: `str`_
        """
        return self.backend.orientation(*args, **kargs)

    def getcolorcell(self, *args):
        return vcs.getcolorcell(args[0], self)
    getcolorcell.__doc__ = vcs.utils.getcolorcell.__doc__

    def getcolormapname(self):
        """Returns the name of the colormap this canvas is set to use by default.

        :Example:

            .. doctest:: canvas_getcolormapname

                >>> a=vcs.init()
                >>> a.show('colormap')
                *******************Colormap Names List**********************
                ...
                *******************End Colormap Names List**********************
                >>> a.setcolormap('rainbow') # set canvas's default colormap
                >>> a.getcolormapname()
                'rainbow'

        To set that colormap, use :py:func:`setcolormap`.
        """
        if self.colormap is None:
            return vcs._colorMap
        return self.colormap

    def dummy_user_action(self, *args, **kargs):
        """Given args and kargs, prints the arguments and keyword arguments
        associated with those parameters.

        Use this function to test what args and kargs are, if you're unsure.

        :Example:

            .. doctest:: canvas_dummy_user_action

                >>> a=vcs.init()
                >>> dua=a.dummy_user_action # alias long name
                >>> dua("falafel", 37, the_answer=42)
                Arguments: ('falafel', 37)
                Keywords: {'the_answer': 42}


        :param args: Any number of arguments, without a keyword specifier.
        :type args: any

        :param kargs: Any number of keyword arguments, associated with any
            number of data (i.e. kwd1="a string", kwd2=42).
        :type kargs: any

        """
        print('Arguments:', args)
        print('Keywords:', kargs)
        return None


def change_date_time(tv, number):
    timeaxis = tv.getTime()
    if timeaxis is not None:
        try:
            tobj = cdtime.reltime(timeaxis[number], timeaxis.units)
            cobj = tobj.tocomp(timeaxis.getCalendar())
            tv.date = '%s/%s/%s\0' % (cobj.year, cobj.month, cobj.day)
            tv.time = '%s:%s:%s\0' % (cobj.hour, cobj.minute, cobj.second)
        except Exception:  # noqa
            pass
