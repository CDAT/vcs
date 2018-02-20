"""
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

    .. pragma: skip-doctest
"""
from __future__ import print_function
import vcs
from . import boxfill
from . import meshfill
from . import isofill
from . import isoline
from . import unified1D
from . import template
from . import projection
from . import colormap
from . import fillarea
from . import marker
from . import line
from . import texttable
from . import textorientation
from . import textcombined
from . import vector
from . import streamline
from . import xmldocs
import random
from .error import vcsError
import warnings
from . import dv3d
import os

try:
    basestring
except NameError:
    basestring = str


def reset(gtype=None):
    """Remove all user generated objects

#    :Example:
#
#        .. doctest:: manageElements_reset
#
#            >>> vcs.reset()
#            >>> vcs.reset("boxfill")
#            >>> vcs.reset(["isofill", "template"])


    :param gtype: String or list of stringsname of a VCS object type.
        (e.g. 'boxfill', 'isofill', 'marker', etc.)
    :type typ: str

    :returns: None
    :rtype: None
    """

    if gtype is None:
        gtype = vcs.listelements()
    elif isinstance(gtype, basestring):
        if gtype not in vcs.listelements():
            raise ValueError("invalid element type: {}".format(gtype))
        gtype = [gtype, ]

    for typ in gtype:
        elements = vcs.listelements(typ)
        for e in elements:
            if e not in vcs._protected_elements[typ]:
                if typ in ["scatter", "xvsy", "xyvsy", "yxvsx"]:
                    vcs.removeG(e, "1d")
                else:
                    vcs.removeobject(vcs.elements[typ][e])

    _dotdir, _dotdirenv = vcs.getdotdirectory()
    user_init = os.path.join(
        os.path.expanduser("~"),
        _dotdir,
        'initial.attributes')
    if os.path.exists(user_init):
        vcs.scriptrun(user_init)


def check_name_source(name, source, typ):
    """Make sure it is a unique name for this type or generates a name for user.

    :Example:

        .. doctest:: manageElements_check_name_source

            >>> cns=vcs.check_name_source # alias for long function name
            >>> vcs.show('boxfill')
            *******************Boxfill Names List**********************
            ...
            *******************End Boxfill Names List**********************
            >>> cns('NEW', 'quick', 'boxfill') # name 'NEW' should be available
            ('NEW', 'quick')
            >>> cns(None, 'default', 'boxfill') # generate unique boxfill name
            ('__boxfill_...', 'default')

    :param name: Desired string name for an object of type *typ*,
        inheriting from source object *source*.
        If name is None, a unique name will be generated.
    :type name: `str`_ or None

    :param source: Source from which the new object is meant to inherit.
        Can be a VCS object or a string name of a VCS object.
    :type source: `str`_ or VCS Object

    :param typ: String name of a VCS object type.
        (e.g. 'boxfill', 'isofill', 'marker', etc.)
    :type typ: str

    :returns: A tuple containing two strings: a unique name and a source name.
        If *name* was provided and an object of type *typ* with that name
        already exists, an error is raised.
    :rtype: `tuple`_
    """
    elts = vcs.listelements(typ)
    if name is None:
        rnd = random.randint(0, 1000000000000000)
        name = '__%s_%i' % (typ, rnd)
        while name in elts:
            rnd = random.randint(0, 1000000000000000)
            name = '__%s_%i' % (typ, rnd)
    if isinstance(name, basestring):
        name = str(name)
    if not isinstance(name, basestring):
        raise vcsError(
            '%s object name must be a string or %s name' %
            (typ, typ))

    if not isinstance(source, basestring):
        loc = locals()
        exec("ok = vcs.is%s(source)" % (typ,))
        ok = loc["ok"]
    else:
        ok = 0
    if (not isinstance(source, basestring)) and ok == 0:
        raise vcsError(
            'Error %s object source must be a string or a %s object' %
            (typ, typ))
    elif ok:
        source = source.name

    if name in elts:
        raise vcsError("Error %s object named %s already exists" % (typ, name))
    if source not in elts and typ != "display":
        raise vcsError(
            "Error source %s object (%s) does not exist!" %
            (typ, source))
    return name, source


def createtemplate(name=None, source='default'):
    """%s

    :param name: The name of the created object
    :type name: `str`_

    :param source: The object to inherit from.
        Can be a template, or a string name of a template
    :type source: `str`_ or :class:`vcs.template.P`

    :returns: A template
    :rtype: vcs.template.P

    """
    name, source = check_name_source(name, source, 'template')

    return template.P(name, source)
createtemplate.__doc__ = createtemplate.__doc__ % xmldocs.create_docs['template']  # noqa


def gettemplate(Pt_name_src='default'):
    """%s

    :param Pt_name_src: String name of an existing template VCS object
    :type Pt_name_src: `str`_

    :returns: A VCS template object
    :rtype: vcs.template.P
    """
    # Check to make sure the argument passed in is a STRING
    if not isinstance(Pt_name_src, basestring):
        raise vcsError('The argument must be a string.')

    if Pt_name_src not in list(vcs.elements["template"].keys()):
        raise ValueError("template '%s' does not exists" % Pt_name_src)
    return vcs.elements["template"][Pt_name_src]
gettemplate.__doc__ = gettemplate.__doc__ % xmldocs.get_docs['template']  # noqa


def createprojection(name=None, source='default'):
    """%s

    :param name: The name of the created object
    :type name: `str`_

    :param source: The object to inherit from.
        Can be a projection, or a string name of a projection.
    :type source: `str`_ or :class:`vcs.projection.Proj`

    :returns: A projection graphics method object
    :rtype: vcs.projection.Proj
    """

    name, source = check_name_source(name, source, 'projection')
    return projection.Proj(name, source)
createprojection.__doc__ = createprojection.__doc__ % xmldocs.create_docs['projection']  # noqa


def getprojection(Proj_name_src='default'):
    """%s

    :param Proj_name_src: String name of an existing VCS projection object
    :type Proj_name_src: `str`_

    :returns: A VCS projection object
    :rtype: vcs.projection.Proj
    """

    # Check to make sure the argument passed in is a STRING
    if not isinstance(Proj_name_src, basestring):
        raise vcsError('The argument must be a string.')

    if Proj_name_src not in vcs.elements["projection"]:
        raise vcsError("No such projection '%s'" % Proj_name_src)
    return vcs.elements["projection"][Proj_name_src]
getprojection.__doc__ = getprojection.__doc__ % xmldocs.get_docs['projection']  # noqa


def createboxfill(name=None, source='default'):
    """%s

    :param name: The name of the created object
    :type name: `str`_

    :param source: The object to inherit from.
        can be a boxfill, or a string name of a boxfill.
    :type source: `str`_ or :class:`vcs.boxfill.Gfb`

    :return: A boxfill graphics method object
    :rtype: vcs.boxfill.Gfb
    """

    name, source = check_name_source(name, source, 'boxfill')
    return boxfill.Gfb(name, source)
createboxfill.__doc__ = createboxfill.__doc__ % xmldocs.create_docs['boxfill']  # noqa


def getboxfill(Gfb_name_src='default'):
    """%s

    :param Gfb_name_src: String name of an existing boxfill VCS object
    :type Gfb_name_src: `str`_

    :return: A pre-existing boxfill graphics method
    :rtype: vcs.boxfill.Gfb
    """
    # Check to make sure the argument passed in is a STRING
    if not isinstance(Gfb_name_src, basestring):
        raise vcsError('The argument must be a string.')

    if Gfb_name_src not in list(vcs.elements["boxfill"].keys()):
        raise Exception("The boxfill method: '%s' does not seem to exist")
    return vcs.elements["boxfill"][Gfb_name_src]
getboxfill.__doc__ = getboxfill.__doc__ % xmldocs.get_docs['boxfill']  # noqa


