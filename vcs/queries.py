#!/usr/bin/env python
#
# The VCS query controls -  query module
#
##########################################################################
#                                                                               #
# Module:       query module                                                    #
#                                                                               #
# Copyright:    "See file Legal.htm for copyright information."                 #
#                                                                               #
# Authors:      PCMDI Software Team                                             #
#               Lawrence Livermore NationalLaboratory:                          #
#               support@pcmdi.llnl.gov                                          #
#                                                                               #
# Description:  Functions which get information about vcs graphics objects      #
#               such as graphics methods and templates.                         #
#                                                                               #
# Version:      4.0                                                             #
#                                                                               #
##########################################################################

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
from . import boxfill
from . import isofill
from . import isoline
from . import taylor
from . import meshfill
from . import unified1D
from . import vector
from . import streamline
from . import line
from . import marker
from . import fillarea
from . import texttable
from . import textorientation
from . import textcombined
from . import template
from . import dv3d
from . import displayplot
from . import projection
import vcs
from . import xmldocs

from .error import vcsError

try:
    import vcsaddons
    hasVCSAddons = True
except Exception:
    hasVCSAddons = False


def isgraphicsmethod(gobj):
    """Indicates if the entered argument is one of the following graphics
    methods: boxfill, isofill, isoline,
    scatter, vector, xvsy, xyvsy, yxvsx.

    :Example:

        .. doctest:: queries_isgraphicsmethod

            >>> a=vcs.init()
            >>> box=a.getboxfill() # get default boxfill object
            >>> vcs.isgraphicsmethod(box)
            1

    :param gobj: A graphics object
    :type gobj: A VCS graphics object

    :returns: Integer reperesenting whether gobj is one of the above graphics methods.
                1 indicates true, 0 indicates false.
    :rtype: `int`_
    """
    if (isinstance(gobj, boxfill.Gfb)):
        return 1
    elif (isinstance(gobj, isofill.Gfi)):
        return 1
    elif (isinstance(gobj, dv3d.Gf3Dscalar)):
        return 1
    elif (isinstance(gobj, dv3d.Gf3DDualScalar)):
        return 1
    elif (isinstance(gobj, dv3d.Gf3Dvector)):
        return 1
    elif (isinstance(gobj, isoline.Gi)):
        return 1
    elif (isinstance(gobj, vector.Gv)):
        return 1
    elif (isinstance(gobj, streamline.Gs)):
        return 1
    elif (isinstance(gobj, unified1D.G1d)):
        return 1
    elif (isinstance(gobj, taylor.Gtd)):
        return 1
    elif (isinstance(gobj, meshfill.Gfm)):
        return 1
    elif hasVCSAddons and isinstance(gobj, vcsaddons.core.VCSaddon):
        return 1
    else:
        return 0


def graphicsmethodlist():
    """
    List available graphics methods.

    :Example:

        .. doctest:: queries_gmlist

            >>> a=vcs.init()
            >>> vcs.graphicsmethodlist() # Return graphics method list
            [...]

    :returns: A list of available grapics methods (i.e., 'boxfill', 'isofill', 'isoline', 'meshfill', 'scatter',
            'vector', 'xvsy', 'xyvsy', 'yxvsx', 'taylordiagram', '1d', '3d_scalar', '3d_dual_scalar', '3d_vector').
    :rtype: `list`_
    """
    return ['boxfill', 'isofill', 'isoline', 'meshfill', 'scatter',
            'vector', 'streamline', 'xvsy', 'xyvsy', 'yxvsx', 'taylordiagram',
            '1d', '3d_scalar', '3d_dual_scalar', '3d_vector']


