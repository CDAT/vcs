"""Utils contains functions and objects that provide VCS with useful utilities.

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
# Adapted for numpy/ma/cdms2 by convertcdms.py
from __future__ import print_function
import numpy
import cdtime
import warnings
import vcs
from . import boxfill
from . import isofill
from . import isoline
from . import taylor
from . import projection
from . import fillarea
from . import template
from . import texttable
from . import textorientation
from . import line
from . import unified1D
from . import vector
from . import marker
from . import colormap
import json
import os
import tempfile
import cdms2
import genutil
import vtk
import struct
from .clickMap import mapPng, getPngDimensions, meshToPngCoords, vcsToHtml, axisToPngCoords  # noqa
try:
    import vcsaddons
    hasVCSAddons = True
except BaseException:
    hasVCSAddons = False

try:
    long  # noqa
except Exception:
    long = int

try:
    basestring
except NameError:
    basestring = str

from .colors import rgb2str, str2rgb, matplotlib2vcs, loadmatplotlibcolormaps  # noqa

indent = 1
sort_keys = True
# Deprecated color map names mapping
vcs_deprecated_colormap_names = {
    "blue2darkred": "bl_to_darkred",
    "blue2darkorange": "bl_to_drkorang",
    "blue2grey": "blue_to_grey",
    "blue2green": "blue_to_grn",
    "blue2orange": "blue_to_orange",
    "blue2orange2red": "blue_to_orgred",
    "brown2blue": "brown_to_blue",
    "green2magenta": "grn_to_magenta",
    "lightblue2darkblue": "ltbl_to_drkbl",
    "rainbownogreen": "rainbow_no_grn",
    "white2blue": "white_to_blue",
    "white2green": "white_to_green",
    "white2magenta": "white_to_magenta",
    "white2red": "white_to_red",
    "white2yellow": "white_to_yellow",
}

defaultColorsRange = list(range(256))


def get_png_dims(fnm):
    """Given the path to a png, return width, height of the png.

    :Example:

        .. doctest:: utils_get_png_dims

            >>> a=vcs.init(bg=True)
            >>> box=vcs.getboxfill('polar')
            >>> array=[range(10) for _ in range(10)]
            >>> a.plot(box,array) # plot something on canvas
            <vcs.displayplot.Dp ...>
            >>> a.png('box.png', width=1536, height=1186) # make a png
            >>> vcs.get_png_dims('box.png') # get (width, height) of 'box.png'
            (1536, 1186)

    :param fnm: String specifying the path to a .png file
    :type fnm: `str`_

    :return: A tuple containing (width, height) of the given png.
    :rtype: `tuple`_
    """
    try:
        data = open(fnm, "rb").read()
        w, h = struct.unpack('>LL', data[16:24])
        width = int(w)
        height = int(h)
    except Exception:
        width = None
        height = None
    return width, height


class Logo(vcs.bestMatch):
    """Creates a 'logo' object

    This also to draw a logo either from a text string or a picture (png) file.
    Picture will be shrunk to fit within the canvas if it's too big to fit

    :Example:

        .. doctest:: utils_Logo

            >>> import os, sys
            >>> x=vcs.init()
            >>> x.open()
            >>> path=os.path.join(sys.prefix,"share","vcs","uvcdat.png")
            >>> logo1=vcs.utils.Logo(path)
            >>> logo1.x=.7
            >>> logo1.y=.8
            >>> logo2 = vcs.utils.Logo("My Test Logo")
            >>> logo2.x = .2
            >>> logo2.y = .2
            >>> logo1.plot(x)
            >>> logo2.plot(x)
    """

    __slots__ = [
        "x",
        "y",
        "width",
        "height",
        "source",
        "source_width",
        "source_height"]

    def __init__(self, source=None, x=.93, y=.95, width=None, height=None):
        """Initialize a new "logo" object to be plotted later on a canvas

        :param source: text string or path to png file representing the logo
        :type source: `str`_

        :param x: x position of the logo's center in fraction of canvas (0<x<1)
        :type x: `float`_

        :param y: y position of the logo's center in fraction of canvas (0<y<1)
        :type y: `float`_

        :param width: width in pixels we want the log to be
        :type width: `int`_

        :param height: height in pixels we want the log to be
        :type height: `int`_
        """
        if source is None:
            self.source = None
        elif vcs.queries.istext(source):
            self.source = source
        elif isinstance(source, basestring):
            self.source_width, self.source_height = get_png_dims(source)
            if self.source_width is not None:
                self.source = source
            else:
                self.source = vcs.createtext()
                if height is None:
                    self.source.height = 20
                else:
                    self.source.height = height
                self.source.halign = 'center'
                self.source.valign = 'half'
                # Set the texttable
                self.source.font = 2
                self.source.color = [5, 10, 67, 100.0]
                self.source.string = source
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def plot(self, canvas, bg=True):
        """Plot the logo onto a given Canvas

        :Example:

            .. doctest:: utils_Logo_plot

                >>> import os, sys
                >>> x=vcs.init()
                >>> x.open()
                >>> path=os.path.join(sys.prefix,"share/vcs/uvcdat.png")
                >>> logo1 = vcs.utils.Logo(path)
                >>> logo1.x=.7
                >>> logo1.y=.8
                >>> logo2 = vcs.utils.Logo("My Test Logo")
                >>> logo2.x = .2
                >>> logo2.y = .2
                >>> logo1.plot(x)
                >>> logo2.plot(x)


        :param canvas: Canvas onto which you desire plotting the logo
        :type canvas: vcs.Canvas.Canvas

        :param bg: do we plot in background (offscreen) mode or not? True/False
        :type bg: `bool`_
        """
        if isinstance(self.source, basestring):
            cnv_info = canvas.canvasinfo()
            if self.width is not None:
                scale = float(self.width) / self.source_width
            elif self.height is not None:
                scale = float(self.height) / self.source_height
            else:
                scale = 1.0

            xoff = cnv_info["width"] * (self.x - 0.5)
            yoff = cnv_info["height"] * (self.y - 0.5)
            canvas.put_png_on_canvas(
                self.source,
                zoom=scale,
                xOffset=xoff,
                yOffset=yoff,
                units="pixels",
                fitToHeight=False)
        elif vcs.queries.istext(self.source):
            self.source.x = [self.x]
            self.source.y = [self.y]
            if self.height is not None:
                self.source.height = self.height
            canvas.plot(self.source, bg=bg)


def process_range_from_old_scr(code, g):
    irg = code.find("range")
    if irg > -1:
        rg_code = code[irg:]
        levs = []
        fac = []
        fai = []
        fas = []
        badfa = False
        while rg_code.find("(id=") > -1:
            iend = rg_code.find(")") + 1
            line = rg_code[:iend]
            rg_code = rg_code[iend:]
            sp = line.split(",")
            levs.append([float(sp[1][7:]), float(sp[2][7:])])
            fa = sp[-1][3:]
            fa = fa[:fa.find(")")]
            if fa not in list(vcs.elements["fillarea"].keys()):
                badfa = True
                fai.append(fa)
            else:
                fa = vcs.elements["fillarea"][fa]
                fac.append(fa.color[0])
                fai.append(fa.index[0])
                fas.append(fa.style[0])
        if not numpy.allclose(levs, 1.e20):
            g.levels = levs
        if badfa:
            g._fillareaindices = fai
        else:
            g.fillareacolors = fac
            g.fillareaindices = fai
            g.fillareastyle = fas[0]


def dumpToDict(obj, skipped=[], must=[]):
    """Takes a VCS object and serializes its properties and their associated
    values in a Python `dict`_ .

    :Example:

        .. doctest:: utils_dumpToDict

            >>> b=vcs.getboxfill()
            >>> t=vcs.gettemplate()
            >>> bd=vcs.dumpToDict(b) # serializes all properties
            >>> td=vcs.dumpToDict(t, skipped=['legend']) # skip legend property
            >>> 'legend' in td[0].keys() # 'legend' should not be in dictionary
            False

    :param obj: An instance of a VCS object to serialize
    :type obj: A VCS object

    :param skipped: A list of strings, associated with property names to skip.
    :type skipped: `list`_

    :param must: A list of strings, associated with property names which must
        be captured in the serialization.
    :type must: `list`_

    :return: A tuple containing:

        * a dictionary with mappings of the object's property names
            to the values associated with those property names.

        * a dictionary with mappings of more complex properties' names
            to sets containing any associated property values.

    :rtype: `tuple`_
    """
    dic = {}
    associated = {"texttable": set(),
                  "textorientation": set(),
                  "line": set(),
                  "colormap": set(),
                  "projection": set(),
                  }
    if isinstance(obj, (vcs.taylor.TDMarker, vcs.taylor.Gtd)):
        del(associated["line"])
    associated_keys = list(associated.keys())
    mylist = list(obj.__slots__)
    props = []
    for attr in dir(obj.__class__):
        if isinstance(getattr(obj.__class__, attr), property):
            props.append(attr)
    mylist += props

    for a in mylist:
        if (a not in skipped) and (a[0] != "_" or a in must):
            try:
                val = getattr(obj, a)
            except BaseException:
                continue
            if a in associated_keys and val not in [
                    "default", "defup", "defcenter", "defright"]:
                if a == "line" and isinstance(
                        obj, (vcs.isoline.Gi, vcs.unified1D.G1d)):
                    continue
                associated[a].add(val)
            if not isinstance(val,
                              (basestring, tuple, list, long, int, float, dict)) and \
                    val is not None:
                val, asso = dumpToDict(val, skipped, must)
                for k in associated_keys:
                    for v in asso[k]:
                        associated[k].add(v)
            dic[a] = val
    return dic, associated


def dumpToJson(obj, fileout, skipped=["info", "member", "attributes"], must=[
], indent=indent, sort_keys=sort_keys):
    """Uses :py:func:`vcs.utils.dumpToDict` and `json.dumps`_ to construct a
    JSON representation of a VCS object's property values.

    :Example:

        .. doctest:: utils_dumpToJson

            >>> box=vcs.getboxfill()
            >>> vcs.dumpToJson(box, 'box.json') # output properties to file
            >>> vcs.dumpToJson(box,None) # returns JSON string
            '{...}'

    :param obj: An instance of a VCS object to serialize
    :type obj: A VCS object

    :param fileout: A file or a string name of a file into which the JSON
        will be written.
    :type fileout: `str`_ or `file`_

    :param skipped: A list of strings, associated with property names to skip.
    :type skipped: `list`_

    :param must: A list of strings, associated with property names which must
        be captured in the serialization.
    :type must: `list`_

    :param indent: An integer representing whether to pretty-print the JSON.

        * If indent is a non-negative integer, JSON will be printed with proper
            indentation levels.

        * If indent is None, 0, or negative, JSON will be printed in its most
            compact form.

    :type indent: `int`_ or `None`_

    :param sort_keys: Boolean value indicating whether output should be sorted
        by key (True), or not (False)
    :type sort_keys: `bool`_

    :return: The VCS object's properties serialized into a JSON formatted `str`_ .
        OR None, if fileout was specified.
    :rtype: `str`_ or `None`_

    .. _json.dumps: https://docs.python.org/2/library/json.html?highlight=dumps#json.dumps
    """
    dic, associated = dumpToDict(obj, skipped, must)
    if fileout is not None:
        if isinstance(fileout, basestring):
            f = open(fileout, "a+")
        else:
            f = fileout
            fileout = f.name
        if os.path.exists(fileout):
            st = os.stat(fileout)
            if st.st_size != 0:
                try:
                    # Mac needs to rewind, seems ok on other platforms
                    f.seek(0)
                    D = json.load(f)
                except Exception as err:
                    print("Error reading json file," +
                          "will be overwritten", fileout, err)
                    D = {}
            else:
                D = {}
            f.close()
        else:
            D = {}
        f = open(fileout, "w")
        for N in ["g_name", "s_name", "p_name"]:
            if N in dic:
                nm = dic[N]
                del(dic[N])
                break
        d = D.get(nm, {})
        nm2 = dic["name"]
        del(dic["name"])
        d[nm2] = dic
        D[nm] = d
        json.dump(
            D,
            f,
            sort_keys=sort_keys,
            indent=indent,
            separators=(
                ', ',
                ': '))
        if isinstance(fileout, basestring):
            f.close()
            for etype in list(associated.keys()):
                for asso in associated[etype]:
                    if asso is not None and asso not in vcs._protected_elements[
                            etype]:
                        dumpToJson(
                            vcs.elements[etype][asso],
                            fileout,
                            skipped=skipped,
                            must=[],
                            indent=indent,
                            sort_keys=sort_keys)
    else:
        return json.dumps(dic, sort_keys=sort_keys, indent=indent)


def getfontname(number):
    """Retrieve a font name for a given font index.

    :Example:

        .. doctest:: utils_getfontname

            >>> vcs.getfontname(1)
            'default'
            >>> vcs.getfontname(4)
            'Helvetica'

    :param number: Index of the font to get the name of.
    :type number: `int`_
    """
    if number not in vcs.elements["fontNumber"]:
        raise Exception("Error font number not existing %i" % number)
    return vcs.elements["fontNumber"][number]


def getfontnumber(name):
    """Retrieve a font index for a given font name.

    :Example:

        .. doctest:: utils_getfontnumber

            >>> vcs.getfontnumber('default')
            1
            >>> vcs.getfontnumber('Helvetica')
            4

    :param name: Name of the font to get the index of.
    :type name: `str`_
    """
    for i in vcs.elements["fontNumber"]:
        if vcs.elements["fontNumber"][i] == name:
            return i
    raise Exception("Font name not existing! %s" % name)


def process_src_element(code):
    i = code.find("_")
    typ = code[:i]
    code = code[i + 1:]
    i = code.find("(")
    nm = code[:i]
    code = code[i + 1:-1]
    try:
        if typ == "Gfb":
            boxfill.process_src(nm, code)
        elif typ == "Gfi":
            isofill.process_src(nm, code)
        elif typ == "Gi":
            isoline.process_src(nm, code)
        elif typ == "L":
            dic = {}
            sp = code.split(",")
            for i in range(0, len(sp), 2):
                dic[eval(sp[i])] = eval(sp[i + 1])
            vcs.elements["list"][nm] = dic
        elif typ == "Gtd":
            taylor.process_src(nm, code)
        elif typ == "Proj":
            projection.process_src(nm, code)
        elif typ == "Tf":
            fillarea.process_src(nm, code)
        elif typ == "P":
            template.process_src(nm, code)
        elif typ == "Tt":
            texttable.process_src(nm, code)
        elif typ == "To":
            textorientation.process_src(nm, code)
        elif typ == "Tl":
            line.process_src(nm, code)
        elif typ in ["GXy", "GYx", "GXY", "GSp"]:
            unified1D.process_src(nm, code, typ)
        elif typ == "Gv":
            vector.process_src(nm, code)
        elif typ == "Tm":
            marker.process_src(nm, code)
        elif typ == "C":
            colormap.process_src(nm, code)
    except Exception as err:
        print("Processing error for %s,%s: %s" % (nm, typ, err))


def listelements(typ=None):
    """List the elements of a given VCS object type.

    :Example:

        .. doctest:: utils_listelements

            >>> vcs.listelements() # list all vcs object types
            ['1d', '3d_dual_scalar', '3d_scalar', '3d_vector', 'boxfill', ...]
            >>> vcs.listelements('1d')
            [...]
            >>> vcs.listelements('boxfill')
            [...]

    :param typ: String specifying the type of VCS object to list.
        If None, list will contain VCS object type names.
    :type typ: `str`_

    :return: If typ is None, returns a list of VCS object type names.
        If typ is a VCS object type, returns a list of the object of that type
        currently present in VCS.
    :rtype: `list`_
    """

    if typ is None:
        return sorted(vcs.elements.keys())
    if typ in ("xvsy", "yxvsx", "scatter", "xyvsy"):
        names = []
        aliased = ("xvsy", "yxvsx")
        for name, gm in vcs.elements["1d"].items():
            if gm.g_type in aliased and typ in aliased:
                names.append(name)
            elif gm.g_type == typ:
                names.append(name)
        return sorted(names)
    if typ not in list(vcs.elements.keys()):
        raise Exception(
            "Error: '%s' is not a valid vcs element\n"
            "Valid vcs elements are: %s" %
            (typ, sorted(vcs.elements.keys())))
    return sorted(vcs.elements[typ].keys())


#
#
# Show VCS primary and secondary elements wrapper for VCS.                  #
#
#
def show(*args):
    """Show the list of VCS primary and secondary class objects.

    :Example:

        .. doctest:: utils_show

            >>> vcs.show() # show all vcs object types
            ['1d', '3d_dual_scalar', '3d_scalar', '3d_vector', 'boxfill', ...]
            >>> vcs.show('boxfill') # List boxfill objects
            *******************Boxfill Names List**********************
            ...
            *******************End Boxfill Names List**********************
            >>> vcs.show('3d_vector') # List 3d_vector objects
            *******************3d_vector Names List**********************
            ...
            *******************End 3d_vector Names List**********************
            >>> vcs.show('3d_scalar') # List 3d_scalar objects
            *******************3d_scalar Names List**********************
            ...
            *******************End 3d_scalar Names List**********************
            >>> vcs.show('3d_dual_scalar') # List 3d_dual_scalar objects
            *******************3d_dual_scalar Names List**********************
            ...
            *******************End 3d_dual_scalar Names List**********************
            >>> vcs.show('1d') # List 1d objects
            *******************1d Names List**********************
            ...
            *******************End 1d Names List**********************

    :param args: String name of a type of object to show, or None
    :type args: `str`_ or `None`_
    """
    if args == ():
        return vcs.listelements()
    else:
        elts = vcs.listelements(args[0])
        try:
            m = max([len(e) for e in elts]) + 1
        except BaseException:
            m = 4
        print("*******************%s Names List**********************" % (
            args[0].capitalize()))
        for i, e in enumerate(elts):
            print(("%s" % e).ljust(m), end=' ')
            if (i + 1) % 3 == 0:
                print()
        if len(elts) > 0 and (i + 1) % 3 != 0:
            print()
        print("*******************End %s Names List**********************" % (
            args[0].capitalize()))
        return


def _scriptrun(script, canvas=None):
    # Now does the python Graphic methods
    f = open(script, 'r')
    # browse through the file to look for taylordiagram/python graphics methods
    processing = False  # found a taylor graphic method
    for l in f:
        if l[:6] == "color(" and canvas is not None:
            canvas.setcolormap(l.strip()[6:-1])
        elif l[:2] in ["P_", "L_", "C_"] or \
                l[:3] in ["Tm_", "Gv_", "Gi_", "Tl_", "To_", "Tt_", "Tf_", ] or\
                l[:4] in ['GXy_', 'GYx_', 'GXY_', 'GSp_',
                          'Gtd_', 'Gfb_', "Gfm_", "Gfi_"] or \
                l[:5] in ["Proj_", ]:
            # We found a graphic method
            processing = True
            opened = 0
            closed = 0
            s = ""
        if processing:
            s += l.strip()
            opened += l.count("(")
            closed += l.count(")")
            if closed == opened:
                # ok we read the whole Graphic method
                vcs.process_src_element(s)
                processing = False
    f.close()
    # Ok now we need to double check the isolines
    gd = vcs.elements["isoline"]["default"]
    for g in list(vcs.elements["isoline"].values()):
        if g.name == "default":
            continue
        for att in ["line", "textcolors", "text"]:
            try:
                if (att == "line"):
                    setattr(g, "linetypes", getattr(g, "linetypes"))
                else:
                    setattr(g, att, getattr(g, att))
            except BaseException:
                lst = []
                if att == "line":
                    for e in g.line:
                        if e in vcs.elements["line"]:
                            lst.append(vcs.elements["line"][e])
                        else:
                            lst.append(e)
                elif att == "text":
                    for e in g.text:
                        if e in vcs.elements["textorientation"]:
                            lst.append(vcs.elements["textorientation"][e])
                        elif e in vcs.elements["textcombined"]:
                            lst.append(vcs.elements["textcombined"][e])
                        else:
                            lst.append(e)
                elif att == "textcolors":
                    for e in g.textcolors:
                        if e in vcs.elements["texttable"]:
                            lst.append(vcs.elements["texttable"][e])
                        elif e in vcs.elements["textcombined"]:
                            lst.append(vcs.elements["textcombined"][e])
                        else:
                            lst.append(e)
                try:
                    if (att == "line"):
                        g.setLineAttributes(lst)
                    else:
                        setattr(g, att, lst)
                except BaseException:
                    if (att == "line"):
                        setattr(g, "linetypes", getattr(gd, "linetypes"))
                    else:
                        setattr(g, att, getattr(gd, att))

#
#
# Import old VCS file script commands into CDAT.                            #
#
#


def scriptrun_scr(*args):
    import __main__

    # Open VCS script file for reading and read all lines into a Python list
    fin = open(args[0], 'r')
    lns = fin.readlines()
    line_ct = len(lns)
    i = 0

    # Check to see if it is a VCS generated Python script file.
    # If it is, then simply
    # call the execfile function to execute the script and close the file.
    if ((lns[0][0:37] == "#####################################") and
            (lns[1][0:35] == "#                                 #") and
            (lns[2][0:33] == "# Import and Initialize VCS     #") and
            (lns[3][0:31] == "#                             #") and
            (lns[4][0:29] == "#############################")):
        fin.close()
        exec(compile(open(args[0]).read(), args[0], 'exec'), __main__.__dict__)
        return

    while i < line_ct:
        # Loop through all lines and determine when a VCS command line
        # begins and ends. That is, get only one VCS command at a time
        scr_str = lns[i]
        lt_paren_ct = lns[i].count('(')
        rt_paren_ct = lns[i].count(')')
        while lt_paren_ct > rt_paren_ct:
            i += 1
            scr_str += lns[i]
            lt_paren_ct += lns[i].count('(')
            rt_paren_ct += lns[i].count(')')
        i += 1
        scr_str = scr_str.strip()

        # Get the VCS command
        vcs_cmd = scr_str.split('(')[0].split('_')[0]

        function = source = name = units = title = lon_name = lat_name = ''
        comment1 = comment2 = comment3 = comment4 = ''
        if vcs_cmd == 'A':
            # Get the data via CDMS. That is, retrieve that data as a
            # _TransientVariable. But first, get the source, name, title,
            # etc. of the file.
            slab_name = scr_str.split('(')[0][2:]
            a = scr_str.split('",')
            for j in range(len(a)):
                b = a[j].split('="')
                if b[0][-4:].lower() == 'file':
                    # Open CDMS file
                    fcdms = cdms2.open(b[1])
                elif b[0][-8:].lower() == 'function':
                    function = b[1]                              # Get function
                elif b[0].lower() == 'source':
                    source = b[1]
                elif ((b[0][-4:].lower() == 'name') and
                      (b[0][-5:].lower() != 'xname') and
                      (b[0][-5:].lower() != 'yname')):
                    name = b[1].split('")')[0]
                elif b[0].lower() == 'units':
                    units = b[1].split('")')[0]
                elif b[0][-5:].lower() == 'title':
                    title = b[1].split('")')[0]
                elif b[0][-5:].lower() == 'xname':
                    lon_name = b[1].split('")')[0].strip()
                elif b[0][-5:].lower() == 'yname':
                    lat_name = b[1].split('")')[0].strip()
                elif b[0][-9:].lower() == 'comment#1':
                    comment1 = b[1]
                elif b[0][-9:].lower() == 'comment#2':
                    comment2 = b[1]
                elif b[0][-9:].lower() == 'comment#3':
                    comment3 = b[1]
                elif b[0][-9:].lower() == 'comment#4':
                    comment4 = b[1]
            if function != '':
                b = function.split('(')
                V = b[1].split(',')[0]
                __main__.__dict__[slab_name] = __main__.__dict__[V] * 1000.
                continue

            a = scr_str.split(',')

            # Now get the coordinate values
            x1 = x2 = y1 = y2 = None
            for j in range(len(a)):
                c = a[j].split(',')[0]
                b = c.split('=')
                if b[0].lower() == 'xfirst':
                    x1 = float(b[1].split(')')[0])
                elif b[0].lower() == 'xlast':
                    x2 = float(b[1].split(')')[0])
                elif b[0][-6:].lower() == 'yfirst':
                    y1 = float(b[1].split(')')[0])
                elif b[0].lower() == 'ylast':
                    y2 = float(b[1].split(')')[0])

            # Get the variable from the CDMS opened file
            V = fcdms.variables[name]

            # Check for the order of the variable and re-order dimensions
            # if necessary
            Order = '(%s)(%s)' % (lat_name, lon_name)
            Order = Order.strip().replace('()', '')
            if Order == '':
                Order = None
            axis_ids = V.getAxisIds()
            re_order_dimension = 'no'
            try:                 # only re-order on two or more dimensions
                if (axis_ids[-1] != lon_name) and (axis_ids[-2] != lat_name):
                    re_order_dimension = 'yes'
            except BaseException:
                pass

            # Must have the remaining dimension names in the Order list
            if Order is not None:
                O_ct = Order.count('(')
                V_ct = len(V.getAxisIds())
                for j in range(O_ct, V_ct):
                    Order = ('(%s)' % axis_ids[V_ct - j - 1]) + Order

            # Set the data dictionary up to retrieve the dat from CDMS
            if re_order_dimension == 'no':
                if ((x1 is not None) and (x2 is not None) and
                        (y1 is not None) and (y2 is not None)):
                    data_dict = {
                        lon_name: (
                            x1, x2), lat_name: (
                            y1, y2), 'order': Order}
                elif ((x1 is not None) and (x2 is not None) and
                      (y1 is None) and (y2 is None)):
                    data_dict = {lon_name: (x1, x2), 'order': Order}
                elif ((x1 is None) and (x2 is None) and
                      (y1 is not None) and (y2 is not None)):
                    data_dict = {lat_name: (y1, y2), 'order': Order}
                elif ((x1 is None) and (x2 is None) and
                      (y1 is None) and (y2 is None)):
                    data_dict = {}
            else:
                if ((x1 is not None) and (x2 is not None) and
                        (y1 is not None) and (y2 is not None)):
                    data_dict = {
                        lat_name: (
                            x1, x2), lon_name: (
                            y1, y2), 'order': Order}
                elif ((x1 is not None) and (x2 is not None) and
                      (y1 is None) and (y2 is None)):
                    data_dict = {lon_name: (x1, x2), 'order': Order}
                elif ((x1 is None) and (x2 is None) and
                      (y1 is not None) and (y2 is not None)):
                    data_dict = {lat_name: (y1, y2), 'order': Order}
                elif ((x1 is None) and (x2 is None) and
                      (y1 is None) and (y2 is None)):
                    data_dict = {}

            # Now store the _TransientVariable in the main dictionary for use
            # later
            V.units = units
            V.source = source
            V.title = title
            V.comment1 = comment1
            V.comment2 = comment2
            V.comment3 = comment3
            V.comment4 = comment4
            __main__.__dict__[slab_name] = V(*(), **data_dict)

            fcdms.close()                                     # Close CDMS file
        elif vcs_cmd == 'D':
            # plot the data with the appropriate graphics method and template
            a = scr_str.split(',')
            a_name = b_name = None
            for j in range(len(a)):
                b = a[j].split('=')
                if b[0][-3:].lower() == 'off':
                    continue
                elif b[0].lower() == 'priority':
                    continue
                elif b[0].lower() == 'type':
                    graphics_type = b[1]
                elif b[0].lower() == 'template':
                    template = b[1]
                elif b[0].lower() == 'graph':
                    graphics_name = b[1]
                elif b[0].lower() == 'a':
                    a_name = b[1].split(')')[0]
                elif b[0].lower() == 'b':
                    b_name = b[1].split(')')[0]

            arglist = []

            if a_name is not None:
                arglist.append(__main__.__dict__[a_name])
            else:
                arglist.append(None)
            if b_name is not None:
                arglist.append(__main__.__dict__[b_name])
            else:
                arglist.append(None)
            arglist.append(template)
            arglist.append(graphics_type)
            arglist.append(graphics_name)

            if (a_name is not None) and (graphics_type != 'continents'):
                CANVAS = vcs.init()
                CANVAS.plot(*arglist, bg=False)

        elif vcs_cmd.lower() == 'canvas':
            warnings.warn("Please implement vcs 'canvas' function")
        elif vcs_cmd.lower() == 'page':
            warnings.warn("Please implement vcs 'page' function")
        else:  # Send command to VCS interpreter
            if (len(scr_str) > 1) and (scr_str[0] != '#'):
                # Save command to a temporary file first,
                # then read script command
                # This is the best solution. Avoids rewriting C code that I
                # know works!
                temporary_file_name = tempfile.mktemp('.scr')
                fout = open(temporary_file_name, 'w')
                fout.writelines(scr_str)
                fout.close()
                _scriptrun(temporary_file_name)
                os.remove(temporary_file_name)
    fin.close()


def saveinitialfile():
    _dotdir, _dotdirenv = vcs.getdotdirectory()
    fnm = os.path.join(os.path.expanduser("~"), _dotdir, 'initial.attributes')
    if os.path.exists(fnm):
        os.remove(fnm)
    Skip = {}
    for k in list(vcs.elements.keys()):
        Skip[k] = []
        for e in list(vcs.elements[k].keys()):
            if e in vcs._protected_elements[k] or e[
                    :2] == "__":  # temporary elt
                Skip[k].append(e)
    for k in list(vcs.elements.keys()):
        if k in ["display", "font", "fontNumber"]:
            continue
        elif k == "list":
            D2 = {}
            D2["L"] = {}
            for l in list(vcs.elements["list"].keys()):
                if l not in Skip["list"]:
                    D2["L"][l] = vcs.elements["list"][l]
            if len(list(D2["L"].keys())) != 0:
                f = open(fnm + ".json", "w")
                json.dump(D2, f)
                f.close()
            continue
        e = vcs.elements[k]
        for nm, g in e.items():
            if nm not in Skip[k]:
                try:
                    g.script(fnm)
                except Exception as err:
                    warnings.warn(
                        "Could not save graphic method %s named %s: %s" %
                        (k, nm, err))
    # extension .json has been auto-added, removing it in this specific case
    os.rename(fnm + ".json", fnm)

#
#
# Import old VCS file script commands into CDAT.
#
#


def scriptrun(script):
    if script.split(".")[-1] == "scr":
        scriptrun_scr(script)
    elif script.split(".")[-1] == "py":
        exec(compile(open(script).read(), script, 'exec'))
    else:
        if os.path.split(script)[-1] == "initial.attributes":
            vcs._doValidation = False
        loader = {"P": 'template',
                  "Gfb": 'boxfill',
                  "Gfi": 'isofill',
                  "Gi": 'isoline',
                  "Gvp": 'vector',
                  "Gs": 'streamline',
                  "Gfm": 'meshfill',
                  "G1d": '1d',
                  "Tf": 'fillarea',
                  "Tt": "texttable",
                  "To": "textorientation",
                  "Tm": "marker",
                  "Tl": "line",
                  "Gf3Dscalar": "3d_scalar",
                  "Gf3DDualScalar": "3d_dual_scalar",
                  "Gf3Dvector": "3d_vector",
                  "Proj": "projection",
                  "Gtd": "taylordiagram",
                  "Cp": "colormap",
                  "L": "L",
                  }
        try:
            f = open(script)
            jsn = json.load(f)
            keys = []
            for k in ["Tt", "To", "Tl",
                      "Tm", "Proj"]:  # always read these first
                if k in list(jsn.keys()):
                    keys.append(k)
            for k in list(jsn.keys()):
                if k not in keys:
                    keys.append(k)
            for typ in keys:
                for nm, v in jsn[typ].items():
                    if typ == "P":
                        try:
                            loadTemplate(str(nm), v)
                        except Exception as err:
                            print("could not load tmpl:", nm, err)
                    else:
                        try:
                            loadVCSItem(loader[typ], nm, v)
                        except Exception as err:
                            print("failed", typ, nm, err)
        # ok could not read json file maybe it is an old initial.attributes
        except Exception as err:
            if os.path.split(script)[-1] == "initial.attributes":
                _scriptrun(script)
            else:
                warnings.warn("unable to source file: %s %s" % (script, err))
    vcs._doValidation = True
    return


def loadTemplate(nm, vals):
    try:
        t = vcs.gettemplate(nm)
    except Exception:
        t = vcs.createtemplate(nm)
    for k, v in vals.items():
        A = getattr(t, k)
        for a, v in v.items():
            if isinstance(v, basestring):
                v = str(v)
            setattr(A, a, v)


def loadVCSItem(typ, nm, json_dict={}):
    if typ in list(vcs._protected_elements.keys(
    )) and nm in vcs._protected_elements[typ]:
        # protected element do not overload
        return
    tp = typ
    if typ == "L":
        d = {}
        for k, v in json_dict.items():
            try:
                d[eval(k)] = eval(v)
            except BaseException:
                d[eval(k)] = v
        vcs.elements["list"][nm] = d
        return

    if nm in vcs.elements[tp]:
        # skip defaults and temp ones
        if nm not in ["default_scatter_", "default_xvsy_",
                      "default_xyvsy_", "default_yxvsx_"]:
            gm = vcs.elements[tp][nm]
    else:
        cmd = "gm = vcs.create%s('%s')" % (typ, nm)
        loc = locals()
        exec(cmd)
        gm = loc["gm"]
    for a, v in json_dict.items():
        if isinstance(v, dict):
            if a == "Marker" and tp == "taylordiagram":
                gm.addMarker()
                for k in list(v.keys()):
                    cmd = "gm.Marker.%s = %s" % (k, repr(v[k]))
                    loc = locals()
                    exec(cmd)
                    gm = loc["gm"]
            else:
                for k in list(v.keys()):
                    try:
                        v[eval(k)] = v[k]
                        del(v[k])
                    except BaseException:
                        pass
        elif isinstance(v, basestring):
            v = str(v)
        if not(a == "Marker" and tp == "taylordiagram"):
            setattr(gm, a, v)

            if nm in vcs_deprecated_colormap_names:
                cmd = "gm = vcs.create%s('%s')" % (
                    typ, vcs_deprecated_colormap_names[nm])
                loc = locals()
                exec(cmd)
                gm = loc["gm"]
                setattr(gm, a, v)

    return gm


def return_display_names():
    return [""], [""]


def getdotdirectory():
    return ".uvcdat", "UVCDAT_DIR"


class VCSUtilsError (Exception):

    def __init__(self, args=None):
        """Create an exception"""
        self.args = args

    def __str__(self):
        """Calculate the string representation"""
        return str(self.args)
    __repr__ = __str__


def minmax(*data):
    """Return the minimum and maximum of a series of array/list/tuples
    (or combination of these)
    You can combine list/tuples/arrays pretty much any combination is allowed

    :Example:

        .. doctest:: utils_minmax

            >>> s = range(7)
            >>> vcs.minmax(s)
            (0.0, 6.0)
            >>> vcs.minmax([s, s])
            (0.0, 6.0)
            >>> vcs.minmax([[s, list(s) * 2], 4., [6., 7., s]],[ 5., -7., 8, (6., 1.)])
            (-7.0, 8.0)

    :param data: A comma-separated list of lists/arrays/tuples
    :type data: `list`_

    :returns: A tuple in the form (min, max)
    :rtype: `tuple`_
    """

    mx = -1.E77
    mn = 1.E77
    if len(data) == 1:
        data = data[0]
    global myfunction

    def myfunction(d, mx, mn):
        if d is None:
            return mx, mn
        from numpy.ma import maximum, minimum, count
        if isinstance(d, (int, float)):
            return maximum(d, mx), minimum(d, mn)
        try:
            if count(d) == 0:
                return mx, mn
            mx = float(maximum(mx, maximum.reduce(d, axis=None)))
            mn = float(minimum(mn, minimum.reduce(d, axis=None)))
        except BaseException:
            for i in d:
                mx, mn = myfunction(i, mx, mn)
        return mx, mn
    mx, mn = myfunction(data, mx, mn)
    if mn == 1.E77 and mx == -1.E77:
        mn, mx = 1.E20, 1.E20
    return mn, mx


def mkevenlevels(n1, n2, nlev=10):
    """Return a series of evenly spaced levels going from n1 to n2.
    By default 10 intervals will be produced.

    :Example:

        .. doctest:: utils_mkevenlevels

            >>> vcs.mkevenlevels(0,100)
            [0.0, 10.0, 20.0, 30.0, 40.0, 50.0, 60.0, 70.0, 80.0, 90.0, 100.0]
            >>> vcs.mkevenlevels(0,100,nlev=5)
            [0.0, 20.0, 40.0, 60.0, 80.0, 100.0]
            >>> vcs.mkevenlevels(100,0,nlev=5)
            [100.0, 80.0, 60.0, 40.0, 20.0, 0.0]

    :param n1: Beginning of range.
    :type n1: `int`_ or `float`_

    :param n2: End of range. Int or float.
    :type n2: `int`_ or `float`_

    :param nlev: Number of levels by which to split the given range.
    :type nlev: `int`_

    :returns: List of floats, splitting range evenly between n1 and n2
    :rtype: `list`_