def createtaylordiagram(name=None, source='default'):
    """%s

    :param name: The name of the created object
    :type name: `str`_

    :param source: The object to inherit from.
        Can be a a taylordiagram, or a string name of a taylordiagram.
    :type source: `str`_ or :class:`vcs.taylor.Gtd`

    :returns: A taylordiagram graphics method object
    :rtype: vcs.taylor.Gtd
    """

    name, source = check_name_source(name, source, 'taylordiagram')
    if name in list(vcs.elements["taylordiagram"].keys()):
        raise vcsError(
            'Error creating taylordiagram graphic method: ' +
            name +
            ' already exist')
    if source not in list(vcs.elements["taylordiagram"].keys()):
        raise vcsError(
            'Error creating taylordiagram graphic method ' +
            source +
            ' does not exist')
    n = vcs.taylor.Gtd(name, source)
    return n
createtaylordiagram.__doc__ = createtaylordiagram.__doc__ % xmldocs.create_docs['taylordiagram']  # noqa


def gettaylordiagram(Gtd_name_src='default'):
    """%s

    :param Gtd_name_src: String name of an existing taylordiagram VCS object
    :type Gtd_name_src: `str`_

    :returns: A taylordiagram VCS object
    :rtype: vcs.taylor.Gtd
    """

    # Check to make sure the argument passed in is a STRING
    if not isinstance(Gtd_name_src, basestring):
        raise vcsError('The argument must be a string.')

    if Gtd_name_src not in list(vcs.elements["taylordiagram"].keys()):
        raise vcsError(
            "The taylordiagram graphic method %s does not exists" %
            Gtd_name_src)
    else:
        return vcs.elements["taylordiagram"][Gtd_name_src]
gettaylordiagram.__doc__ = gettaylordiagram.__doc__ % xmldocs.get_docs['taylordiagram']  # noqa


def createmeshfill(name=None, source='default'):
    """%s

    :param name: The name of the created object
    :type name: `str`_

    :param source: The object to inherit from.
        Can be a meshfill, or a string name of a meshfill.
    :type source: `str`_ or :class:`vcs.meshfill.Gfm`

    :returns: A meshfill graphics method object
    :rtype: vcs.meshfill.Gfm
    """
    name, source = check_name_source(name, source, 'meshfill')
    return meshfill.Gfm(name, source)
createmeshfill.__doc__ = createmeshfill.__doc__ % xmldocs.create_docs['meshfill']  # noqa


def getmeshfill(Gfm_name_src='default'):
    """%s

    :param Gfm_name_src: String name of an existing meshfill VCS object
    :type Gfm_name_src: `str`_

    :returns: A meshfill VCS object
    :rtype: vcs.meshfill.Gfm
    """

    # Check to make sure the argument passed in is a STRING
    if not isinstance(Gfm_name_src, basestring):
        raise vcsError('The argument must be a string.')

    if Gfm_name_src not in vcs.elements["meshfill"]:
        raise ValueError("meshfill '%s' does not exists" % Gfm_name_src)

    return vcs.elements["meshfill"][Gfm_name_src]
getmeshfill.__doc__ = getmeshfill.__doc__ % xmldocs.get_docs['meshfill']  # noqa


def createisofill(name=None, source='default'):
    """%s

    :param name: The name of the created object
    :type name: `str`_

    :param source: The object to inherit from.
        Can be an isofill object, or string name of an isofill object.
    :type source: `str`_ or :class:`vcs.isofill.Gfi`

    :returns: An isofill graphics method
    :rtype: vcs.isofill.Gfi
    """

    name, source = check_name_source(name, source, 'isofill')
    return isofill.Gfi(name, source)
createisofill.__doc__ = createisofill.__doc__ % xmldocs.create_docs['isofill']  # noqa


def getisofill(Gfi_name_src='default'):
    """%s

    :param Gfi_name_src: String name of an existing isofill VCS object
    :type Gfi_name_src: `str`_

    :returns: The specified isofill VCS object
    :rtype: vcs.isofill.Gfi
    """

    # Check to make sure the argument passed in is a STRING
    if not isinstance(Gfi_name_src, basestring):
        raise vcsError('The argument must be a string.')

    if Gfi_name_src not in vcs.elements["isofill"]:
        raise ValueError("The isofill '%s' does not exists" % Gfi_name_src)
    return vcs.elements["isofill"][Gfi_name_src]
getisofill.__doc__ = getisofill.__doc__ % xmldocs.get_docs['isofill']  # noqa


def createisoline(name=None, source='default'):
    """%s

    :param name: The name of the created object
    :type name: `str`_

    :param source: The object to inherit from.
        Can be an isoline object, or string name of an isoline object.
    :type source: `str`_ or :class:`vcs.isoline.Gi`

    :returns: An isoline graphics method object
    :rtype: vcs.isoline.Gi
    """

    name, source = check_name_source(name, source, 'isoline')
    return isoline.Gi(name, source)
createisoline.__doc__ = createisoline.__doc__ % xmldocs.create_docs['isoline']  # noqa


def getisoline(Gi_name_src='default'):
    """%s

    :param Gi_name_src: String name of an existing isoline VCS object
    :type Gi_name_src: `str`_

    :returns: The requested isoline VCS object
    :rtype: vcs.isoline.Gi
    """

    # Check to make sure the argument passed in is a STRING
    if not isinstance(Gi_name_src, basestring):
        raise vcsError('The argument must be a string.')
    if Gi_name_src not in vcs.elements["isoline"]:
        raise ValueError("The isoline '%s' does not exists" % Gi_name_src)
    return vcs.elements["isoline"][Gi_name_src]
getisoline.__doc__ = getisoline.__doc__ % xmldocs.get_docs['isoline']  # noqa


def create1d(name=None, source='default'):
    """Creates a new :py:class:`vcs.unified1d.G1d` object called name, and inheriting from source.

    :Example:

        .. doctest:: manageElements_create1d

            >>> vcs.show('1d')
            *******************1d Names List**********************
            ...
            *******************End 1d Names List**********************
            >>> vcs.create1d() # inherits default, name generated
            <vcs.unified1D.G1d ...>
            >>> vcs.create1d("one_D") # inherits default, name "one_D"
            <vcs.unified1D.G1d ...>
            >>> vcs.create1d(source="one_D") # inherits from "one_D"
            <vcs.unified1D.G1d ...>

    :param name: A string name for the 1d to be created. If None, a unique name will be created.
    :type name: `str`_

    :param source: A 1d object or string name of a 1d object from which the new 1d will inherit.
    :type source: `str`_ or :py:class:`vcs.unified1D.G1d`

    :return: A new 1d object, inheriting from source.
    :rtype: :py:class:`vcs.unified1D.G1d`
    """
    name, source = check_name_source(name, source, '1d')
    return unified1D.G1d(name, source)


def get1d(name):
    """Given name, returns a :py:class:`vcs.unified1d.G1d` from vcs with that name.
    Unlike other VCS 'get' functions, name cannot be None when calling get1d().

    :Example:

        .. doctest:: manageElements_get_1d

            >>> vcs.show('1d')
            *******************1d Names List**********************
            ...
            *******************End 1d Names List**********************
            >>> vcs.get1d('blue_yxvsx')
            <vcs.unified1D.G1d ...>

    :param name: String name of a 1d in vcs. If there is no 1d with that name, an error will be raised.
    :type name: `str`_

    :return: A 1d from vcs with the given name.
    :rtype: :py:class:`vcs.unified1d.G1d`
    """
    # Check to make sure the argument passed in is a STRING
    if not isinstance(name, basestring):
        raise vcsError('The argument must be a string.')

    if name not in vcs.elements["1d"]:
        raise ValueError("The 1d '%s' graphics method does not exists" % name)
    return vcs.elements["1d"][name]


def createxyvsy(name=None, source='default'):
    """%s

    :param name: The name of the created object
    :type name: `str`_


    :param source: The object to inherit from.
        Can be a xyvsy, or a string name of a xyvsy.
    :type source: `str`_ or :class:`vcs.unified1D.G1d`

    :returns: A XYvsY graphics method object
    :rtype: vcs.unified1D.G1d
    """
    try:
        gm = vcs.create1d(name, source)
    except vcsError as ve:
        if ve.message == "Error 1d object named %s already exists" % name:
            warning_message = "A 1D graphics method named %s already exists, creating yours as %s" % (name,
                                                                                                      name + "_xyvsy")
            warnings.warn(warning_message)
            gm = vcs.create1d(name + "_xyvsy", source)
        else:
            raise ve
    gm.flip = True
    return gm