def graphicsmethodtype(gobj):
    """Check the type of a graphics object.

    Returns None if the object is not a graphics method.

    :Example:

        .. doctest:: queries_gmtype

            >>> a=vcs.init()
            >>> box=a.getboxfill() # Get default boxfill graphics method
            >>> iso=a.getisofill() # Get default isofill graphics method
            >>> ln=a.getline() # Get default line element
            >>> vcs.graphicsmethodtype(box)
            'boxfill'
            >>> vcs.graphicsmethodtype(iso)
            'isofill'
            >>> vcs.graphicsmethodtype(ln)
            Traceback (most recent call last):
            ...
            vcsError: The object passed is not a graphics method object.

    :returns: If gobj is a graphics method object, returns its type: 'boxfill', 'isofill', 'isoline', 'meshfill',
        'scatter', 'vector', 'xvsy', 'xyvsy', 'yxvsx', 'taylordiagram', '1d', '3d_scalar', '3d_dual_scalar',
        '3d_vector'.
        If gobj is not a graphics method object, raises an exception and prints a vcsError message.
    :rtype: `str`_ or `None`_
    """
    if (isinstance(gobj, boxfill.Gfb)):
        return 'boxfill'
    elif (isinstance(gobj, isofill.Gfi)):
        return 'isofill'
    elif (isinstance(gobj, dv3d.Gf3Dscalar)):
        return '3d_scalar'
    elif (isinstance(gobj, dv3d.Gf3DDualScalar)):
        return '3d_dual_scalar'
    elif (isinstance(gobj, dv3d.Gf3Dvector)):
        return '3d_vector'
    elif (isinstance(gobj, isoline.Gi)):
        return 'isoline'
    elif (isinstance(gobj, vector.Gv)):
        return 'vector'
    elif (isinstance(gobj, streamline.Gs)):
        return 'streamline'
    elif (isinstance(gobj, unified1D.G1d)):
        return "1d"
    elif (isinstance(gobj, taylor.Gtd)):
        return 'taylordiagram'
    elif (isinstance(gobj, meshfill.Gfm)):
        return 'meshfill'
    elif hasVCSAddons and isinstance(gobj, vcsaddons.core.VCSaddon):
        return gobj
    else:
        raise vcsError('The object passed is not a graphics method object.')


def isplot(pobj):
    """Check to see if this object is a VCS secondary display plot.

    :Example:

        .. doctest:: queries_isplot

            >>> a=vcs.init()
            >>> array=[range(10) for _ in range(10)]
            >>> dsp=a.plot(array) # plotting should return a displayplot object
            >>> vcs.queries.isplot(dsp)
            1

    :param obj: A VCS object
    :type obj: VCS Object

    :returns: An integer indicating whether the object is a display plot (1), or not (0).
    :rtype: `int`_
    """
    if (isinstance(pobj, displayplot.Dp)):
        return 1
    else:
        return 0


def iscolormap(obj):
    if (isinstance(obj, vcs.colormap.Cp)):
        return 1
    else:
        return 0
iscolormap.__doc__ = xmldocs.is_docs['colormap']  # noqa


def istemplate(gobj):
    if (isinstance(gobj, template.P)):
        return 1
    else:
        return 0
istemplate.__doc__ = xmldocs.is_docs['template']  # noqa


def issecondaryobject(sobj):
    """Check to see if this object is a VCS secondary object

        .. note::

            Secondary objects will be one of the following:

                1.) colormap: specification of combinations of 256 available
                    colors

                2.) fill area: style, style index, and color index

                3.) format: specifications for converting numbers to display
                    strings

                4.) line: line type, width, and color index

                5.) list: a sequence of pairs of numerical and character values

                6.) marker: marker type, size, and color index

                7.) text table: text font type, character spacing, expansion,
                    and color index

                8.) text orientation: character height, angle, path, and
                    horizontal/vertical alignment

                9.) projections

                10.) displays

    :Example:

        .. doctest:: queries_issecondary

            >>> a=vcs.init()
            >>> a.show('projection') # Show all available projections
            *******************Projection Names List**********************
            ...
            *******************End Projection Names List**********************
            >>> ex = a.getprojection('default') # To test an existing line object
            >>> vcs.issecondaryobject(ex)
            1

    :param obj: A VCS object
    :type obj: VCS Object

    :returns: An integer indicating whether the object is a projection graphics object (1), or not (0).
    :rtype: `int`_
    """
    if (isinstance(sobj, line.Tl)):
        return 1
    elif (isinstance(sobj, marker.Tm)):
        return 1
    elif (isinstance(sobj, fillarea.Tf)):
        return 1
    elif (isinstance(sobj, texttable.Tt)):
        return 1
    elif (isinstance(sobj, textorientation.To)):
        return 1
    elif (isinstance(sobj, textcombined.Tc)):
        return 1
    elif (isinstance(sobj, marker.Tm)):
        return 1
    elif (isinstance(sobj, projection.Proj)):
        return 1
    elif (isinstance(sobj, vcs.colormap.Cp)):
        return 1
    elif (isinstance(sobj, vcs.displayplot.Dp)):
        return 1
    else:
        return 0


def isdisplay(obj):
    """
    Check to see if this object is a VCS display object

    :param obj: A VCS object
    :type obj: VCS Object

    :returns: An integer indicating whether the object is a
        display (1), or not (0).
    :rtype: int
    """
    if (isinstance(obj, vcs.displayplot.Dp)):
        return 1
    else:
        return 0


def isprojection(obj):
    if (isinstance(obj, projection.Proj)):
        return 1
    else:
        return 0
isprojection.__doc__ = xmldocs.is_docs['projection']  # noqa


