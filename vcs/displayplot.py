# Automatically adapted for numpy.oldnumeric Jul 06, 2007 by numeric2numpy.py

"""
# Display Plot (Dp) module
"""
###############################################################################
#                                                                             #
# Module:       Display Plot (Dp) module                                      #
#                                                                             #
# Copyright:    2000, Regents of the University of California                 #
#               This software may not be distributed to others without        #
#               permission of the author.                                     #
#                                                                             #
# Authors:      PCMDI Software Team                                           #
#               Lawrence Livermore NationalLaboratory:                        #
#               support@pcmdi.llnl.gov                                        #
#                                                                             #
# Description:  Python command wrapper for VCS's display plot object.         #
#                                                                             #
# Version:      4.0                                                           #
#                                                                             #
###############################################################################
#
#
#
from . import VCS_validation_functions
import vcs
import tempfile
from .xmldocs import listdoc  # noqa
from functools import partial

try:
    import IPython.display
    HAVE_IPY = True
    try:
        import sidecar
        HAVE_SIDECAR = True
    except Exception:
        HAVE_SIDECAR = False
    try:
        import ipywidgets
        HAVE_IPYWIDGETS = True
    except Exception:  # no widgets
        HAVE_IPYWIDGETS = False
except Exception:  # no IPython
    HAVE_IPY = False
    HAVE_SIDECAR = False
    HAVE_IPYWIDGETS = False


try:
    basestring  # noqa
except Exception:
    basestring = str


def get_update_array_kw(disp, array, widgets, debug_target=None):
    if array is None:
        return {}
    if debug_target is not None:
        with debug_target:
            print("ok looking at kewwords for", array.id)
    kw = {}
    for ax in array.getAxisList():
        if debug_target is not None:
            with debug_target:
                print("ok ", ax.id)
        for widget in widgets:
            slider = widget.children[0]
            if debug_target is not None:
                with debug_target:
                    print("\tvs", slider.description)
            if ax.id == slider.description:
                kw[ax.id] = slice(slider.value, slider.value + 1)
    if debug_target is not None:
        with debug_target:
            print("ok we should update", array.id, "with", kw)
    return kw