createxyvsy.__doc__ = createxyvsy.__doc__ % xmldocs.create_docs['xyvsy']  # noqa


def getxyvsy(GXy_name_src='default'):
    """%s

    :param GXy_name_src: String name of an existing Xyvsy graphics method
    :type GXy_name_src: `str`_

    :returns: An XYvsY graphics method object
    :rtype: vcs.unified1D.G1d
    """
    gm = vcs.get1d(GXy_name_src)
    if gm.g_type != "xyvsy":
        # Already existed when name_src was created, most likely
        return vcs.get1d(GXy_name_src + "_xyvsy")
    return gm
getxyvsy.__doc__ = getxyvsy.__doc__ % xmldocs.get_docs['xyvsy']  # noqa


def createyxvsx(name=None, source='default'):
    """%s

    :param name: The name of the created object
    :type name: `str`_

    :param source: The object to inherit from.
        Can be a yxvsy, or a string name of a yxvsy.
    :type source: `str`_ or :class:`vcs.unified1D.G1d`

    :returns: A YXvsX graphics method object
    :rtype: vcs.unified1D.G1d
    """
    try:
        gm = vcs.create1d(name, source)
    except vcsError as ve:
        if ve.message == "Error 1d object named %s already exists" % name:
            warning_message = "A 1D graphics method named %s already exists, creating yours as %s" % (name,
                                                                                                      name + "_yxvsx")
            warnings.warn(warning_message)
            gm = vcs.create1d(name + "_yxvsx", source)
        else:
            raise ve
    return gm
createyxvsx.__doc__ = createyxvsx.__doc__ % xmldocs.create_docs['yxvsx']  # noqa


def getyxvsx(GYx_name_src='default'):
    """%s

    :param GYx_name_src: String name of an existing Yxvsx graphics method
    :type GYx_name_src: str

    :return: A Yxvsx graphics method object
    :rtype: vcs.unified1D.G1d
    """
    gm = vcs.get1d(GYx_name_src)
    if gm.g_type != "yxvsx":
        return vcs.get1d(GYx_name_src + "_yxvsx")
    return gm
getyxvsx.__doc__ = getyxvsx.__doc__ % xmldocs.get_docs['yxvsx']  # noqa


def createxvsy(name=None, source='default'):
    """%s

    :param name: The name of the created object
    :type name: `str`_

    :param source: The object to inherit from.
        Can be a xvsy, or a string name of a xvsy.
    :type source: `str`_ or :class:`vcs.unified1D.G1d`

    :returns: A XvsY graphics method object
    :rtype: vcs.unified1D.G1d
    """
    try:
        gm = vcs.create1d(name, source)
    except vcsError as ve:
        if ve.message == "Error 1d object named %s already exists" % name:
            warning_message = "A 1D graphics method named %s already exists, creating yours as %s" % (name,
                                                                                                      name + "_xvsy")
            warnings.warn(warning_message)
            gm = vcs.create1d(name + "_xvsy", source)
        else:
            raise ve
    return gm
createxvsy.__doc__ = createxvsy.__doc__ % xmldocs.create_docs['xvsy']  # noqa


def getxvsy(GXY_name_src='default'):
    """%s

    :param GXY_name_src: String name of a 1d graphics method
    :type GXY_name_src: `str`_

    :returns: A XvsY graphics method object
    :rtype: vcs.unified1D.G1d
    """
    gm = vcs.get1d(GXY_name_src)
    # Deliberately yxvsx here; xvsy is just an alias
    if gm.g_type != "yxvsx":
        return vcs.get1d(GXY_name_src + "_xvsy")
    return gm
getxvsy.__doc__ = getxvsy.__doc__ % xmldocs.get_docs['xvsy']  # noqa


def createvector(name=None, source='default'):
    """%s

    :param name: The name of the created object
    :type name: `str`_

    :param source: The object to inherit from.
        Can be a vector, or a string name of a vector.
    :type source: `str`_ or :class:`vcs.vector.Gv`

    :returns: A vector graphics method object
    :rtype: vcs.vector.Gv
    """
    name, source = check_name_source(name, source, 'vector')
    return vector.Gv(name, source)
createvector.__doc__ = createvector.__doc__ % xmldocs.create_docs['vector']  # noqa


def getvector(Gv_name_src='default'):
    """%s

    :param Gv_name_src: String name of an existing vector VCS object
    :type Gv_name_src: `str`_

    :returns: A vector graphics method object
    :rtype: vcs.vector.Gv
    """

    # Check to make sure the argument passed in is a STRING
    if not isinstance(Gv_name_src, basestring):
        raise vcsError('The argument must be a string.')
    if Gv_name_src not in vcs.elements["vector"]:
        raise ValueError("The vector '%s' does not exist" % Gv_name_src)
    return vcs.elements["vector"][Gv_name_src]
getvector.__doc__ = getvector.__doc__ % xmldocs.get_docs['vector']  # noqa


def createstreamline(name=None, source='default'):
    """
    %s

    :param name: The name of the created object
    :type name: str

    :param source: The object to inherit from
    :type source: a streamline or a string name of a streamline

    :returns: A streamline graphics method object
    :rtype: vcs.streamline.Gs
    """
    name, source = check_name_source(name, source, 'streamline')
    return streamline.Gs(name, source)
createstreamline.__doc__ = createstreamline.__doc__ % xmldocs.create_docs['streamline']  # noqa


def getstreamline(Gs_name_src='default'):
    """
    %s

    :param Gs_name_src: String name of an existing streamline VCS object
    :type Gs_name_src: str

    :returns: A streamline graphics method object
    :rtype: vcs.streamline.Gs
    """

    # Check to make sure the argument passed in is a STRING
    if not isinstance(Gs_name_src, basestring):
        raise vcsError('The argument must be a string.')
    if Gs_name_src not in vcs.elements["streamline"]:
        raise ValueError("The streamline '%s' does not exist" % Gs_name_src)
    return vcs.elements["streamline"][Gs_name_src]
getstreamline.__doc__ = getstreamline.__doc__ % xmldocs.get_docs['streamline']  # noqa


def createscatter(name=None, source='default'):
    """%s

    :param name: The name of the created object
    :type name: `str`_

    :param source: The object to inherit from.
        Can be a scatter or, a string name of a scatter.
    :type source: `str`_ or :class:`vcs.unified1D.G1d`

    :return: A scatter graphics method
    :rtype: vcs.unified1D.G1d
    """
    try:
        gm = vcs.create1d(name, source)
    except vcsError as ve:
        if ve.message == "Error 1d object named %s already exists" % name:
            warning_message = "A 1D graphics method named %s already exists, creating yours as %s" % (name,
                                                                                                      name + "_scatter")
            warnings.warn(warning_message)
            gm = vcs.create1d(name + "_scatter", source)
        else:
            raise ve
    gm.linewidth = 0
    return gm
createscatter.__doc__ = createscatter.__doc__ % xmldocs.create_docs['scatter']  # noqa


def getscatter(GSp_name_src='default'):
    """%s

    :param GSp_name_src: String name of an existing scatter VCS object.
    :type GSp_name_src: `str`_

    :returns: A scatter graphics method object
    :rtype: vcs.unified1D.G1d
    """
    gm = vcs.get1d(GSp_name_src)
    if gm.g_type != "scatter":
        return vcs.get1d(GSp_name_src + "_scatter")
    return gm
getscatter.__doc__ = getscatter.__doc__ % xmldocs.get_docs['scatter']  # noqa