def istaylordiagram(obj):
    if (isinstance(obj, taylor.Gtd)):
        return 1
    else:
        return 0
istaylordiagram.__doc__ = xmldocs.is_docs['taylordiagram']  # noqa


def ismeshfill(obj):
    if (isinstance(obj, meshfill.Gfm)):
        return 1
    else:
        return 0
ismeshfill.__doc__ = xmldocs.is_docs['meshfill']  # noqa


def isstreamline(obj):
    if (isinstance(obj, streamline.Gs)):
        return 1
    else:
        return 0
isstreamline.__doc__ = xmldocs.is_docs['streamline']  # noqa


def isboxfill(obj):
    if (isinstance(obj, boxfill.Gfb)):
        return 1
    else:
        return 0
isboxfill.__doc__ = xmldocs.is_docs['boxfill']  # noqa


def is3d_scalar(obj):
    if (isinstance(obj, dv3d.Gf3Dscalar) or isinstance(obj, dv3d.Gf3DDualScalar)):
        return 1
    else:
        return 0
is3d_scalar.__doc__ = xmldocs.is_docs['3d_scalar']  # noqa


def is3d_dual_scalar(obj):
    if isinstance(obj, dv3d.Gf3DDualScalar):
        return 1
    else:
        return 0
is3d_dual_scalar.__doc__ = xmldocs.is_docs['3d_dual_scalar']  # noqa


def is3d_vector(obj):
    if (isinstance(obj, dv3d.Gf3Dvector)):
        return 1
    else:
        return 0
is3d_vector.__doc__ = xmldocs.is_docs['3d_vector']  # noqa


def isisofill(obj):
    if (isinstance(obj, isofill.Gfi)):
        return 1
    else:
        return 0
isisofill.__doc__ = xmldocs.is_docs['isofill']  # noqa


def isisoline(obj):
    if (isinstance(obj, isoline.Gi)):
        return 1
    else:
        return 0
isisoline.__doc__ = xmldocs.is_docs['isoline']  # noqa


def isscatter(obj):
    if (isinstance(obj, unified1D.G1d)) and obj.g_type == "scatter":
        return 1
    else:
        return 0
isscatter.__doc__ = xmldocs.is_docs['scatter']  # noqa


def isxyvsy(obj):
    if (isinstance(obj, unified1D.G1d)) and obj.g_type == "xyvsy":
        return 1
    else:
        return 0
isxyvsy.__doc__ = xmldocs.is_docs['xyvsy']  # noqa


def isyxvsx(obj):
    if (isinstance(obj, unified1D.G1d)) and obj.g_type == "yxvsx":
        return 1
    else:
        return 0
isyxvsx.__doc__ = xmldocs.is_docs['yxvsx']  # noqa


def isxvsy(obj):
    if (isinstance(obj, unified1D.G1d)) and obj.g_type == "yxvsx":
        return 1
    else:
        return 0
isxvsy.__doc__ = xmldocs.is_docs['xvsy']  # noqa


def is1d(obj):
    if (isinstance(obj, unified1D.G1d)):
        return 1
    else:
        return 0
is1d.__doc__ = xmldocs.is_docs['1d']  # noqa


def isvector(obj):
    if (isinstance(obj, vector.Gv)):
        return 1
    else:
        return 0
isvector.__doc__ = xmldocs.is_docs['1d']  # noqa


def isline(obj):
    if (isinstance(obj, line.Tl)):
        return 1
    else:
        return 0
isline.__doc__ = xmldocs.is_docs['line']  # noqa


def ismarker(obj):
    if (isinstance(obj, marker.Tm)):
        return 1
    else:
        return 0
ismarker.__doc__ = xmldocs.is_docs['marker']  # noqa


def isfillarea(obj):
    if (isinstance(obj, fillarea.Tf)):
        return 1
    else:
        return 0
isfillarea.__doc__ = xmldocs.is_docs['fillarea']  # noqa


def istexttable(obj):
    if (isinstance(obj, texttable.Tt)):
        return 1
    else:
        return 0
istexttable.__doc__ = xmldocs.is_docs['texttable']  # noqa


def istextorientation(obj):
    if (isinstance(obj, textorientation.To)):
        return 1
    else:
        return 0
istextorientation.__doc__ = xmldocs.is_docs['textorientation']  # noqa


def istextcombined(obj):
    if (isinstance(obj, textcombined.Tc)):
        return 1
    else:
        return 0
istextcombined.__doc__ = xmldocs.is_docs['textcombined']  # noqa

# Set an alias for the secondary text combined method in VCS.               #
# This is much easier to type than 'textcombined'.                          #
istext = istextcombined