class Dp(vcs.bestMatch):

    """
    The Display plot object allows the manipulation of the plot name, off,
    priority, template, graphics type, graphics name, and data array(s).

    This class is used to define a display plot table entry used in VCS, or it
    can be used to change some or all of the display plot attributes in an
    existing display plot table entry.

    .. describe:: Useful Functions:

        .. code-block:: python

            # Canvas constructor
            a=vcs.init()
            # Show display plot objects
            a.show('plot')
            # Updates the VCS Canvas at user's request
            a.update()

    .. describe:: General display plot usage:

        .. code-block:: python

            #Create a VCS Canvas object
            a=vcs.init()
            #To Create a new instance of plot:
            # Create a plot object
            p1=a.plot(s)
            #To Modify an existing plot in use:
            p1=a.getplot('dpy_plot_1')

    .. describe:: Display plot object attributes:

        .. code-block:: python

            # Will list all the display plot attributes
            p1.list()
            # "On" or "Off" status, 1=on, 0=off
            p1.off=1
            # Priority to place plot in front of other objects
            p1.priority=1
            # Name of template object
            p1.template='quick'
            # Graphics method type
            p1.g_type='boxfill'
            # Graphics method name
            p1.g_name='quick'
            # List of all the array names
            p1.array=['a1']

    .. pragma: skip-doctest
    """
    __slots__ = ["_name",
                 "s_name",
                 "_parent",
                 "_off",
                 "_priority",
                 "_template",
                 "__template_origin",
                 "_Dp__template_origin",
                 "_g_type",
                 "_g_name",
                 "_array",
                 "_continents",
                 "_continents_line",
                 "_backend",
                 "_newelements",
                 "_widget",
                 "extradisplays",
                 "ratio",
                 "_display_target"
                 ]

    def handle_slider_change(self, change, widgets, name):
        if not HAVE_IPYWIDGETS:  # No need to go further
            return
        if self._parent._display_target_out is None:
            debug = False
        else:
            debug = True
        if debug:
            with self._parent._display_target_out:
                print("ok updating slider nasmed", name, "with", change["new"])
        for disp_name in self._parent.display_names:
            disp = vcs.elements["display"][disp_name]
            if debug:
                with self._parent._display_target_out:
                    print("ok looking at arrays", disp.array)
            if disp.array[0] is None:
                continue
            if name not in disp.array[0].getAxisIds():
                if debug:
                    with self._parent._display_target_out:
                        print("skipping array:", disp.array)
                continue
            if debug:
                debug_target = self._parent._display_target_out
            else:
                debug_target = None
            kw1 = get_update_array_kw(disp, disp.array[0], widgets, debug_target)
            kw2 = get_update_array_kw(disp, disp.array[1], widgets, debug_target)
            # Ok in some case (u/v e.g) same dims but different name on 2nd array
            if disp.array[1] is not None:
                for axId in kw1:
                    if axId not in kw2:  # probably should be there as wll
                        ax = disp.array[0].getAxis(disp.array[0].getAxisIndex(axId))
                        if debug:
                            with self._parent._display_target_out:
                                print("Examing axis:", axId, "vs", ax, hasattr(ax, "axis"))
                        if hasattr(ax, "axis"):  # special dim (T,Z,Y,X)
                            if debug:
                                with self._parent._display_target_out:
                                    print("Examing axis:", axId, "vs", ax.axis)
                            for ax2 in disp.array[1].getAxisList():
                                if debug:
                                    with self._parent._display_target_out:
                                        print("Examing axis:", axId, "vs", ax2.id)
                                if hasattr(ax2, "axis") and ax2.axis == ax.axis:
                                    kw2[ax2.id] = kw1[ax.id]
            if debug:
                with self._parent._display_target_out:
                    print("kws", kw1, kw2)
            if len(kw1) != 0:
                if debug:
                    with self._parent._display_target_out:
                        print("updating :", disp.array[0].id, kw1)
                new1 = disp.array[0](**kw1)
                if debug:
                    with self._parent._display_target_out:
                        print("updated :", new1.shape)
            else:
                new1 = disp.array[0]
            if len(kw2) != 0:
                if debug:
                    with self._parent._display_target_out:
                        print("updating 2:", kw2)
                new2 = disp.array[1](**kw2)
                if debug:
                    with self._parent._display_target_out:
                        print("updated 2:", new2.shape)
            else:
                if debug:
                    with self._parent._display_target_out:
                        print("not updating 2:", disp.array[1])
                new2 = disp.array[1]
            if kw1 is not {} or kw2 is not {}:
                if debug:
                    with self._parent._display_target_out:
                        print("calling update")
                disp._parent.backend.update_input(disp.backend, new1, new2)
        for widget in widgets:
            slider, label = widget.children
            sp = slider.description
            if debug:
                with self._parent._display_target_out:
                    print("OPk looking at:", name, slider.description, sp, sp == name)
            if sp == name:
                value = label.values[change["new"]]
                label.value = "{}".format(value)
                if debug:
                    with self._parent._display_target_out:
                        print("Ok new value:", value, label.value)
        if debug:
            with self._parent._display_target_out:
                print("Ok about to dump png")
        tmp = tempfile.mktemp() + ".png"
        self._parent.png(tmp)
        f = open(tmp, "rb")
        st = f.read()
        f.close()
        if debug:
            IPython.display.display(self._parent._display_target_out)
        IPython.display.display(*widgets)
        self._parent._display_target_image.value = st
        if debug:
            with self._parent._display_target_out:
                print("Ok update")

    def generate_sliders(self, debug):
        dimensions = set()
        funcs = []
        widgets = []
        for disp_name in self._parent.display_names:
            disp = vcs.elements["display"][disp_name]
            gm_info = vcs.graphicsmethodinfo(vcs.getgraphicsmethod(disp.g_type, disp.g_name))
            data = disp.array[0]
            if data is None:
                continue
            for dim in data.getAxisList()[:-gm_info["dimensions_used_on_plot"]]:
                units = getattr(dim, "units", None)
                if (dim.id, units, dim[0], dim[-1]) not in dimensions:
                    if dim.isTime():
                        values = dim.asComponentTime()
                    else:
                        values = ["{}{}".format(value, units) for value in dim[:]]
                    slider = ipywidgets.IntSlider(
                        value=0,
                        min=0,
                        max=len(dim)-1,
                        step=1,
                        description='{}'.format(dim.id),
                        disabled=False,
                        continuous_update=False,
                        orientation='horizontal',
                        readout=True,
                        readout_format='d'
                    )
                    label = ipywidgets.Label(str(values[0]))
                    label.values = values
                    box = ipywidgets.HBox([slider, label])
                    widgets.append(box)
                    funcs.append(partial(self.handle_slider_change, name=dim.id))
                dimensions.add((dim.id, units, dim[0], dim[-1]))
        for i, wdgt in enumerate(widgets):
            slider = wdgt.children[0]
            slider.observe(partial(funcs[i], widgets=widgets), names="value")
        if debug:
            IPython.display.display(self._parent._display_target_out)
        return widgets

    def _repr_png_(self):
        st = None
        debug = False
        if not HAVE_IPYWIDGETS:
            debug = False
        if HAVE_IPY:
            if HAVE_SIDECAR:
                if self._parent._display_target is None:  # no target specified
                    self._parent._display_target = sidecar.Sidecar(
                        title="VCS Canvas {:d}".format(self._parent.canvasid()))
                elif isinstance(self._parent._display_target, basestring) and \
                        self._parent._display_target.lower() not in ["inline", "off", "no"]:
                    self._parent._display_target = sidecar.Sidecar(
                        title=self._parent._display_target)
            self._parent._display_target_image = ipywidgets.Image()
            if HAVE_IPYWIDGETS:
                if debug:
                    self._parent._display_target_out = ipywidgets.Output(layout={'border': '1px solid black'})
                else:
                    self._parent._display_target_out = None
                widgets = self.generate_sliders(debug)
                vbox = ipywidgets.VBox(widgets + [self._parent._display_target_image])
                if HAVE_SIDECAR:
                    with self._parent._display_target:
                        IPython.display.clear_output()
                        IPython.display.display(vbox)
                else:
                    IPython.display.clear_output()
                    IPython.display.display(vbox)
            else:
                IPython.display.clear_output()
            tmp = tempfile.mktemp() + ".png"
            self._parent.png(tmp)
            f = open(tmp, "rb")
            st = f.read()
            f.close()
            self._parent._display_target_image.value = st
            return None
        tmp = tempfile.mktemp() + ".png"
        self._parent.png(tmp)
        f = open(tmp, "rb")
        st = f.read()
        f.close()
        return st