def createline(name=None, source='default', ltype=None,
               width=None, color=None, priority=None,
               viewport=None, worldcoordinate=None,
               x=None, y=None, projection=None):
    """%s

    :param name: Name of created object
    :type name: `str`_

    :param source: a line, or string name of a line
    :type source: `str`_

    :param ltype: One of "dash", "dash-dot", "solid", "dot", or "long-dash".
    :type ltype: `str`_

    :param width: Thickness of the line to be created
    :type width: `int`_

    :param color: A color name from the `X11 Color Names list <https://en.wikipedia.org/wiki/X11_color_names>`_,
                  or an integer value from 0-255, or an RGB/RGBA tuple/list (e.g. (0,100,0), (100,100,0,50))
    :type color: `str`_ or `int`_

    :param priority: The layer on which the line will be drawn.
    :type priority: `int`_

    :param viewport: 4 floats between 0 and 1 which specify the area that X/Y values are mapped to inside of the canvas.
    :type viewport: `list`_

    :param worldcoordinate: List of 4 floats (xmin, xmax, ymin, ymax)
    :type worldcoordinate: `list`_

    :param x: List of lists of x coordinates. Values must be between worldcoordinate[0] and worldcoordinate[1].
    :type x: `list`_

    :param y: List of lists of y coordinates. Values must be between worldcoordinate[2] and worldcoordinate[3].
    :type y: `list`_

    :param projection: Specify a geographic projection used to convert x/y from spherical coordinates to 2D coordinates.
    :type projection: `str`_ or projection object

    :returns: A VCS line secondary method object
    :rtype: vcs.line.Tl
    """
    name, source = check_name_source(name, source, 'line')

    ln = line.Tl(name, source)
    if (ltype is not None):
        ln.type = ltype
    if (width is not None):
        ln.width = width
    if (color is not None):
        ln.color = color
    if (priority is not None):
        ln.priority = priority
    if (viewport is not None):
        ln.viewport = viewport
    if (worldcoordinate is not None):
        ln.worldcoordinate = worldcoordinate
    if (x is not None):
        ln.x = x
    if (y is not None):
        ln.y = y
    if (projection is not None):
        ln.projection = projection
    return ln
createline.__doc__ = createline.__doc__ % xmldocs.create_docs['line']  # noqa


def setLineAttributes(to, l):
    """Set attributes linecolor, linewidth and linetype from line l on object to.

    :Example:

        .. doctest:: manageElements_setLineAttributes

            >>> vcs.show('line')
            *******************Line Names List**********************
            ...
            *******************End Line Names List**********************
            >>> new_isoline = vcs.createisoline('new_iso')
            >>> vcs.setLineAttributes(new_isoline, 'continents')
            >>> new_vector = vcs.createvector('new_vec')
            >>> vcs.setLineAttributes(new_vector, 'continents')
            >>> new_1d = vcs.create1d('new_1d', 'blue_yxvsx')
            >>> vcs.setLineAttributes(new_1d, 'continents')

    :param to: A vector, 1d, or isoline object to set the properties of.
    :type to: :class:`vcs.vector.Gv`, :class:`vcs.unified1d.G1d`

    :param l: l can be a line name defined in vcs.elements or a line object.
        l will be used to set the properties of to.
    :type l: :py:class:`vcs.line.Tl` or str
    """
    from . import queries
    line = None
    if (queries.isline(l)):
        line = l
    elif l in vcs.elements["line"]:
        line = vcs.elements["line"][l]
    else:
        raise ValueError("Expecting a line object or a " +
                         "line name defined in vcs.elements, got type " +
                         type(l).__name__)
    if queries.isisoline(to):
        to.linecolors = line.color
        to.linewidths = line.width
        to.linetypes = line.type
    else:
        to.linecolor = line.color[0]
        to.linewidth = line.width[0]
        to.linetype = line.type[0]


def getline(name='default', ltype=None, width=None, color=None,
            priority=None, viewport=None,
            worldcoordinate=None,
            x=None, y=None):
    """%s

    :param name: Name of created object
    :type name: `str`_

    :param ltype: One of "dash", "dash-dot", "solid", "dot", or "long-dash".
    :type ltype: `str`_

    :param width: Thickness of the line to be created
    :type width: `int`_

    :param color: A color name from the `X11 Color Names list <https://en.wikipedia.org/wiki/X11_color_names>`_,
        or an integer value from 0-255, or an RGB/RGBA tuple/list (e.g. (0,100,0), (100,100,0,50))
    :type color: `str`_ or int

    :param priority: The layer on which the marker will be drawn.
    :type priority: `int`_

    :param viewport: 4 floats between 0 and 1 which specify the area that X/Y values are mapped to inside of the canvas.
    :type viewport: `list`_

    :param worldcoordinate: List of 4 floats (xmin, xmax, ymin, ymax)
    :type worldcoordinate: `list`_

    :param x: List of lists of x coordinates. Values must be between worldcoordinate[0] and worldcoordinate[1].
    :type x: `list`_

    :param y: List of lists of y coordinates. Values must be between worldcoordinate[2] and worldcoordinate[3].
    :type y: `list`_

    :returns: A VCS line object
    :rtype: vcs.line.Tl
    """

    # Check to make sure the argument passed in is a STRING
    if not isinstance(name, basestring):
        raise vcsError('The argument must be a string.')

    if name not in vcs.elements["line"]:
        raise ValueError("The line '%s' does not exist" % name)
    ln = vcs.elements["line"][name]
    if ltype is not None and ln.name != 'default':
        ln.type = ltype
    if width is not None and ln.name != 'default':
        ln.width = width
    if color is not None and ln.name != 'default':
        ln.color = color
    if priority is not None and ln.name != 'default':
        ln.priority = priority
    if viewport is not None and ln.name != 'default':
        ln.viewport = viewport
    if worldcoordinate is not None and ln.name != 'default':
        ln.worldcooridnate = worldcoordinate
    if viewport is not None and ln.name != 'default':
        ln.viewport = viewport
    if x is not None and ln.name != 'default':
        ln.x = x
    if y is not None and ln.name != 'default':
        ln.y = y
    return ln
getline.__doc__ = getline.__doc__ % xmldocs.get_docs['line']  # noqa


def createmarker(name=None, source='default', mtype=None,
                 size=None, color=None, priority=None,
                 viewport=None, worldcoordinate=None,
                 x=None, y=None, projection=None):
    """%s

    :param name: Name of created object
    :type name: `str`_

    :param source: A marker, or string name of a marker
    :type source: `str`_

    :param mtype: Specifies the type of marker, i.e. "dot", "circle"
    :type mtype: `str`_

    :param size:
    :type size: `int`_

    :param color: A color name from the `X11 Color Names list <https://en.wikipedia.org/wiki/X11_color_names>`_,
        or an integer value from 0-255, or an RGB/RGBA tuple/list (e.g. (0,100,0), (100,100,0,50))
    :type color: `str`_ or int

    :param priority: The layer on which the marker will be drawn.
    :type priority: `int`_

    :param viewport: 4 floats between 0 and 1 which specify the area that X/Y values are mapped to inside of the canvas.
    :type viewport: `list`_

    :param worldcoordinate: List of 4 floats (xmin, xmax, ymin, ymax)
    :type worldcoordinate: `list`_

    :param x: List of lists of x coordinates. Values must be between worldcoordinate[0] and worldcoordinate[1].
    :type x: `list`_

    :param y: List of lists of y coordinates. Values must be between worldcoordinate[2] and worldcoordinate[3].
    :type y: `list`_

    :returns: A secondary marker method
    :rtype: vcs.marker.Tm
    """
    name, source = check_name_source(name, source, 'marker')

    mrk = marker.Tm(name, source)
    if (mtype is not None):
        mrk.type = mtype
    if (size is not None):
        mrk.size = size
    if (color is not None):
        mrk.color = color
    if (priority is not None):
        mrk.priority = priority
    if (viewport is not None):
        mrk.viewport = viewport
    if (worldcoordinate is not None):
        mrk.worldcoordinate = worldcoordinate
    if (x is not None):
        mrk.x = x
    if (y is not None):
        mrk.y = y
    if (projection is not None):
        mrk.projection = projection
    return mrk
createmarker.__doc__ = createmarker.__doc__ % xmldocs.create_docs['marker']  # noqa