"""
    import numpy.ma
    lev = numpy.ma.arange(nlev + 1, dtype=numpy.float)
    factor = float(n2 - n1) / nlev
    lev = factor * lev
    lev = lev + n1
    return list(lev)


def mkscale(n1, n2, nc=12, zero=1, ends=False):
    """This function return a nice scale given a min and a max

    .. warning::

        Not all functionality for the 'zero' parameter has been implemented.
        zero=0 is intended to let the function decide what should be done with zeros,
        but it has yet to be defined. Do not use zero=0.

    :Examples:

        .. doctest:: utils_mkscale

            >>> vcs.mkscale(0,100)
            [0.0, 10.0, 20.0, 30.0, 40.0, 50.0, 60.0, 70.0, 80.0, 90.0, 100.0]
            >>> vcs.mkscale(0,100,nc=5)
            [0.0, 20.0, 40.0, 60.0, 80.0, 100.0]
            >>> vcs.mkscale(-10,100,nc=5)
            [-25.0, 0.0, 25.0, 50.0, 75.0, 100.0]
            >>> vcs.mkscale(-10,100,nc=5,zero=-1)
            [-20.0, 20.0, 60.0, 100.0]
            >>> vcs.mkscale(2,20)
            [2.0, 4.0, 6.0, 8.0, 10.0, 12.0, 14.0, 16.0, 18.0, 20.0]
            >>> vcs.mkscale(2,20,zero=2)
            [0.0, 2.0, 4.0, 6.0, 8.0, 10.0, 12.0, 14.0, 16.0, 18.0, 20.0]

    :param n1: Minimum number in range.
    :type n1: `float`_

    :param n2: Maximum number in range.
    :type n2: `float`_

    :param nc: Maximum number of intervals
    :type nc: `int`_

    :param zero: Integer flag to indicate how zero should be handled. Flags are as follows
        -1: zero MUST NOT be a contour
        0: let the function decide # NOT IMPLEMENTED
        1: zero CAN be a contour  (default)
        2: zero MUST be a contour
    :type zero: `int`_

    :param end: Boolean value indicating whether n1 and n2 should be part of the returned labels.
        Defaults to False.
    :type end: `bool`_

    :returns: List of floats split into nc intervals
    :rtype: `list`_
    """
    if n1 == n2:
        return [n1]
    import numpy
    nc = int(nc)
    cscale = 0  # ???? May be later
    min, max = minmax(n1, n2)
    if zero > 1.:
        if min > 0.:
            min = 0.
        if max < 0.:
            max = 0.
    rg = float(max - min)  # range
    if rg == 0:
        return [min, ]
    delta = rg / nc  # basic delta
    # scale delta to be >10 and <= 100
    lg = -numpy.log10(delta) + 2.
    il = numpy.floor(lg)
    delta = delta * (10. ** il)
    max = max * (10. ** il)
    min = min * (10. ** il)
    if zero > -0.5:
        if delta <= 20.:
            delta = 20
        elif delta <= 25.:
            delta = 25
        elif delta <= 40.:
            delta = 40
        elif delta <= 50.:
            delta = 50
        elif delta <= 101.:
            delta = 100
        first = numpy.floor(min / delta) - 1.
    else:
        if delta <= 20.:
            delta = 20
        elif delta <= 40.:
            delta = 40
        elif delta <= 60.:
            delta = 60
        elif delta <= 101.:
            delta = 100
        first = numpy.floor(min / delta) - 1.5

    if ends:
        scvals = n1 + delta * numpy.arange(2 * nc)
    else:
        scvals = delta * (numpy.arange(2 * nc) + first)

    a = 0
    for j in range(len(scvals)):
        if scvals[j] > min:
            a = j - 1
            break
    b = 0
    for j in range(len(scvals)):
        if scvals[j] >= max:
            b = j + 1
            break
    if cscale == 0:
        cnt = scvals[a:b] / 10. ** il
    else:
        # not done yet...
        raise VCSUtilsError('ERROR scale not implemented in this function')
    return list(cnt)


def __split2contiguous(levels):
    """ Function __split2contiguous(levels)
    takes list of split intervals and make it contiguous if possible
    """
    tmplevs = []
    for il in range(len(levels)):
        lv = levels[il]
        if not (isinstance(lv, list) or isinstance(lv, tuple)):
            raise VCSUtilsError("Error levels must be a set of intervals")
        if not len(lv) == 2:
            raise VCSUtilsError("Error intervals can only have 2 elements")
        if il != 0:
            lv2 = levels[il - 1]
            if lv2[1] != lv[0]:
                raise VCSUtilsError(
                    "Error intervals are NOT contiguous from " + str(lv2[1]) + " to " + str(lv[0]))
        tmplevs.append(lv[0])
    tmplevs.append(levels[-1][1])
    return tmplevs


def mklabels(vals, output='dict'):
    """This function gets levels and output strings for nice display of the
    levels values.

    :Examples:

        .. doctest:: utils_mklabels

            >>> from __future__ import print_function
            >>> scale = vcs.mkscale(2, 20, zero=2)
            >>> labels = vcs.mklabels(scale)
            >>> keys = sorted(labels.keys())
            >>> for key in keys:
            ...     print(key, ':', labels[key])
            0.0 : 0
            2.0 : 2
            4.0 : 4
            6.0 : 6
            8.0 : 8
            10.0 : 10
            12.0 : 12
            14.0 : 14
            16.0 : 16
            18.0 : 18
            20.0 : 20
            >>> labels=vcs.mklabels([.00002,.00003,.00005])
            >>> keys=sorted(labels.keys())
            >>> for key in keys:
            ...     print(key, ':', labels[key])
            2e-05 : 2E-5
            3e-05 : 3E-5
            5e-05 : 5E-5
            >>> vcs.mklabels ([.00002,.00005],output='list')
            ['2E-5', '5E-5']

    :param vals: List or tuple of float values
    :type vals: `list`_, `tuple`_

    :param output: Specifies the desired output type. One of ['dict', 'list'].
    :type output: `str`_

    :returns: Dictionary or list of labels for the given values.
    :rtype: `dict`_ or `list`_
    """
    import numpy.ma
    if isinstance(vals[0], (list, tuple)):
        vals = __split2contiguous(vals)
    vals = numpy.ma.asarray(vals)
    nvals = len(vals)
    ineg = 0
    # Finds maximum number to write
    amax = float(numpy.ma.maximum(numpy.ma.absolute(vals)))
    if amax == 0:
        if output[:3].lower() == 'dic':
            return {0: '0'}
        else:
            return ['0']
    amin, amax = minmax(numpy.ma.masked_equal(numpy.ma.absolute(vals), 0))
    ratio = amax / amin
    if int(numpy.ma.floor(numpy.ma.log10(ratio))) + 1 > 6:
        lbls = []
        for i in range(nvals):
            if vals[i] != 0:
                lbls.append(mklabels([vals[i]], output='list')[0])
            else:
                lbls.append('0')
        if output[:3].lower() == 'dic':
            dic = {}
            for i in range(len(vals)):
                dic[float(vals[i])] = lbls[i]
            return dic
        else:
            return lbls
    tmax = float(numpy.ma.maximum(vals))
    if tmax < 0.:
        ineg = 1
        vals = -vals
        amax = float(numpy.ma.maximum(vals))
    #  Number of digit on the left of decimal point
    idigleft = int(numpy.ma.floor(numpy.ma.log10(amax))) + 1

    # Now determine the number of significant figures
    idig = 0
    for i in range(nvals):
        aa = numpy.ma.power(10., -idigleft)
        while abs(round(aa * float(vals[i])) - aa * vals[i]) > .000001:
            aa = aa * 10.
        idig = numpy.ma.maximum(
            idig,
            numpy.ma.floor(
                numpy.ma.log10(
                    aa *
                    numpy.ma.power(
                        10.,
                        idigleft))))
    idig = int(idig)

    # Now does the writing part
    lbls = []
    # First if we need an E format
    if idigleft > 5 or idigleft < -2:
        if idig == 1:
            for i in range(nvals):
                aa = int(
                    round(
                        float(
                            vals[i]) /
                        numpy.ma.power(
                            10.,
                            idigleft -
                            1)))
                lbls.append(str(aa) + 'E' + str(idigleft - 1))
        else:
            for i in range(nvals):
                aa = str(
                    round(
                        ((vals[i] /
                          numpy.ma.power(
                            10.,
                            idigleft -
                            1)) *
                            numpy.power(
                            10,
                            idig))) /
                    numpy.power(
                        10,
                        idig))
                ii = 1
                if vals[i] < 0.:
                    ii = 2
                aa = aa.ljust(idig + ii)
                aa = aa.replace(' ', '0')
                lbls.append(aa + 'E' + str(idigleft - 1))
    elif idigleft > 0 and idigleft >= idig:  # F format
        for i in range(nvals):
            lbls.append(str(int(round(float(vals[i])))))
    else:
        for i in range(nvals):
            ii = 1
            if vals[i] < 0.:
                ii = 2
            ndig = idig + ii
            rdig = idig - idigleft
            if idigleft < 0:
                ndig = idig - idigleft + 1 + ii
            aa = '%' + str(ndig) + '.' + str(rdig) + 'f'
            aa = aa % vals[i]
            lbls.append(aa)
    if ineg:
        vals = -vals
        for i in range(len(lbls)):
            lbls[i] = '-' + lbls[i]
    if output[:3].lower() == 'dic':
        dic = {}
        for i in range(len(vals)):
            dic[float(vals[i])] = str(lbls[i])
        return dic
    else:
        return lbls


def getcolors(levs, colors=None, split=1, white="white"):
    """For isofill/boxfill purposes
    Given a list of levels this function returns the colors that would
    best spread a list of "user-defined" colors (default is 0 to 255,
    i.e 256 colors), always using the first and last color.
    Optionally the color range can be split into 2 equal domain to
    represent <0 and >0 values.
    If the colors are split an interval goes from <0 to >0
    then this is assigned the "white" color
    the default range of colors to use can be adjusted by setting:
    vcs.utils.defaultColorsRange = newrange

    :Example:

        .. doctest:: utils_getcolors

            >>> a=[0.0, 2.0, 4.0, 6.0, 8.0, 10.0, 12.0, 14.0, 16.0, 18.0, 20.0]
            >>> vcs.getcolors (a)
            [0, 28, 57, 85, 113, 142, 170, 198, 227, 255]
            >>> vcs.getcolors (a,colors=range(16,200))
            [16, 36, 57, 77, 97, 118, 138, 158, 179, 199]
            >>> vcs.getcolors(a,colors=[16,25,15,56,35,234,12,11,19,32,132,17])
            [16, 25, 15, 35, 234, 12, 11, 32, 132, 17]
            >>> a=[-6.0, -2.0, 2.0, 6.0, 10.0, 14.0, 18.0, 22.0, 26.0]
            >>> vcs.getcolors (a,white=241)
            [0, 241, 128, 153, 179, 204, 230, 255]
            >>> vcs.getcolors (a,white=241,split=0)
            [0, 36, 73, 109, 146, 182, 219, 255]

    :param levs: levels defining the color ranges
    :type levs: `list`_ or `tuple`_

    :param colors: A list/tuple of the of colors you wish to use
    :type colors: `list`_ or `tuple`_

    :param split: Integer flag to split colors between two equal domains.
        0 : no split
        1 : split if the levels go from <0 to >0
        2 : split even if all the values are positive or negative
    :type split: `int`_

    :param white: If split is on and an interval goes from <0 to >0 this color
                  will be used within this interval.
    :type white: `int`_ or `str`_ or `tuple`_

    :returns: List of colors
    :rtype: `list`_
    """

    if colors is None:
        colors = defaultColorsRange
    if len(levs) == 1:
        return [colors[0]]
    if isinstance(levs[0], list) or isinstance(levs[0], tuple):
        tmplevs = [levs[0][0]]
        for i in range(len(levs)):
            if i != 0:
                if levs[i - 1][1] * levs[i][0] < 0.:
                    tmplevs[-1] = 0.
            tmplevs.append(levs[i][1])
        levs = tmplevs
    # Take care of the input argument split
    if isinstance(split, basestring):
        if split.lower() == 'no':
            split = 0
        elif split.lower() == 'force':
            split = 2
        else:
            split = 1
    # Take care of argument white
    if isinstance(white, basestring):
        white = [value / 2.55 for value in genutil.colors.str2rgb(white)]

    # Gets first and last value, and adjust if extensions
    mn = levs[0]
    mx = levs[-1]
    # If first level is < -1.E20 then use 2nd level for mn
    if levs[0] <= -9.E19 and levs[1] > 0.:
        mn = levs[1]
    # If last level is > 1.E20 then use 2nd to last level for mx
    if levs[-1] >= 9.E19 and levs[-2] < 0.:
        mx = levs[-2]
    # Do we need to split the palette in 2 ?
    sep = 0
    if mx * mn < 0. and split == 1:
        sep = 1
    if split == 2:
        sep = 1
    # Determine the number of colors to use
    nc = len(levs) - 1

    # In case only 2 levels, i.e only one color to return
    if nc == 1:
        if split > 0 and levs[0] * levs[1] <= 0:  # Change of sign
            return white
        else:
            return colors[0]

    # Number of colors passed
    ncols = len(colors)

    col = []
    # Counts the number of negative colors
    nn = 0  # initialize
    # if (mn<=0.) and (levs[0]<=-9.E19) : nn=nn+1 # Ext is one more <0 box
    zr = 0  # Counter to know if you stop by zero or it is included in a level
    for i in range(nc):
        if levs[i] < 0.:
            nn = nn + 1  # Count nb of <0 box
        if levs[i] == 0.:
            zr = 1    # Do we stop at zero ?
    np = nc - nn  # Nb of >0 box is tot - neg -1 for the blank box

    if mx * mn < 0. and zr == 0:
        nn = nn - 1  # we have a split cell bet + and - so remove a -
    # Determine the interval (in colors) between each level
    cinc = (ncols - 1.) / float(nc - 1.)

    # Determine the interval (in colors) between each level (neg)
    cincn = 0.
    if nn != 0 and nn != 1:
        cincn = (ncols / 2. - 1.) / float(nn - 1.)

    # Determine the interval (in colors) between each level (pos)
    cincp = 0
    isplit = 0
    if np != 0 and np != 1:
        cincp = (ncols / 2. - 1.) / float(np - 1.)
    if sep != 1:
        for i in range(nc):
            cv = i * cinc
            col.append(colors[int(round(cv))])
    else:
        col = []
        for i in range(nc):
            if levs[i] < 0:
                cv = i * cincn
            # if nn==1 : cv=len(colors)/4.   # if only 1 neg then use the
            # middle of the neg colors
                if (levs[i]) * (levs[i + 1]) < 0:
                    col.append(white)
                    isplit = 1
                else:
                    col.append(colors[int(round(cv))])
            else:
                # if only 1 pos then use the middle of the pos colors
                if np == 1:
                    cv = 3 * \
                        len(colors) / \
                        4.
                cv = ncols / 2. + (i - nn - isplit) * cincp
                col.append(colors[int(round(cv))])
    if col[0] == white and levs[0] < -9.E19:
        col[0] = colors[0]
    return col


def generate_time_labels(d1, d2, units, calendar=cdtime.DefaultCalendar):
    """Generates a dictionary of time labels for an interval of time,
    in a user defined units system.

    :Example:

        .. doctest:: utils_generate_time_labels

            # Two ways to generate a dictionary of time labels
            >>> import cdtime
            >>> lbls = vcs.generate_time_labels(cdtime.reltime(0,'months since 2000'),
            ...     cdtime.reltime(12,'months since 2000'),
            ...     'days since 1800') # for the year 2000 in units of 'days since 1800'
            >>> lbls = vcs.generate_time_labels(cdtime.reltime(0,'months since 2000'),
            ...     cdtime.comptime(2001),
            ...     'days since 1800') # for the year 2000 in units of 'days since 1800'
            >>> lbls = vcs.generate_time_labels(0, 12, 'months since 2000') # time labels for year 2000


    :param d1: The beginning of the time interval to be labelled. Expects a cdtime object.
                Can also take int, long, or float,
                which will be used to create a cdtime object with the given units parameter.
    :type d1: cdtime object or `int`_ or `long`_ or `float`_

    :param d2: The end of the time interval to be labelled. Expects a cdtime object.
                Can also take int, long, or float,
                which will be used to create a cdtime object with the given units parameter.
    :type d2: cdtime object or `int`_ or `long`_ or `float`_

    :param units: String with the format '[time_unit] since [date]'.
    :type units: `str`_

    :param calendar: A cdtime calendar

    :returns: Dictionary of time labels over the given time interval
    :rtype: dict

    """
    if isinstance(d1, (int, float)):
        d1 = cdtime.reltime(d1, units)
    if isinstance(d2, (int, float)):
        d2 = cdtime.reltime(d2, units)
    d1r = d1.torel(units, calendar)
    d2r = d2.torel(units, calendar)
    d1, d2 = minmax(d1r.value, d2r.value)
    u = units.split('since')[0].strip().lower()
    dic = {}
    if u in ['month', 'months']:
        delta = (d2 - d1) * 30
    elif u in ['year', 'years']:
        delta = (d2 - d1) * 365
    elif u in ['hours', 'hour']:
        delta = (d2 - d1) / 24.
    elif u in ['minute', 'minutes']:
        delta = (d2 - d1) / 24. / 60.
    elif u in ['second', 'seconds']:
        delta = (d2 - d1) / 24. / 60. / 60.
    else:
        delta = d2 - d1
    if delta < .042:  # less than 1 hour
        levs = mkscale(d1, d2)
        for l in levs:
            dic[l] = str(cdtime.reltime(l, units).tocomp(calendar))
    elif delta < 1:  # Less than a day put a label every hours
        d1 = d1r.torel('hours since 2000').value
        d2 = d2r.torel('hours since 2000').value
        d1, d2 = minmax(d1, d2)
        levs = mkscale(d1, d2)
        for l in levs:
            t = cdtime.reltime(l, 'hours since 2000').tocomp(calendar)
            if t.minute > 30:
                t = t.add(1, cdtime.Hour)
            t.minute = 0
            t.second = 0
            tr = t.torel(units, calendar)
            dic[tr.value] = str(t).split(':')[0]
    elif delta < 90:  # Less than 3 month put label every day
        d1 = d1r.torel('days since 2000').value
        d2 = d2r.torel('days since 2000').value
        d1, d2 = minmax(d1, d2)
        levs = mkscale(d1, d2)
        for l in levs:
            t = cdtime.reltime(l, 'days since 2000').tocomp(calendar)
            if t.hour > 12:
                t = t.add(1, cdtime.Day)
            t.hour = 0
            t.minute = 0
            t.second = 0
            tr = t.torel(units, calendar)
            dic[tr.value] = str(t).split(' ')[0]
    elif delta < 800:  # ~ Less than 24 month put label every month
        d1 = d1r.torel('months since 2000').value
        d2 = d2r.torel('months since 2000').value
        d1, d2 = minmax(d1, d2)
        levs = mkscale(d1, d2)
        for l in levs:
            t = cdtime.reltime(l, 'months since 2000').tocomp(calendar)
            if t.day > 15:
                t = t.add(1, cdtime.Month)
            t.day = 1
            t.hour = 0
            t.minute = 0
            t.second = 0
            tr = t.torel(units, calendar)
            dic[tr.value] = '-'.join(str(t).split('-')[:2])
    else:  # ok lots of years, let auto decide but always puts at Jan first
        d1 = d1r.torel('years since 2000').value
        d2 = d2r.torel('years since 2000').value
        d1, d2 = minmax(d1, d2)
        levs = mkscale(d1, d2)
        for l in levs:
            t = cdtime.reltime(l, 'years since 2000').tocomp(calendar)
            if t.month > 6:
                t = t.add(1, cdtime.Year)
            t.month = 1
            t.day = 1
            t.hour = 0
            t.minute = 0
            t.second = 0
            tr = t.torel(units, calendar)
            dic[tr.value] = str(t).split('-')[0]
    return dic


def prettifyAxisLabels(ticks, axis):
    for k in list(ticks.keys()):
        if len(ticks[k]) == 0:
            continue
        if axis == "longitude":
            K = k % 360
            if K > 180:
                if int(K) == float(K):
                    ticks[k] = "%iW" % (360 - K)
                else:
                    ticks[k] = "%.2fW" % (360 - K)
            elif K < 180:
                if numpy.allclose(K, 0.):
                    ticks[k] = "0"
                elif int(K) == float(K):
                    ticks[k] = "%iE" % (K)
                else:
                    ticks[k] = "%.2fE" % (K)
            else:
                if k == -180.:
                    ticks[k] = "180W"
                else:
                    ticks[k] = "180E"
        elif axis == "latitude":
            if k < 0:
                if len(ticks[k]) > 4:
                    ticks[k] = "%.1f" % eval(ticks[k][1:]) + "S"
                else:
                    ticks[k] = ticks[k][1:] + "S"
            elif k > 0:
                if len(ticks[k]) > 4:
                    ticks[k] = "%.1f" % eval(ticks[k]) + "N"
                else:
                    ticks[k] = ticks[k] + "N"
            else:
                ticks[0] = "Eq"
    return ticks


def setTicksandLabels(gm, copy_gm, datawc_x1, datawc_x2,
                      datawc_y1, datawc_y2, x=None, y=None):
    """Sets the labels and ticks for a graphics method made in python

    :param gm: A VCS graphics method to alter
    :type gm: VCS graphics method

    :param copy_gm: A VCS graphics method object
    :type copy_gm: VCS graphics method

    :param datawc_x1: Float value to set the graphics method's datawc_x1 property to.
    :type datawc_x1: `float`_

    :param datawc_x2: Float value to set the graphics method's datawc_x2 property to.
    :type datawc_x2: `float`_

    :param datawc_y1: Float value to set the graphics method's datawc_y1 property to.
    :type datawc_y1: `float`_

    :param datawc_y2: Float value to set the graphics method's datawc_y2 property to.
    :type datawc_y2: `float`_

    :param x: If provided, must be the string 'longitude'
    :type x: `str`_

    :param y: If provided, must be the string 'latitude'
    :type y: `str`_

    :returns: A VCS graphics method object
    :rtype: A VCS graphics method object
    """
    # Ok all this is nice but if user specified datawc we need to use it!
    for a in ["x1", "x2", "y1", "y2"]:
        nm = "datawc_%s" % a
        if not numpy.allclose(getattr(gm, nm), 1.e20):
            loc = locals()
            exec("%s = gm.%s" % (nm, nm))
            if nm == "datawc_x1":
                datawc_x1 = loc[nm]
            elif nm == "datawc_x2":
                datawc_x2 = loc[nm]
            elif nm == "datawc_y1":
                datawc_y1 = loc[nm]
            elif nm == "datawc_y2":
                datawc_y2 = loc[nm]
    if isinstance(gm, vcs.taylor.Gtd):
        return
    # Now the template stuff
    # first create the dictionary to remember which ones are changed
    dic = {}
    for key in ('xticlabels1', 'xmtics1', 'xticlabels2', 'xmtics2',
                'yticlabels1', 'ymtics1', 'yticlabels2', 'ymtics2'):
        dic[key] = False
    # xticklabels1
    if gm.xticlabels1 is None or gm.xticlabels1 == '*':
        if copy_gm is None:
            copy_gm = creategraphicsmethod(gm.g_name, gm.name)
            gm = copy_gm
        if x == "longitude" and abs(datawc_x2 - datawc_x1) > 30:
            ticks = "Lon30"
        else:
            ticks = vcs.mkscale(datawc_x1, datawc_x2)
            ticks = prettifyAxisLabels(vcs.mklabels(ticks), x)
        setattr(gm, 'xticlabels1', ticks)
        dic['xticlabels1'] = True
    # xmtics1
    if gm.xmtics1 is None or gm.xmtics1 == '*':
        if copy_gm is None:
            copy_gm = creategraphicsmethod(gm.g_name, gm.name)
            gm = copy_gm
        if x == "longitude" and abs(datawc_x2 - datawc_x1) > 30:
            ticks = list(gm.xticlabels1.keys())
        else:
            ticks = vcs.mkscale(datawc_x1, datawc_x2)
        tick2 = []
        for i in range(len(ticks) - 1):
            tick2.append((ticks[i] + ticks[i + 1]) / 2.)
        ticks = prettifyAxisLabels(vcs.mklabels(tick2), x)
        setattr(gm, 'xmtics1', ticks)
        dic['xmtics1'] = True
    # xticklabels2
    if hasattr(gm, "xticlabels2") and (
            gm.xticlabels2 is None or gm.xticlabels2 == '*'):
        if copy_gm is None:
            copy_gm = creategraphicsmethod(gm.g_name, gm.name)
            gm = copy_gm
        if x == "longitude" and abs(datawc_x2 - datawc_x1) > 30:
            ticks = "Lon30"
        else:
            ticks = vcs.mkscale(datawc_x1, datawc_x2)
            ticks = prettifyAxisLabels(vcs.mklabels(ticks), x)
        setattr(gm, 'xticlabels2', ticks)
        dic['xticlabels2'] = True
    # xmtics2
    if hasattr(gm, "xmtics2") and (gm.xmtics2 is None or gm.xmtics2 == '*'):
        if copy_gm is None:
            copy_gm = creategraphicsmethod(gm.g_name, gm.name)
            gm = copy_gm
        if x == "longitude" and abs(datawc_x2 - datawc_x1) > 30:
            ticks = list(gm.xticlabels2.keys())
        else:
            ticks = vcs.mkscale(datawc_x1, datawc_x2)
        tick2 = []
        for i in range(len(ticks) - 1):
            tick2.append((ticks[i] + ticks[i + 1]) / 2.)
        ticks = prettifyAxisLabels(vcs.mklabels(tick2), x)
        setattr(gm, 'xmtics2', ticks)
        dic['xmtics2'] = True
    # yticklabels1
    if gm.yticlabels1 is None or gm.yticlabels1 == '*':
        if copy_gm is None:
            copy_gm = creategraphicsmethod(gm.g_name, gm.name)
            gm = copy_gm
        if y == "latitude" and abs(datawc_y2 - datawc_y1) > 20:
            ticks = "Lat20"
        else:
            ticks = vcs.mkscale(datawc_y1, datawc_y2)
            ticks = prettifyAxisLabels(vcs.mklabels(ticks), y)
        setattr(gm, 'yticlabels1', ticks)
        dic['yticlabels1'] = True
    # ymtics1
    if gm.ymtics1 is None or gm.ymtics1 == '*':
        if copy_gm is None:
            copy_gm = creategraphicsmethod(gm.g_name, gm.name)
            gm = copy_gm
        if y == "latitude" and abs(datawc_y2 - datawc_y1) > 20:
            ticks = list(gm.yticlabels1.keys())
        else:
            ticks = vcs.mkscale(datawc_y1, datawc_y2)
        tick2 = []
        for i in range(len(ticks) - 1):
            tick2.append((ticks[i] + ticks[i + 1]) / 2.)
        ticks = prettifyAxisLabels(vcs.mklabels(tick2), y)
        setattr(gm, 'ymtics1', ticks)
        dic['ymtics1'] = True
    # yticklabels2
    if hasattr(gm, "yticlabels2") and (
            gm.yticlabels2 is None or gm.yticlabels2 == '*'):
        if copy_gm is None:
            copy_gm = creategraphicsmethod(gm.g_name, gm.name)
            gm = copy_gm
        if y == "latitude" and abs(datawc_y2 - datawc_y1) > 20:
            ticks = "Lat20"
        else:
            ticks = vcs.mkscale(datawc_y1, datawc_y2)
            ticks = prettifyAxisLabels(vcs.mklabels(ticks), y)
        setattr(gm, 'yticlabels2', ticks)
        dic['yticlabels2'] = True
    # ymtics2
    if hasattr(gm, "ymtics2") and (gm.ymtics2 is None or gm.ymtics2 == '*'):
        if copy_gm is None:
            copy_gm = creategraphicsmethod(gm.g_name, gm.name)
            gm = copy_gm
        if y == "latitude" and abs(datawc_y2 - datawc_y1) > 20:
            ticks = list(gm.yticlabels2.keys())
        else:
            ticks = vcs.mkscale(datawc_y1, datawc_y2)
        tick2 = []
        for i in range(len(ticks) - 1):
            tick2.append((ticks[i] + ticks[i + 1]) / 2.)
        ticks = prettifyAxisLabels(vcs.mklabels(tick2), y)
        setattr(gm, 'ymtics2', ticks)
        dic['ymtics2'] = True
    return copy_gm


def getcolormap(Cp_name_src='default'):
    """VCS contains a list of secondary methods. This function will create a
    colormap class object from an existing VCS colormap secondary method. If
    no colormap name is given, then colormap 'default' will be used.

    .. note::

        VCS does not allow the modification of 'default' attribute sets.
        However, a 'default' attribute set that has been copied under a
        different name can be modified. (See the createcolormap function.)

    :Example:

        .. doctest:: utils_getcolormap

            >>> a=vcs.init()
            >>> a.show('colormap') # Show all  colormap secondary methods
            *******************Colormap Names List**********************
            ...
            *******************End Colormap Names List**********************
            >>> cp=a.getcolormap() # 'default' colormap
            >>> cp2=a.getcolormap('rainbow') # 'rainbow' colormap


    :param Cp_name_src: String name of an existing colormap VCS object
    :type Cp_name_src: `str`_

    :returns: A pre-existing VCS colormap object
    :rtype: vcs.colormap.Cp
    """
    # Check to make sure the argument passed in is a STRING
    if not isinstance(Cp_name_src, basestring):
        raise ValueError('Error -  The argument must be a string.')

    return vcs.elements["colormap"][Cp_name_src]


def getcolorcell(cell, obj=None):
    """Gets the colorcell of the provided object's colormap at the specified
    cell index. If no object is provided, or if the provided object has no
    colormap, the default colormap is used.

    :Example:

        .. doctest:: utils_getcolorcell

            >>> a=vcs.init()
            >>> b=vcs.createboxfill()
            >>> b.colormap='rainbow'
            >>> a.getcolorcell(2,b)
            [26, 1, 34, 100]

    :param cell: An integer value indicating the index of the desired colorcell.
    :type cell: `int`_

    :param obj: Optional parameter with the object to get a colormap from.
    :type obj: Any VCS object capable of containing a colormap

    :return: The RGBA values of the colormap at the specified cell index.
    :rtype: `list`_
    """
    if obj is None:
        cmap = vcs.getcolormap()
    elif obj.colormap is None:
        cmap = vcs.getcolormap()
    else:
        cmap = vcs.getcolormap(obj.colormap)
    return cmap.index[cell]


def setcolorcell(obj, num, r, g, b, a=100):
    """Set a individual color cell in the active colormap. If default is
    the active colormap, then return an error string.

    .. note::

        If the the visual display is 16-bit, 24-bit, or 32-bit TrueColor,
        then a redrawing
        of the VCS Canvas is made every time the color cell is changed.

    :Example:

        .. doctest:: utils_setcolorcell

            >>> vcs.setcolorcell("AMIP",11,0,0,0)
            >>> vcs.setcolorcell("AMIP",21,100,0,0)
            >>> vcs.setcolorcell("AMIP",31,0,100,0)
            >>> vcs.setcolorcell("AMIP",41,0,0,100)
            >>> vcs.setcolorcell("AMIP",51,100,100,100)
            >>> vcs.setcolorcell("AMIP",61,70,70,70)

    :param obj: String name of a colormap, or a VCS object
    :type obj: `str`_ or VCS object

    :param num: Integer specifying which color cell to change.
        Must be from 0-239.
    :type num: `int`_

    :param r: Integer specifying the red value for the colorcell
    :type r: `int`_

    :param g: Integer specifying the green value for the colorcell
    :type g: `int`_

    :param b: Integer specifying the blue value for the colorcell
    :type b: `int`_

    :param a: Integer specifying the opacity value for the colorcell.
        Must be from 0-100.
    :type a: `int`_
    """

    if isinstance(obj, basestring):
        cmap = getcolormap(obj)
    else:
        cmap = getcolormap(obj.colormap)
    cmap.index[num] = (r, g, b, a)

    return


def match_color(color, colormap=None):
    """Returns the color in the colormap that's closest to the specified color.

    :Example:

        .. doctest:: utils_match_color

            >>> a=vcs.init()
            >>> print(vcs.match_color('salmon', 'magma'))
            192
            >>> print(vcs.match_color('red', 'rainbow'))
            242
            >>> print(vcs.match_color([0,0,100],'default')) # closest color from blue
            52

    :param color: Either a string name, or a rgb value between 0 and 100.
    :type color: `str`_ or `int`_

    :param colormap: A VCS colormap object. If not specified, the default
        colormap is used.
    :type colormap: vcs.colormap.Cp

    :returns: Integer value representing a matching rgb color
    :rtype: int
    """
    # First gets the rgb values
    if isinstance(color, basestring):
        vals = genutil.colors.str2rgb(color)
        vals[0] /= 2.55
        vals[1] /= 2.55
        vals[2] /= 2.55
    else:
        vals = color

    # Now gets the colormap to look in
    if colormap is None:
        colormap = 'default'
    cmap = vcs.getcolormap(colormap)

    # Now tries determines the min rms diff
    rmsmin = 2.E40
    match = None
    for i in list(cmap.index.keys()):
        col = cmap.index[i]
        rms = numpy.sqrt((vals[0] - col[0]) ** 2 +
                         (vals[1] - col[1]) ** 2 +
                         (vals[2] - col[2]) ** 2
                         )
        if rms < rmsmin:
            rmsmin = rms
            match = i
    return match


def monotonic(x):
    """Uses `numpy.diff <https://docs.scipy.org/doc/numpy-1.10.1/reference/generated/numpy.diff.html>`_
    to determine whether the data given by x is monotonic in nature.

    :Example:

        .. doctest:: utils_monotonic

            >>> import numpy, cdms2, os
            >>> from random import randint
            >>> array=numpy.array([range(10) for _ in range(10)])
            >>> mask=[] # we will use this to create a random mask
            >>> for _ in range(10):
            ...     mask.append([randint(0,1) for _ in range(10)])
            >>> ma=numpy.ma.MaskedArray(array, mask)
            >>> if not os.path.exists(vcs.sample_data):
            ...     vcs.download_sample_data_files() # get some data for cdms2
            >>> f=cdms2.open(vcs.sample_data + '/clt.nc')
            >>> v=f('v') # get variable 'v' from clt.nc
            >>> vcs.monotonic(array) # monotonicity of 2D numpy array
            True
            >>> vcs.monotonic(ma) # monotonicity of simple masked array
            True
            >>> vcs.monotonic(v) # monotonicity of cdms2 variable
            False

    :param x: The variable to test for monotonicity.
        Can be any variable with an array-like structure.
        Typical examples are numpy arrays, numpy masked arrays,
        and cdms2 variables (examples for each shown above).
    :type x: numpy.array or numpy.ma.MaskedArray or cdms2 variable

    :return: A boolean value indicating whether the given data is monotonic.
    :rtype: `bool`_
    """
    dx = numpy.diff(x)
    return numpy.all(dx <= 0) or numpy.all(dx >= 0)


def getgraphicsmethod(type, name):
    """Retrieves an existing graphics method, given by type and name.

    :Example:

        .. doctest:: utils_getgraphicsmethod

            >>> vcs.show('boxfill') # list available boxfills
            *******************Boxfill Names List**********************
            ...
            *******************End Boxfill Names List**********************
            >>> vcs.getgraphicsmethod('boxfill','polar') # get polar boxfill
            <vcs.boxfill.Gfb ...>

    :param type: String name of a VCS graphics method type
    :type type: `str`_

    :param name: String name of a VCS graphics method of the given type.
    :type name: `str`_

    :return: A graphics method of the given type and name.
        If such a graphics method doesn't exist, None will be returned.
    :rtype: VCS graphics method or `None`_
    """
    if type == "default":
        type = "boxfill"
    if hasVCSAddons and isinstance(type, vcsaddons.core.VCSaddon):
        func = type.getgm
        copy_mthd = func(name)
    else:
        try:
            copy_mthd = vcs.elements[type][name]
        except BaseException:
            copy_mthd = None
    return copy_mthd


def creategraphicsmethod(gtype, gname='default', name=None):
    """Creates a graphics method of the type given by gtype.

    :Example:

        .. doctest:: utils_creategraphicsmethod

            >>> cgm=vcs.creategraphicsmethod # alias long name
            >>> cgm('Gfm') # meshfill inherits default; name generated
            <vcs.meshfill.Gfm ...>
            >>> cgm('boxfill','polar') # boxfill inherits polar; name generated
            <vcs.boxfill.Gfb ...>
            >>> cgm('Gfi',name='my_gfi') # isofill inherits default; user-named
            <vcs.isofill.Gfi ...>

    :param gtype: String name of the type of graphics method object to create.
    :type gtype: `str`_

    :param gname: String name of the specific graphics method for the new
        graphics method to inherit.
    :type gname: `str`_

    :param name: String name for the new object.
        If None, a unique name will be generated.
    :type name: `str`_ or `None`_

    :return: A graphics method object

    """
    if gtype in ['isoline', 'Gi']:
        func = vcs.createisoline
    elif gtype in ['isofill', 'Gfi']:
        func = vcs.createisofill
    elif gtype in ['boxfill', 'Gfb', 'default']:
        # VCS uses a temporary graphics method type 'default' when the user
        # doesn't specify a graphics method. This gets replaced later down the
        # plotting pipeline, but is important for tracking tick information.
        func = vcs.createboxfill
    elif gtype in ['meshfill', 'Gfm']:
        func = vcs.createmeshfill
    elif gtype in ['scatter', ]:
        func = vcs.createscatter
    elif gtype in ['xvsy', ]:
        func = vcs.createxvsy
    elif gtype in ['xyvsy', ]:
        func = vcs.createxyvsy
    elif gtype in ['yxvsx', ]:
        func = vcs.createyxvsx
    elif gtype in ['1d', 'G1d']:
        func = vcs.create1d
    elif gtype in ['vector', 'Gv']:
        func = vcs.createvector
    elif gtype in ['streamline', 'Gs']:
        func = vcs.createstreamline
    elif gtype in ['taylordiagram', 'Gtd']:
        func = vcs.createtaylordiagram
    elif gtype == '3d_scalar':
        func = vcs.create3d_scalar
    elif gtype == '3d_dual_scalar':
        func = vcs.create3d_dual_scalar
    elif gtype == '3d_vector':
        func = vcs.create3d_vector
    elif hasVCSAddons and isinstance(gtype, vcsaddons.core.VCSaddon):
        func = gtype.creategm
    else:
        raise ValueError("Invalid graphic method type: {}".format(gtype))
    copy_mthd = func(name=name, source=gname)
    return copy_mthd


# Returns the float value for datawc_...
# datawc_ can be a float or a cdtime.reltime
# TODO: Investigate why datawc is converted to a cdtime.reltime
def getDataWcValue(v):
    if (isinstance(v, type(cdtime.reltime(0, 'months since 1900')))):  # noqa
        return v.value
    else:
        return v


def getworldcoordinates(gm, X, Y):
    """Given a graphics method and two axes, calculates correct world coordinates.

    :Example:

        .. doctest:: utils_getworldcoordinates

            >>> import cdms2, os
            >>> if not os.path.exists(vcs.sample_data):
            ...     vcs.download_sample_data_files() # get some data for cdms2
            >>> f=cdms2.open(vcs.sample_data + '/clt.nc')
            >>> v=f('v') # read variable v from clt.nc
            >>> xax=v.getAxis(3) # X axis
            >>> yax=v.getAxis(2) # Y axis
            >>> box=vcs.getboxfill()
            >>> vcs.getworldcoordinates(box, xax, yax)
            [-180.0, 180.0, -88.288399, 88.288399]

    :param gm: A VCS graphics method object to get worldcoordinates for.
    :type gm: graphics method object

    :param X: A cdms2 transient axs
    :type X: cdms2.axis.TransientAxis

    :param Y: A cdms2 transient axs
    :type Y: cdms2.axis.TransientAxis

    :returns: A list of the worldcoordinates associated with the given graphics
        method and axes
    :rtype: `list`_
    """
    # compute the spanning in x and y, and adjust for the viewport
    wc = [0, 1, 0, 1]
    try:
        datawc = [getDataWcValue(gm.datawc_x1), getDataWcValue(gm.datawc_x2),
                  getDataWcValue(gm.datawc_y1), getDataWcValue(gm.datawc_y2)]
        if numpy.isclose(datawc[0], 1.e20):
            try:
                i = 0
                try:
                    while X[:][i].count() == 0:
                        i += 1
                except BaseException:
                    pass
                wc[0] = X[:][i]
            except BaseException:
                wc[0] = X[:].min()
        else:
            wc[0] = datawc[0]
        if numpy.isclose(datawc[1], 1.e20):
            try:
                i = -1
                try:
                    while X[:][i].count() == 0:
                        i -= 1
                except BaseException:
                    pass
                wc[1] = X[:][i]
            except BaseException:
                wc[1] = X[:].max()
        else:
            wc[1] = datawc[1]
    except BaseException:
        return wc
    if (((not isinstance(X, cdms2.axis.TransientAxis) and
          isinstance(Y, cdms2.axis.TransientAxis)) or
         not vcs.utils.monotonic(X[:])) and numpy.allclose([datawc[0], datawc[1]], 1.e20)):
        wc[0] = X[:].min()
        wc[1] = X[:].max()
    if numpy.isclose(datawc[2], 1.e20):
        try:
            i = 0
            try:
                while Y[:][i].count() == 0:
                    i += 1
            except Exception:
                pass
            wc[2] = Y[:][i]
        except BaseException:
            wc[2] = Y[:].min()
    else:
        wc[2] = datawc[2]
    if numpy.isclose(datawc[3], 1.e20):
        try:
            i = -1
            try:
                while Y[:][i].count() == 0:
                    i -= 1
            except BaseException:
                pass
            wc[3] = Y[:][i]
        except BaseException:
            wc[3] = Y[:].max()
    else:
        wc[3] = datawc[3]
    if (((not isinstance(Y, cdms2.axis.TransientAxis) and
          isinstance(X, cdms2.axis.TransientAxis)) or not vcs.utils.monotonic(Y[:])) and
        numpy.allclose([datawc[2], datawc[3]], 1.e20)) \
            or (hasattr(gm, "projection") and
                vcs.elements["projection"][
                gm.projection].type.lower().split()[0]
                not in ["linear", "polar"] and
                numpy.allclose([datawc[2], datawc[3]], 1.e20) and
                numpy.allclose([datawc[0], datawc[1]], 1.e20)):
        wc[2] = Y[:].min()
        wc[3] = Y[:].max()
    if wc[3] == wc[2]:
        wc[2] -= .0001
        wc[3] += .0001
    if numpy.allclose(wc[0], wc[1]):
        wc[0] -= .0001
        wc[1] += .0001
    return wc


def rgba_color(color, colormap):
    """Try all of the various syntaxes of colors and return 0-100 RGBA values.

    :Example:

        .. doctest:: utils_rbga_color

            >>> cp = vcs.getcolormap() # Get a copy of the default colormap
            >>> vcs.rgba_color('black', cp) # Find the rgba equivalent for black
            [0.0, 0.0, 0.0, 100]


    :param color: The color to get the rgba value for. Can be an integer from 0-255, or a string name of a color.
    :type color: `int`_ or `str`_

    :param colormap: A VCS colormap
    :type colormap: vcs.colormap.Cp

    :returns: List of 4 floats; the R, G, B, and A values associated with the given color.
    :rtype: `list`_
    """
    try:
        # Is it a colormap index?
        return colormap.index[color]
    except ValueError:
        # Is it a color tuple?
        if len(color) == 3 or len(color) == 4:
            for c in color:
                try:
                    int(c)
                except BaseException:
                    break
            else:
                if any((c > 100 for c in color)):
                    r, g, b = (c / 2.55 for c in color[0:3])
                    if len(color) == 4:
                        a = color[-1] / 2.55
                    else:
                        a = 100
                else:
                    r, g, b = color[:3]
                    if len(color) == 4:
                        a = color[-1]
                    else:
                        a = 100
                return [r, g, b, a]
    r, g, b = genutil.colors.str2rgb(color)
    return [r / 2.55, g / 2.55, b / 2.55, 100]


def png_read_metadata(path):
    reader = vtk.vtkPNGReader()
    reader.SetFileName(path)
    reader.Update()
    numberOfTextChunks = reader.GetNumberOfTextChunks()
    m = {}
    for i in range(0, numberOfTextChunks):
        m[reader.GetTextKey(i)] = reader.GetTextValue(i)
    return m


def download_sample_data_files(path=None):
    """Downloads sample data to be used with VCS.
    Default download directory is vcs.sample_data, but if __path__ is provided
    then data will be downloaded to that path.

    :Example:

        .. doctest:: utils_download_sample_data

            >>> import os # use this to check if sample data already exists
            >>> if not os.path.isdir(vcs.sample_data):
            ...     vcs.download_sample_data_files()

    :param path: String of a valid filepath.
        If None, sample data will be downloaded into the
        vcs.sample_data directory.
    :type path: `str`_ or `None`_
    """
    if path is None:
        path = vcs.sample_data
    import cdat_info
    import sys
    cdat_info.download_sample_data_files(
        os.path.join(
            sys.prefix,
            "share",
            "vcs",
            "sample_files.txt"),
        path)


def drawLinesAndMarkersLegend(canvas, templateLegend,
                              linecolors, linetypes, linewidths,
                              markercolors, markertypes, markersizes,
                              strings, scratched=None, stringscolors=None,
                              stacking="horizontal", bg=False, render=True,
                              smallestfontsize=None, backgroundcolor=None):
    """Draws a legend with line/marker/text inside a template legend box
    Auto adjust text size to make it fit inside the box
    Auto arrange the elements to fill the box nicely

    :Example:

        .. doctest:: utils_drawLinesAndMarkersLegend

            >>> import vcs
            >>> x = vcs.init()
            >>> t = vcs.createtemplate()
            >>> vcs.utils.drawLinesAndMarkersLegend(x,t.legend,
            ...     ["red","blue","green"], ["solid","dash","dot"],[1,4,8],
            ...     ["blue","green","red"], ["cross","square","dot"],[3,4,5],
            ...     ["sample A","type B","thing C"], bg=True)
            >>> x.png("sample")

    :param canvas: a VCS canvas object onto which to draw the legend
    :type canvas: vcs.Canvas.Canvas

    :param templateLegend: a template legend object used to determine the
        coordinates of the box and the box line type
    :type legendTemplate: vcs.Plegend.Pls

    :param linecolors: list containing the colors of each line to draw.
         Colors must be specified as either integers, (r,g,b,opacity),
         or string color names.
    :type linecolors: `list`_

    :param linetypes: list containing the type of each line to draw.
         values must be int or line type strings
    :type linetypes: `list`_

    :param linewidths: list containing each line width.
        line widths must be of type float.
    :type linewidths: `list`_

    :param markercolors: list of the markers colors to draw.
        Colors must be specified as either integers, (r,g,b,opacity),
        or string color names.
    :type markercolors: `list`_

    :param markertypes: list of the marker types to draw.
         Marker type must be int or string of marker type names.
    :type markertypes: `list`_

    :param markersizes: list of the size of each marker to draw.
        marker size must be of type float.
    :type markersizes: `list`_

    :param strings: list of the string to draw next to each line/marker
    :type strings: `list`_

    :param scratched: None (off) or list. list contains False where no scratch is
        needed. For scratched, provide True or line type to use for scratch.
        Color will match that of text.
    :type scratched: `None`_ or `list`_

    :param stringscolors: A list of the strings colors to draw.
        Colors are represented as either an int from 0-255, an rgba tuple,
        or a string color name.
    :type stringscolors: `list`_

    :param stacking: Prefered direction to stack element ('horizontal' or 'vertical')
    :type stringscolors: `string`_

    :param bg: Boolean value indicating to draw in background (True),
        Or foreground (False).
    :type bg: `bool`_

    :param render: Boolean value indicating whether or not to render the new
        lines and markers.
    :type render: `bool`_

    :param smallestfontsize: Integer value indicating the smallest font size we can use for rendering
        None means no limit, 0 means use original size. Downscaling will still be used by algorigthm
        to try to fit everything in the legend box.
    :type smallestfintsize: `int`_

    :param backgroundcolor: A list indicating the background color of the legended box.
            Colors are represented as either an int from 0-255, an rgba tuple,
            or a string color name.
        :type markercolors: `list`_
    """
    # backgroundcolor
    if backgroundcolor is not None:
        # Adding a fill area above the legends
        fa = canvas.createfillarea()
        fa.x = [[templateLegend.x1, templateLegend.x2, templateLegend.x2, templateLegend.x1, templateLegend.x1]]
        fa.y = [[templateLegend.y1, templateLegend.y1, templateLegend.y2, templateLegend.y2, templateLegend.y1]]
        fa.style = ["solid"]
        fa.color = backgroundcolor
        canvas.plot(fa)

    nlines = len(linecolors)
    # Now figures out the widest string and tallest
    text = vcs.createtext(To_source=templateLegend.textorientation,
                          Tt_source=templateLegend.texttable)
    text.x = .5
    text.y = .5
    maxx = 0  # Max number of elts on X direction
    maxy = 0  # Max number of elts on Y direction
    dx = abs(templateLegend.x2 - templateLegend.x1)
    dy = abs(templateLegend.y2 - templateLegend.y1)

    nolines = True
    for lwidth in linewidths:
        nolines = nolines and lwidth == 0.

    originalFontSize = text.height

    # Loop until we can fit all elts into the box
    while maxx * maxy < nlines:
        maxwidth = 0
        maxheight = 0
        for i in range(nlines):
            text.string = strings[i]
            ext = canvas.gettextextent(text)[0]
            maxwidth = max(maxwidth, ext[1] - ext[0])
            maxheight = max(maxheight, ext[3] - ext[2])
        if nolines:
            leg_lines = 0.
            leg_spc = .015
        elif len(strings[i]) > 4:
            leg_lines = maxwidth / 3.
            leg_spc = leg_lines / 3.
        else:
            leg_lines = maxwidth
            leg_spc = leg_lines / 3.
        maxwidth = maxwidth + leg_lines + leg_spc
        maxx = int(dx / maxwidth)
        maxy = int(dy / maxheight)
        if maxx * maxy < nlines:
            # Does not fit less shrink the text a bit
            text.height -= 1
        if text.height == 0:
            # Oh well it cannot fit...
            # We settle for the smallest size
            text.height = 1
            break

    # Check if we had some user imposed limitation on font size
    if smallestfontsize is not None:
        if smallestfontsize == 0:
            text.height = originalFontSize
        else:
            text.height = smallestfontsize

    if stacking[:3].lower() == "hor":
        nH = min(maxx, len(strings))  # How many elts on horizontal direction
        nV = numpy.ceil(nlines / float(nH))  # How many elts vertically
    else:
        nV = min(maxy, len(strings))  # How many elts on horizontal direction
        nH = numpy.ceil(nlines / float(nV))  # How many elts vertically
    spcX = (dx - maxwidth * nH) / (nH + 1)
    spcY = (dy - maxheight * nV) / (nV + 1)
    txs = []
    tys = []
    ts = []
    x1 = min(templateLegend.x1, templateLegend.x2)
    y1 = max(templateLegend.y1, templateLegend.y2)
    # Box around legend area
    ln = canvas.createline(source=templateLegend.line)
    ln.x = [
        templateLegend.x1,
        templateLegend.x2,
        templateLegend.x2,
        templateLegend.x1,
        templateLegend.x1]
    ln.y = [
        templateLegend.y1,
        templateLegend.y1,
        templateLegend.y2,
        templateLegend.y2,
        templateLegend.y1]
    canvas.plot(ln, bg=bg, render=render)

    # Create the objects
    for i in range(len(strings)):
        col = int(i % nH)
        row = int(i / nH)
        # TODO check if previous line was identical
        # so that we create less objet/renderers
        ln = canvas.createline()
        ln.color = [linecolors[i], ]
        if linewidths[i] > 0:
            ln.width = linewidths[i]
            ln.priority = templateLegend.priority
        else:
            ln.priority = 0
        ln.type = linetypes[i]
        # TODO check if previous marker was identical
        # so that we create less objet/renderers
        mrk = canvas.createmarker()
        mrk.color = [markercolors[i]]
        mrk.type = markertypes[i]
        if markersizes[i] > 0:
            mrk.size = markersizes[i]
            mrk.priority = templateLegend.priority
        else:
            mrk.priority = 0
        xs = x1 + spcX + col * (maxwidth + spcX)
        ln.x = [xs, xs + leg_lines]
        mrk.x = [xs + leg_lines / 2.]
        txs.append(xs + leg_lines + leg_spc)
        ts.append(strings[i])
        ys = y1 - row * (maxheight + spcY) - spcY - maxheight / 2.
        ln.y = [ys, ys]
        mrk.y = [ys]
        tys.append(ys)
        if scratched is not None and scratched[i] is not False:
            scratch = canvas.createline(source=ln.name)
            scratch.width = scratch.width[0] * 2.
            scratch.color = [text.color]
            scratch.type = scratched[i]
            text.string = strings[i]
            ext = canvas.gettextextent(text)[0]
            scratch.x = [txs[-1], txs[-1] + ext[1] - ext[0]]
            scratch.priority = text.priority + 1
            if scratch.priority != 1:
                canvas.plot(scratch, bg=bg, render=render)
        canvas.plot(ln, bg=bg, render=render)
        canvas.plot(mrk, bg=bg, render=render)
    text.halign = "left"
    text.valign = "half"
    text.string = ts
    text.priority = templateLegend.priority
    if stringscolors is None:
        text.x = txs
        text.y = tys
        canvas.plot(text, bg=bg, render=render)
    else:
        for i in range(len(strings)):
            txt = vcs.createtext(
                Tt_source=text.Tt_name,
                To_source=text.To_name)
            txt.x = txs[i]
            txt.y = tys[i]
            txt.color = stringscolors[i]
            txt.string = strings[i]
            canvas.plot(txt, bg=bg, render=render)


def _createLegendString(value, unit):
    """
    Creates a label "value unit"
    """
    legendString = "%.4g" % value
    if (unit):
        legendString += (" " + unit)
    return legendString


def drawVectorLegend(canvas, templateLegend,
                     linecolor, linetype, linewidth,
                     unitString, maxNormInVp=1., maxNorm=1.,
                     minNormInVp=0., minNorm=0., bg=False, render=True):
    """Draws a legend with vector line/text inside a template legend box
    Auto adjust text size to make it fit inside the box

    :Example:

        .. doctest:: utils_drawVectorLegend

            >>> import vcs
            >>> x = vcs.init()
            >>> t = vcs.createtemplate()
            >>> vcs.utils.drawVectorLegend(x,t.legend,
            ...     "red", "solid", 1, "sample A", bg=True)

    :param canvas: a VCS canvas object onto which to draw the legend
    :type canvas: vcs.Canvas.Canvas

    :param templateLegend: a template legend object used to determine the
        coordinates of the box and the box line type
    :type legendTemplate: vcs.Plegend.Pls

    :param linecolor: color of vector to draw.
         The color must be specified as either integers, (r,g,b,opacity),
         or string color name.
    :type linecolor: `string`_

    :param linetype: type of the vector line to draw.
         values must be int or line type string
    :type linetype: `string`_

    :param linewidth: vector line width.
        line width must be of type float.
    :type linewidth: `string`_

    :param unitString: unit for maxNorm
    :type unitString: `string`_

    : param maxNormInVp: maxNorm in viewport coordinates
    : type maxNormInVp: `float`_

    : param maxNorm: maxNorm in world coordinates
    : type maxNorm: `float`_

    : param minNormInVp: minNorm in viewport coordinates. If None, we don't
                         to show minNorm legend
    : type minNormInVp: `float`_

    : param minNorm: minNorm in world coordinates
    : type minNorm: `float`_

    :param bg: Boolean value indicating to draw in background (True),
        Or foreground (False).
    :type bg: `bool`_

    :param render: Boolean value indicating whether or not to render the new
        lines.
    :type render: `bool`_
    """

    # Figure out space length
    text = vcs.createtext(To_source=templateLegend.textorientation,
                          Tt_source=templateLegend.texttable)
    text.x = .5
    text.y = .5
    maxLegendString = _createLegendString(maxNorm, unitString)
    text.string = maxLegendString
    maxExt = canvas.gettextextent(text)[0]

    minLegendString = _createLegendString(minNorm, unitString)
    text.string = minLegendString
    minExt = canvas.gettextextent(text)[0]

    # space between line and label - one character long
    spaceLength = (maxExt[1] - maxExt[0]) / len(maxLegendString)
    # line vector - min 2 and max 15 characters long
    minMaxNormLineLength = 2 * spaceLength
    maxMaxNormLineLength = 15 * spaceLength
    # clamp lineLegth between 2 and 15 spaceLength
    maxLineLength = maxNormInVp
    minLineLength = minNormInVp
    ratio = 1.0
    if (maxLineLength < minMaxNormLineLength):
        while (maxLineLength < minMaxNormLineLength):
            maxLineLength *= 2
            ratio *= 2
    elif (maxLineLength > maxMaxNormLineLength):
        while (maxLineLength > maxMaxNormLineLength):
            maxLineLength /= 2
            ratio /= 2

    # update maxLegendString with the clamped value
    if (ratio != 1):
        maxLegendString = _createLegendString(maxNorm * ratio, unitString)
        text.string = maxLegendString
        maxExt = canvas.gettextextent(text)[0]

    maxLegendLength = maxExt[1] - maxExt[0]
    maxheight = maxExt[3] - maxExt[2]

    maxLegendLength = maxLegendLength + maxLineLength + spaceLength
    minLegendLength = minExt[1] - minExt[0]
    if (minNormInVp):
        minLegendLength = minLegendLength + minLineLength + spaceLength

    dy = abs(templateLegend.y2 - templateLegend.y1)
    spcY = (dy - maxheight) / 2
    y1 = max(templateLegend.y1, templateLegend.y2)

    txs = []
    tys = []
    ts = []
    n = 1
    if (minNormInVp):
        n = 2
    legendLength = [maxLegendLength, minLegendLength]
    legendString = [maxLegendString, minLegendString]
    lineLength = [maxLineLength, minLineLength]
    for i in range(n):
        # vector stem
        ln = canvas.createline()
        ln.color = [linecolor, ]
        ln.type = linetype
        ln.width = linewidth
        ln.priority = templateLegend.priority
        if (minNormInVp):
            xs = (templateLegend.x1 + templateLegend.x2) * \
                (2 - i) / 3 - legendLength[i] / 2
        else:
            xs = (templateLegend.x1 + templateLegend.x2) / \
                2 - legendLength[i] / 2
        ln.x = [xs, xs + lineLength[i]]
        ys = y1 - spcY - maxheight / 2.
        ln.y = [ys, ys]
        canvas.plot(ln, bg=bg, render=render)
        # vector head
        ln.x = [xs + lineLength[i] * 0.7, xs + lineLength[i]]
        ln.y = [ys - lineLength[i] * 0.1, ys]
        canvas.plot(ln, bg=bg, render=render)
        ln.x = [xs + lineLength[i] * 0.7, xs + lineLength[i]]
        ln.y = [ys + lineLength[i] * 0.1, ys]
        canvas.plot(ln, bg=bg, render=render)

        # string legend
        text.halign = "left"
        text.valign = "half"
        ts.append(legendString[i])
        text.string = ts
        txs.append(xs + lineLength[i] + spaceLength)
        tys.append(ys)
        text.x = txs
        text.y = tys
        text.priority = templateLegend.priority

    canvas.plot(text, bg=bg, render=render)