# TODO: html,json,jpeg,png,svg,latex

    def _getname(self):
        return self._name

    def _setname(self, value):
        value = VCS_validation_functions.checkname(self, 'name', value)
        if value is not None:
            self._name = value
    name = property(_getname, _setname)

    def _setnewelements(self, value):
        if not isinstance(value, dict):
            raise ValueError("newelements attribute must be a dictionary")
        self._newelements = value

    def _getnewelements(self):
        return self._newelements
    newelements = property(_getnewelements, _setnewelements)

    def _getcontinents(self):
        return self._continents

    def _setcontinents(self, value):
        VCS_validation_functions.checkContinents(
            self,
            value)
        self._continents = value
    continents = property(_getcontinents, _setcontinents)

    def _getcontinents_line(self):
        return self._continents_line

    def _setcontinents_line(self, value):
        self._continents_line = VCS_validation_functions.checkLine(
            self, "continents_line", value)
    continents_line = property(_getcontinents_line, _setcontinents_line)

    def _getpriority(self):
        return self._priority

    def _setpriority(self, value):
        self._priority = VCS_validation_functions.checkInt(
            self,
            'priority',
            value,
            minvalue=0)
    priority = property(_getpriority, _setpriority)

    def _getoff(self):
        return self._off

    def _setoff(self, value):
        self._off = VCS_validation_functions.checkInt(
            self,
            'off',
            value,
            minvalue=0,
            maxvalue=1)
        for d in self.extradisplays:
            d.off = self._off
    off = property(_getoff, _setoff)

    def _getg_name(self):
        return self._g_name

    def _setg_name(self, value):
        self._g_name = VCS_validation_functions.checkString(
            self,
            'g_name',
            value)
    g_name = property(_getg_name, _setg_name)

    def _getarray(self):
        return self._array

    def _setarray(self, value):
        if not isinstance(value, list):
            raise ValueError('The array must be contained in a list object.')
        self._array = value
    array = property(_getarray, _setarray)

    def _gettemplate(self):
        return self._template

    def _settemplate(self, value):
        self._template = VCS_validation_functions.checkString(
            self,
            'template',
            value)
    template = property(_gettemplate, _settemplate)

    def _gettemplate_origin(self):
        return self.__template_origin

    def _settemplate_origin(self, value):
        self.__template_origin = VCS_validation_functions.checkString(
            self,
            '_template_origin',
            value)
    _template_origin = property(_gettemplate_origin, _settemplate_origin)

    def _getg_type(self):
        return self._g_type

    def _setg_type(self, value):
        try:
            hasVCSAddons = True
            import vcsaddons
        except Exception:
            hasVCSAddons = False
        value = VCS_validation_functions.checkString(self, 'g_type', value)
        value = value.lower()
        if value not in vcs.elements and value != "text" and (hasVCSAddons and value not in vcsaddons.gms):
            raise ValueError(
                "invalid g_type '%s' must be one of: %s " %
                (value, list(vcs.elements.keys())))
        self._g_type = value
    g_type = property(_getg_type, _setg_type)

    def _get_backend(self):
        return self._backend

    def _set_backend(self, value):
        if not isinstance(value, (dict, None)):
            raise Exception(
                "The dispaly backend attribute must be a dictionary or None")
        self._backend = value
    backend = property(
        _get_backend,
        _set_backend,
        None,
        "dictionary of things the backend wants to be able to reuse")

    ##########################################################################
    #                                                                           #
    # Initialize the display plot attributes.                                   #
    #                                                                           #
    ##########################################################################
    def __init__(self, Dp_name, Dp_name_src='default', parent=None):
        #                                                                           #
        ###################################################################
        # Initialize the display plot's class and its members                       #
        # The getDpmember function retrieves the values of the                      #
        # display plot members in the C structure and passes back the               #
        # appropriate Python Object.                                                #
        ###################################################################
        #                                                                           #
        self.extradisplays = []
        self._name = Dp_name
        self.s_name = 'Dp'
        self._parent = parent
        self._widget = None
        if self._name == "default":
            self._off = 0
            self._priority = 0
            self._template = "default"
            self.__template_origin = "default"
            self._g_type = "boxfill"
            self._g_name = "default"
            self._array = []
            self._continents = 1
            self._continents_line = "default"
            self.ratio = None
        else:
            src = vcs.elements["display"][Dp_name_src]
            self.off = src.off
            self.array = src.array
            self.template = src.template
            self._template_origin = src._template_origin
            self.g_type = src.g_type
            self.g_name = src.g_name
            self.continents = src.continents
            self.continents_line = src.continents_line
            self.priority = src.priority
            self.ratio = src.ratio

        vcs.elements["display"][self._name] = self
    ##########################################################################
    #                                                                           #
    # List out display plot members (attributes).                               #
    #                                                                           #
    ##########################################################################

    def list(self):
        """Lists the current values of object attributes

            :Example:

                .. doctest:: displayplot_listdoc

                    >>> a=vcs.init()
                    >>> array = [range(10) for _ in range(10)]
                    >>> obj=a.getboxfill() # default boxfill
                    >>> dsp = a.plot(obj,array) # store displayplot
                    >>> dsp.list()
                    ---------- ... ----------
                    ...
            """
        if (self.name == '__removed_from_VCS__'):
            raise ValueError('This instance has been removed from VCS.')
        print("---------- Display Plot (Dp) member (attribute) listings ----------")
        print("Display plot method =", self.s_name)
        print("name =", self.name)
        print("off =", self.off)
        print("priority =", self.priority)
        print("template =", self.template)
        print("template_origin =", self._template_origin)
        print("g_type =", self.g_type)
        print("g_name =", self.g_name)
        print("array =", self.array)
        print("continents =", self.continents)
        print("extradisplays =", self.extradisplays)
        print("ratio =", self.ratio)