def getmarker(name='default', mtype=None, size=None, color=None,
              priority=None, viewport=None,
              worldcoordinate=None,
              x=None, y=None):
    """%s

    :param name: Name of created object
    :type name: `str`_

    :param source: A marker, or string name of a marker
    :type source: `str`_

    :param mtype: Specifies the type of marker, i.e. "dot", "circle"
    :type mtype: `str`_

    :param size: Size of the marker
    :type size: `int`_

    :param color: A color name from the `X11 Color Names list <https://en.wikipedia.org/wiki/X11_color_names>`_,
        or an integer value from 0-255, or an RGB/RGBA tuple/list (e.g. (0,100,0), (100,100,0,50))
    :type color: `str`_ or int

    :param priority: The layer on which the marker will be drawn.
    :type priority: `int`_

    :param viewport: 4 floats between 0 and 1 which specify the area that X/Y values are mapped to inside of the canvas.
    :type viewport: `list`_

    :param worldcoordinate: List of 4 floats (xmin, xmax, ymin, ymax)
    :type worldcoordinate: `list`_

    :param x: List of lists of x coordinates. Values must be between worldcoordinate[0] and worldcoordinate[1].
    :type x: `list`_

    :param y: List of lists of y coordinates. Values must be between worldcoordinate[2] and worldcoordinate[3].
    :type y: `list`_

    :returns: A marker graphics method object
    :rtype: vcs.marker.Tm
    """

    # Check to make sure the argument passed in is a STRING
    if not isinstance(name, basestring):
        raise vcsError('The argument must be a string.')

    if name not in vcs.elements["marker"]:
        raise ValueError("The marker object '%s' does not exists")
    mrk = vcs.elements["marker"][name]
    if (mtype is not None) and (mrk.name != "default"):
        mrk.type = mtype
    if (size is not None) and (mrk.name != "default"):
        mrk.size = size
    if (color is not None) and (mrk.name != "default"):
        mrk.color = color
    if (priority is not None) and (mrk.name != "default"):
        mrk.priority = priority
    if (viewport is not None) and (mrk.name != "default"):
        mrk.viewport = viewport
    if (worldcoordinate is not None) and (mrk.name != "default"):
        mrk.worldcoordinate = worldcoordinate
    if (x is not None) and (mrk.name != "default"):
        mrk.x = x
    if (y is not None) and (mrk.name != "default"):
        mrk.y = y
    return mrk
getmarker.__doc__ = getmarker.__doc__ % xmldocs.get_docs['marker']  # noqa


def createfillarea(name=None, source='default', style=None,
                   index=None, color=None, priority=None,
                   viewport=None, worldcoordinate=None,
                   x=None, y=None):
    """%s

    :param name: Name of created object
    :type name: `str`_

    :param source: a fillarea, or string name of a fillarea
    :type source: `str`_

    :param style: One of "hatch", "solid", or "pattern".
    :type style: `str`_

    :param index: Specifies which `pattern <http://uvcdat.llnl.gov/gallery/fullsize/pattern_chart.png>`_ to fill with.
        Accepts ints from 1-20.
    :type index: `int`_

    :param color: A color name from the `X11 Color Names list <https://en.wikipedia.org/wiki/X11_color_names>`_,
        or an integer value from 0-255, or an RGB/RGBA tuple/list (e.g. (0,100,0), (100,100,0,50))

    :type color: `str`_ or int

    :param priority: The layer on which the fillarea will be drawn.
    :type priority: `int`_

    :param viewport: 4 floats between 0 and 1 which specify the area that X/Y values are mapped to inside of the canvas.
    :type viewport: `list`_

    :param worldcoordinate: List of 4 floats (xmin, xmax, ymin, ymax)
    :type worldcoordinate: `list`_

    :param x: List of lists of x coordinates. Values must be between worldcoordinate[0] and worldcoordinate[1].
    :type x: `list`_

    :param y: List of lists of y coordinates. Values must be between worldcoordinate[2] and worldcoordinate[3].
    :type y: `list`_

    :returns: A fillarea object
    :rtype: vcs.fillarea.Tf
    """

    name, source = check_name_source(name, source, 'fillarea')

    fa = fillarea.Tf(name, source)
    if (style is not None):
        fa.style = style
    if (index is not None):
        fa.index = index
    if (color is not None):
        fa.color = color
    if (priority is not None):
        fa.priority = priority
    if (viewport is not None):
        fa.viewport = viewport
    if (worldcoordinate is not None):
        fa.worldcoordinate = worldcoordinate
    if (x is not None):
        fa.x = x
    if (y is not None):
        fa.y = y
    return fa
createfillarea.__doc__ = createfillarea.__doc__ % xmldocs.create_docs['fillarea']  # noqa


def getfillarea(name='default', style=None,
                index=None, color=None,
                priority=None, viewport=None,
                worldcoordinate=None,
                x=None, y=None):
    """%s

    :param name: String name of an existing fillarea VCS object
    :type name: `str`_

    :param style: One of "hatch", "solid", or "pattern".
    :type style: `str`_

    :param index: Specifies which `pattern <http://uvcdat.llnl.gov/gallery/fullsize/pattern_chart.png>`_ to fill with.
                  Accepts ints from 1-20.
    :type index: `int`_

    :param color: A color name from the `X11 Color Names list <https://en.wikipedia.org/wiki/X11_color_names>`_,
                  or an integer value from 0-255, or an RGB/RGBA tuple/list (e.g. (0,100,0), (100,100,0,50))
    :type color: `str`_ or int

    :param priority: The layer on which the texttable will be drawn.
    :type priority: `int`_

    :param viewport: 4 floats between 0 and 1 which specify the area that X/Y
        values are mapped to inside of the canvas.
    :type viewport: `list`_

    :param worldcoordinate: List of 4 floats (xmin, xmax, ymin, ymax)
    :type worldcoordinate: `list`_

    :param x: List of lists of x coordinates. Values must be between worldcoordinate[0] and worldcoordinate[1].
    :type x: `list`_

    :param y: List of lists of y coordinates. Values must be between worldcoordinate[2] and worldcoordinate[3].
    :type y: `list`_

    :returns: A fillarea secondary object
    :rtype: vcs.fillarea.Tf
    """

    # Check to make sure the argument passed in is a STRING
    if not isinstance(name, basestring):
        raise vcsError('The argument must be a string.')
    if name not in list(vcs.elements["fillarea"].keys()):
        raise vcsError("Fillarea '%s' does not exist" % (name))

    fa = vcs.elements["fillarea"][name]
    if (style is not None) and (fa.name != "default"):
        fa.style = style
    if (index is not None) and (fa.name != "default"):
        fa.index = index
    if (color is not None) and (fa.name != "default"):
        fa.color = color
    if (priority is not None) and (fa.name != "default"):
        fa.priority = priority
    if (viewport is not None) and (fa.name != "default"):
        fa.viewport = viewport
    if (worldcoordinate is not None) and (fa.name != "default"):
        fa.worldcoordinate = worldcoordinate
    if (x is not None) and (fa.name != "default"):
        fa.x = x
    if (y is not None) and (fa.name != "default"):
        fa.y = y
    return fa
getfillarea.__doc__ = getfillarea.__doc__ % xmldocs.get_docs['fillarea']  # noqa


def createtexttable(name=None, source='default', font=None,
                    spacing=None, expansion=None, color=None, priority=None,
                    viewport=None, worldcoordinate=None,
                    x=None, y=None):
    """%s

    :param name: Name of created object
    :type name: `str`_

    :param source: a texttable, or string name of a texttable
    :type source: `str`_

    :param font: Which font to use (index or name).
    :type font: `int`_ or `str`_

    :param color: A color name from the `X11 Color Names list <https://en.wikipedia.org/wiki/X11_color_names>`_,
                  or an integer value from 0-255, or an RGB/RGBA tuple/list (e.g. (0,100,0), (100,100,0,50))
    :type color: `str`_ or int

    :param priority: The layer on which the texttable will be drawn.
    :type priority: `int`_

    :param viewport: 4 floats between 0 and 1 which specify the area that X/Y values are mapped to inside of the canvas.
    :type viewport: `list`_

    :param worldcoordinate: List of 4 floats (xmin, xmax, ymin, ymax)
    :type worldcoordinate: `list`_

    :param x: List of lists of x coordinates.
        Values must be between worldcoordinate[0] and worldcoordinate[1].
    :type x: `list`_

    :param y: List of lists of y coordinates.
        Values must be between worldcoordinate[2] and worldcoordinate[3].
    :type y: `list`_

    :returns: A texttable graphics method object
    :rtype: vcs.texttable.Tt

    .. note::

        The expansion parameter is no longer used
    """

    name, source = check_name_source(name, source, 'texttable')

    tt = texttable.Tt(name, source)
    try:
        if (font is not None):
            tt.font = font
        if (spacing is not None):
            tt.spacing = spacing
        if (expansion is not None):
            tt.expansion = expansion
        if (color is not None):
            tt.color = color
        if (priority is not None):
            tt.priority = priority
        if (viewport is not None):
            tt.viewport = viewport
        if (worldcoordinate is not None):
            tt.worldcoordinate = worldcoordinate
        if (x is not None):
            tt.x = x
        if (y is not None):
            tt.y = y
        return tt
    except Exception:
        pass
createtexttable.__doc__ = createtexttable.__doc__ % xmldocs.create_docs['texttable']  # noqa


def gettexttable(name='default', font=None,
                 spacing=None, expansion=None, color=None,
                 priority=None, viewport=None,
                 worldcoordinate=None,
                 x=None, y=None):
    """%s

    :param name: String name of an existing VCS texttable object
    :type name: `str`_

    :param font: Which font to use (index or name).
    :type font: `int`_ or `str`_

    :param color: A color name from the `X11 Color Names list <https://en.wikipedia.org/wiki/X11_color_names>`_,
                  or an integer value from 0-255, or an RGB/RGBA tuple/list (e.g. (0,100,0), (100,100,0,50))
    :type color: `str`_ or int

    :param priority: The layer on which the texttable will be drawn.
    :type priority: `int`_

    :param viewport: 4 floats between 0 and 1 which specify the area that X/Y values are mapped to inside of the canvas.
    :type viewport: `list`_

    :param worldcoordinate: List of 4 floats (xmin, xmax, ymin, ymax)
    :type worldcoordinate: `list`_

    :param x: List of lists of x coordinates. Values must be between worldcoordinate[0] and worldcoordinate[1].
    :type x: `list`_

    :param y: List of lists of y coordinates. Values must be between worldcoordinate[2] and worldcoordinate[3].
    :type y: `list`_

    :returns: A texttable graphics method object
    :rtype: vcs.texttable.Tt

    .. note::

        The expansion parameter is no longer used
    """

    # Check to make sure the argument passed in is a STRING
    if not isinstance(name, basestring):
        raise vcsError('The argument must be a string.')

    if name not in vcs.elements["texttable"]:
        raise ValueError("The texttable '%s' does not exists" % name)
    return vcs.elements["texttable"][name]
gettexttable.__doc__ = gettexttable.__doc__ % xmldocs.get_docs['texttable']  # noqa


def createtextorientation(name=None, source='default'):
    """%s

    :param name: The name of the created object
    :type name: `str`_

    :param source: The object to inherit from.
        Can be a textorientation, or a string name of a textorientation.
    :type source: `str`_ or :class:`vcs.textorientation.To`

    :returns: A textorientation secondary method
    :rtype: vcs.textorientation.To
    """

    name, source = check_name_source(name, source, 'textorientation')

    return textorientation.To(name, source)
createtextorientation.__doc__ = createtextorientation.__doc__ % xmldocs.create_docs['textorientation']  # noqa


def gettextorientation(To_name_src='default'):
    """%s

    :param To_name_src: String name of an existing textorientation VCS object
    :type To_name_src: `str`_

    :returns: A textorientation VCS object
    :rtype: vcs.textorientation.To
    """

    # Check to make sure the argument passed in is a STRING
    if not isinstance(To_name_src, basestring):
        raise vcsError('The argument must be a string.')

    if To_name_src not in vcs.elements["textorientation"]:
        raise ValueError(
            "The textorientation '%s' does not exists" %
            To_name_src)
    return vcs.elements["textorientation"][To_name_src]
gettextorientation.__doc__ = gettextorientation.__doc__ % xmldocs.get_docs['textorientation']  # noqa


def createtextcombined(Tt_name=None, Tt_source='default', To_name=None, To_source='default',
                       font=None, spacing=None, expansion=None, color=None,
                       priority=None, viewport=None, worldcoordinate=None, x=None, y=None,
                       height=None, angle=None, path=None, halign=None, valign=None, projection=None):
    """%s

    :param Tt_name: Name of created object
    :type Tt_name: `str`_

    :param Tt_source: Texttable object to inherit from. Can be a texttable, or a string name of a texttable.
    :type Tt_source: `str`_ or :class:`vcs.texttable.Tt`

    :param To_name: Name of the textcombined's text orientation  (to be created)
    :type To_name: `str`_

    :param To_source: Name of the textorientation to inherit.
            Can be a textorientation, or a string name of a textorientation.
    :type To_source: `str`_ or :class:`vcs.textorientation.To`

    :param font: Which font to use (index or name).
    :type font: `int`_ or `str`_

    :param color: A color name from the `X11 Color Names list <https://en.wikipedia.org/wiki/X11_color_names>`_,
                  or an integer value from 0-255, or an RGB/RGBA tuple/list (e.g. (0,100,0), (100,100,0,50))
    :type color: `str`_ or int

    :param priority: The layer on which the object will be drawn.
    :type priority: `int`_

    :param viewport: 4 floats between 0 and 1 which specify the area that X/Y values are mapped to inside of the canvas.
    :type viewport: `list`_

    :param worldcoordinate: List of 4 floats (xmin, xmax, ymin, ymax)
    :type worldcoordinate: `list`_

    :param x: List of lists of x coordinates. Values must be between worldcoordinate[0] and worldcoordinate[1].
    :type x: `list`_

    :param y: List of lists of y coordinates. Values must be between worldcoordinate[2] and worldcoordinate[3].
    :type y: `list`_

    :param height: Size of the font
    :type height: `int`_

    :param angle: Angle of the text, in degrees
    :type angle: `int`_

    :param halign: Horizontal alignment of the text. One of ["left", "center", "right"].
    :type halign: `str`_

    :param valign: Vertical alignment of the text. One of ["top", "center", "botom"].
    :type valign: `str`_

    :param projection: Specify a geographic projection used to convert x/y from spherical coordinates to 2D coordinates.
    :type projection: `str`_ or projection object

    :returns: A VCS text object
    :rtype: vcs.textcombined.Tc

    .. note::

        The spacing, path, and expansion parameters are no longer used
    """
    # Check if to is defined
    if To_name is None:
        To_name = Tt_name
    Tt_name, Tt_source = check_name_source(Tt_name, Tt_source, 'texttable')
    To_name, To_source = check_name_source(
        To_name, To_source, 'textorientation')

    tc = textcombined.Tc(Tt_name, Tt_source, To_name, To_source)
    if (font is not None):
        tc.font = font
    if (spacing is not None):
        tc.spacing = spacing
    if (expansion is not None):
        tc.expansion = expansion
    if (color is not None):
        tc.color = color
    if (priority is not None):
        tc.priority = priority
    if (viewport is not None):
        tc.viewport = viewport
    if (worldcoordinate is not None):
        tc.worldcoordinate = worldcoordinate
    if (x is not None):
        tc.x = x
    if (y is not None):
        tc.y = y
    if (height is not None):
        tc.height = height
    if (angle is not None):
        tc.angle = angle
    if (path is not None):
        tc.path = path
    if (halign is not None):
        tc.halign = halign
    if (valign is not None):
        tc.valign = valign
    if (projection is not None):
        tc.projection = projection
    return tc
#
# Set alias for the secondary createtextcombined.
createtext = createtextcombined  # noqa
createtextcombined.__doc__ = createtextcombined.__doc__ % xmldocs.create_docs['textcombined']  # noqa


def gettextcombined(Tt_name_src='default', To_name_src=None, string=None, font=None, spacing=None,
                    expansion=None, color=None,
                    priority=None, viewport=None, worldcoordinate=None, x=None, y=None,
                    height=None, angle=None, path=None, halign=None, valign=None):
    """%s

    :param Tt_name_src: Name of parent texttable object
    :type Tt_name_src: `str`_

    :param To_name_src: Name of parent textorientation object
    :type To_name_src: `str`_

    :param string: Text to render
    :type string: `list`_

    :param font: Which font to use (index or name)
    :type font: `int`_ or `str`_

    :param color: A color name from the `X11 Color Names list <https://en.wikipedia.org/wiki/X11_color_names>`_,
        or an integer value from 0-255, or an RGB/RGBA tuple/list (e.g. (0,100,0), (100,100,0,50))
    :type color: `str`_ or int

    :param priority: The layer on which the object will be drawn.
    :type priority: `int`_

    :param viewport: 4 floats between 0 and 1 which specify the area that X/Y values are mapped to inside of the canvas.
    :type viewport: `list`_

    :param worldcoordinate: List of 4 floats (xmin, xmax, ymin, ymax)
    :type worldcoordinate: `list`_

    :param x: List of lists of x coordinates.
        Values must be between worldcoordinate[0] and worldcoordinate[1].
    :type x: `list`_

    :param y: List of lists of y coordinates. Values must be between worldcoordinate[2] and worldcoordinate[3].
    :type y: `list`_

    :param height: Size of the font
    :type height: `int`_

    :param angle: Angle of the rendered text, in degrees.
        Must be a list of integers.
    :type angle: `list`_

    :param halign: Horizontal alignment of the text. One of ["left", "center", "right"]
    :type halign: `str`_

    :param valign: Vertical alignment of the text. One of ["top", "center", "bottom"]
    :type valign: `str`_

    :returns: A textcombined object
    :rtype: vcs.textcombined.Tc

    .. note::

        The spacing, path, and expansion parameters are no longer used
    """

    # Check to make sure the arguments passed in are a STRINGS
    if not isinstance(Tt_name_src, basestring):
        raise vcsError('The first argument must be a string.')
    if To_name_src is None:
        sp = Tt_name_src.split(":::")
        if len(sp) == 2:
            Tt_name_src = sp[0]
            To_name_src = sp[1]
    if not isinstance(To_name_src, basestring):
        raise vcsError('The second argument must be a string.')

    tc = vcs.elements["textcombined"].get(
        "%s:::%s" %
        (Tt_name_src, To_name_src), None)
    if tc is None:
        raise Exception(
            "No such text combined: %s:::%s" %
            (Tt_name_src, To_name_src))

    if (string is not None) and (tc.Tt_name != "default"):
        tc.string = string
    if (font is not None) and (tc.Tt_name != "default"):
        tc.font = font
    if (spacing is not None) and (tc.Tt_name != "default"):
        tc.spacing = spacing
    if (expansion is not None) and (tc.Tt_name != "default"):
        tc.expansion = expansion
    if (color is not None) and (tc.Tt_name != "default"):
        tc.color = color
    if (priority is not None) and (tc.Tt_name != "default"):
        tc.priority = priority
    if (viewport is not None) and (tc.Tt_name != "default"):
        tc.viewport = viewport
    if (worldcoordinate is not None) and (tc.Tt_name != "default"):
        tc.worldcoordinate = worldcoordinate
    if (x is not None) and (tc.To_name != "default"):
        tc.x = x
    if (y is not None) and (tc.To_name != "default"):
        tc.y = y
    if (height is not None) and (tc.To_name != "default"):
        tc.height = height
    if (angle is not None) and (tc.To_name != "default"):
        tc.angle = angle
    if (path is not None) and (tc.To_name != "default"):
        tc.path = path
    if (halign is not None) and (tc.To_name != "default"):
        tc.halign = halign
    if (valign is not None) and (tc.To_name != "default"):
        tc.valign = valign
    return tc
gettextcombined.__doc__ = gettextcombined.__doc__ % xmldocs.get_docs['textcombined']  # noqa
#
# Set alias for the secondary gettextcombined.
gettext = gettextcombined  # noqa


def get3d_scalar(Gfdv3d_name_src='default'):
    """%s

    :param Gfdv3d_name_src: String name of an existing 3d_scalar VCS object.
    :type Gfdv3d_name_src: str

    :returns: A pre-existing 3d_scalar VCS object
    :rtype: vcs.dv3d.Gf3Dscalar
    """

    # Check to make sure the argument passed in is a STRING
    if not isinstance(Gfdv3d_name_src, basestring):
        raise vcsError('The argument must be a string.')

    if Gfdv3d_name_src not in vcs.elements["3d_scalar"]:
        raise ValueError("dv3d '%s' does not exists" % Gfdv3d_name_src)

    return vcs.elements["3d_scalar"][Gfdv3d_name_src]
get3d_scalar.__doc__ = get3d_scalar.__doc__ % xmldocs.get_docs['3d_scalar']  # noqa


def create3d_scalar(name=None, source='default'):
    """%s

    :param name: The name of the created object
    :type name: `str`_

    :param source: The object to inherit from.
        Can be a 3d_scalar, or a string name of a 3d_scalar.
    :type source: `str`_ or :class:`vcs.dv3d.Gf3Dscalar`

    :returns: A 3d_scalar graphics method object
    :rtype: vcs.dv3d.Gf3Dscalar
    """
    name, source = check_name_source(name, source, '3d_scalar')
    return dv3d.Gf3Dscalar(name, source)
create3d_scalar.__doc__ = create3d_scalar.__doc__ % xmldocs.create_docs['3d_scalar']  # noqa


def get3d_dual_scalar(Gfdv3d_name_src='default'):
    """%s

    :param Gfdv3d_name_src: String name of an existing 3d_dual_scalar VCS object
    :type Gfdv3d_name_src: `str`_

    :returns: A pre-existing 3d_dual_scalar VCS object
    :rtype: vcs.dv3d.Gf3DDualScalar
    """
    # Check to make sure the argument passed in is a STRING
    if not isinstance(Gfdv3d_name_src, basestring):
        raise vcsError('The argument must be a string.')

    if Gfdv3d_name_src not in vcs.elements["3d_dual_scalar"]:
        raise ValueError("dv3d '%s' does not exists" % Gfdv3d_name_src)

    return vcs.elements["3d_dual_scalar"][Gfdv3d_name_src]
get3d_dual_scalar.__doc__ = get3d_dual_scalar.__doc__ % xmldocs.get_docs['3d_dual_scalar']  # noqa


def create3d_dual_scalar(name=None, source='default'):
    """%s

    :param name: The name of the created object
    :type name: `str`_

    :param source: The object to inherit from.
        Can be a 3d_dual_scalar, or a string name of a 3d_dual_scalar.
    :type source: `str`_ or :class:`vcs.dv3d.Gf3DDualScalar`

    :returns: A 3d_dual_scalar graphics method object
    :rtype: vcs.dv3d.Gf3DDualScalar
    """

    name, source = check_name_source(name, source, '3d_dual_scalar')
    return dv3d.Gf3DDualScalar(name, source)
create3d_dual_scalar.__doc__ = create3d_dual_scalar.__doc__ % xmldocs.create_docs['3d_dual_scalar']  # noqa


def get3d_vector(Gfdv3d_name_src='default'):
    """%s

    :param Gfdv3d_name_src: String name of an existing 3d_vector VCS object
    :type Gfdv3d_name_src: `str`_

    :returns: A pre-existing 3d_vector VCS object
    :rtype: vcs.dv3d.Gf3Dvector
    """

    # Check to make sure the argument passed in is a STRING
    if not isinstance(Gfdv3d_name_src, basestring):
        raise vcsError('The argument must be a string.')

    if Gfdv3d_name_src not in vcs.elements["3d_vector"]:
        raise ValueError("dv3d '%s' does not exists" % Gfdv3d_name_src)

    return vcs.elements["3d_vector"][Gfdv3d_name_src]
get3d_vector.__doc__ = get3d_vector.__doc__ % xmldocs.get_docs['3d_vector']  # noqa


def create3d_vector(name=None, source='default'):
    """%s

    :param name: The name of the created object
    :type name: `str`_

    :param source: The object to inherit from.
        Can be a 3d_vector, or a string name of a 3d_vector.
    :type source: `str`_ or :class:`vcs.dv3d.Gf3Dvector`

    :returns: A 3d_vector graphics method object
    :rtype: vcs.dv3d.Gf3Dvector
    """

    name, source = check_name_source(name, source, '3d_vector')
    return dv3d.Gf3Dvector(name, source)
create3d_vector.__doc__ = create3d_vector.__doc__ % xmldocs.create_docs['3d_vector']  # noqa

#############################################################################
#                                                                           #
# Colormap functions for VCS.                                               #
#                                                                           #
#############################################################################


def createcolormap(Cp_name=None, Cp_name_src='default'):
    """%s

    :param Cp_name: The name of the created object
    :type Cp_name: `str`_

    :param Cp_name_src: The object to inherit from.
        Can be a colormap or a string name of a colormap.
    :type Cp_name_src: `str`_ or :class:`vcs.colormap.Cp`

    :returns: A VCS colormap object
    :rtype: vcs.colormap.Cp
    """

    Cp_name, Cp_name_src = check_name_source(Cp_name, Cp_name_src, 'colormap')
    return colormap.Cp(Cp_name, Cp_name_src)
createcolormap.__doc__ = createcolormap.__doc__ % xmldocs.create_docs['colormap']  # noqa


def getcolormap(Cp_name_src='default'):
    """%s

    :param Cp_name_src: String name of an existing colormap VCS object
    :type Cp_name_src: `str`_

    :returns: A pre-existing VCS colormap object
    :rtype: vcs.colormap.Cp
    """
    # Check to make sure the argument passed in is a STRING
    if not isinstance(Cp_name_src, basestring):
        raise ValueError('Error -  The argument must be a string.')

    return vcs.elements["colormap"][Cp_name_src]
getcolormap.__doc__ = getcolormap.__doc__ % xmldocs.get_docs['colormap']  # noqa

# Function that deal with removing existing vcs elements


def removeG(obj, gtype="boxfill"):
    if isinstance(obj, basestring):
        name = obj
        if obj not in list(vcs.elements[gtype].keys()):
            raise RuntimeError("Cannot remove inexisting %s %s" % (gtype, obj))
    else:
        name = obj.name
        loc = locals()
        exec("res = vcs.is%s(obj)" % gtype)
        res = loc["res"]
        if not res:  # noqa
            raise RuntimeError("You are trying to remove a VCS %s but %s is not one" % (gtype, repr(obj)))
    msg = "Removed %s object %s" % (gtype, name)
    del(vcs.elements[gtype][name])
    return msg


def removeGfb(obj):
    return removeG(obj, "boxfill")


def removeGfi(obj):
    return removeG(obj, "isofill")


def removeGi(obj):
    return removeG(obj, "isoline")


def removeGXy(obj):
    return removeG(obj, "xyvsx")


def removeGYx(obj):
    return removeG(obj, "yxvsx")


def removeGXY(obj):
    return removeG(obj, "xvsy")


def removeG1d(obj):
    return removeG(obj, "1d")


def removeGv(obj):
    return removeG(obj, "vector")


def removeGs(obj):
    return removeG(obj, "streamline")


def removeGSp(obj):
    return removeG(obj, "scatter")


def removeGfm(obj):
    return removeG(obj, "meshfill")


def removeGtd(obj):
    return removeG(obj, "taylordiagram")


def removeTl(obj):
    return removeG(obj, "line")


def removeTm(obj):
    return removeG(obj, "marker")


def removeTf(obj):
    return removeG(obj, "fillarea")


def removeTt(obj):
    return removeG(obj, "texttable")


def removeTo(obj):
    return removeG(obj, "textorientation")


def removeTc(obj):
    if isinstance(obj, basestring):
        Tt, To = obj.split(":::")
    else:
        To = obj.To_name
        Tt = obj.Tt_name
    msg = removeTt(Tt)
    msg += removeTo(To)
    removeG(obj, "textcombined")
    return msg


def removeProj(obj):
    return removeG(obj, "projection")


def removeCp(obj):
    return removeG(obj, "colormap")


def removeDp(obj):
    if isinstance(obj, basestring):
        obj = vcs.elements["display"][obj]
    if obj.name not in obj._parent.return_display_names():
        return removeG(obj, "display")


def removeP(obj):
    # first we need to see if the template was scaled
    # If so we need to remove the textorientation objects
    # associated with this
    if not vcs.istemplate(obj):
        if obj not in list(vcs.elements["template"].keys()):
            raise RuntimeError("Cannot remove inexisting template %s" % obj)
    if isinstance(obj, basestring):
        obj = vcs.gettemplate(obj)
    if obj._scaledFont:
        props = []
        for attr in dir(obj.__class__):
            if isinstance(getattr(obj.__class__, attr), property):
                props.append(attr)
        try:
            attr = list(vars(obj).keys())
        except Exception:
            attr = list(obj.__slots__)+props

        if len(attr) == 0:
            attr = list(obj.__slots__)+props

        for a in attr:
            if a[0] == "_":
                continue
            try:
                v = getattr(obj, a)
                to = getattr(v, 'textorientation')
                removeTo(to)
            except Exception:
                pass
    return removeG(obj, "template")


def remove3d_dual_scalar(obj):
    return removeG(obj, '3d_dual_scalar')


def removeobject(obj):
    """The user has the ability to create primary and secondary class
    objects. The function allows the user to remove these objects
    from the appropriate class list.

    .. note::

        The user is not allowed to remove a "default" class
        object.

    :Example:

        .. doctest:: manageElements_removeobject

            >>> a=vcs.init()
            >>> iso=a.createisoline('dean') # Create an instance of an isoline object
            >>> a.removeobject(iso) # Remove isoline object from VCS list
            'Removed isoline object dean'

    :param obj: Any VCS primary or secondary object
    :type obj: VCS object

    :returns: String indicating the specified object was removed
    :rtype: str
    """

    if vcs.istemplate(obj):
        msg = vcs.removeP(obj.name)
    elif vcs.isgraphicsmethod(obj):
        if (obj.g_name == 'Gfb'):
            msg = vcs.removeGfb(obj.name)
        elif (obj.g_name == 'Gfi'):
            msg = vcs.removeGfi(obj.name)
        elif (obj.g_name == 'Gi'):
            msg = vcs.removeGi(obj.name)
        elif (obj.g_name == 'GXy'):
            msg = vcs.removeGXy(obj.name)
        elif (obj.g_name == 'GYx'):
            msg = vcs.removeGYx(obj.name)
        elif (obj.g_name == 'GXY'):
            msg = vcs.removeGXY(obj.name)
        elif (obj.g_name == 'Gv'):
            msg = vcs.removeGv(obj.name)
        elif (obj.g_name == 'GSp'):
            msg = vcs.removeGSp(obj.name)
        elif (obj.g_name == 'Gfm'):
            msg = vcs.removeGfm(obj.name)
        elif (obj.g_name == 'G1d'):
            msg = vcs.removeG1d(obj.name)
        elif (obj.g_name == 'Gtd'):
            msg = vcs.removeGtd(obj.name)
        elif (obj.g_name == 'Gs'):
            msg = vcs.removeGs(obj.name)
        else:
            msg = vcs.removeG(obj.name, obj.g_name)
    elif vcs.issecondaryobject(obj):
        if (obj.s_name == 'Tl'):
            msg = vcs.removeTl(obj.name)
        elif (obj.s_name == 'Tm'):
            msg = vcs.removeTm(obj.name)
        elif (obj.s_name == 'Tf'):
            msg = vcs.removeTf(obj.name)
        elif (obj.s_name == 'Tt'):
            msg = vcs.removeTt(obj.name)
        elif (obj.s_name == 'To'):
            msg = vcs.removeTo(obj.name)
        elif (obj.s_name == 'Tc'):
            msg = vcs.removeTc(obj.name)
        elif (obj.s_name == 'Proj'):
            msg = vcs.removeProj(obj.name)
        elif (obj.s_name == 'Cp'):
            msg = vcs.removeCp(obj.name)
        elif (obj.s_name == 'Dp'):
            msg = vcs.removeDp(obj.name)
        else:
            msg = 'Could not find the correct secondary class object.'
            raise vcsError(msg)
    else:
        msg = 'This ({}) is not a template, graphics method, or secondary method object.'.format(obj)
        raise vcsError(msg)
    return msg
