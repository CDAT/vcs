#
# Errorbars (Te) module
###############################################################################
#                                                                             #
# Module:       errorbars (Te) module                                         #
#                                                                             #
# Copyright:    2000, Regents of the University of California                 #
#               This software may not be distributed to others without        #
#               permission of the author.                                     #
#                                                                             #
# Author:       PCMDI Software Team                                           #
#               Lawrence Livermore NationalLaboratory:                        #
#               support@pcmdi.llnl.gov                                        #
#                                                                             #
# Description:  Python command/1d wrapper for VCS's errorbars object          #
#                                                                             #
# Version:      1.0                                                           #
#                                                                             #
###############################################################################
#
#
#
import VCS_validation_functions
import vcs
import genutil
from xmldocs import scriptdocs, listdoc


def process_src(nm, code):

    # Takes VCS script code (string) as input and generates oneD gm from it
    try:
        gm = Te(nm)
    except:
        gm = vcs.elements["errorbars"][nm]
    # process attributes with = as assignment
    for att in ["type", "color"]:
        i = code.find(" %s(" % att)
        if i == -1:
            i = code.find(",%s(" % att)
        if i > -1:
            v = genutil.get_parenthesis_content(code[i:])
            setattr(gm, att, eval(v))


###############################################################################
#                                                                             #
# Errorbars (Te) Class.                                                       #
#                                                                             #
###############################################################################
class Te(vcs.bestMatch):

    """
    The Errorbars object allows the manipulation of errorbar type, size and
    color index.

    This class is used to define an error bars for 1D plots in VCS, or it can be
    used to change some or all of the error bar attributes in an existing plot.

    .. describe:: Useful functions:

        .. code-block:: python

            # VCS canvas Constructor
            x = vcs.init()
            # mock data
            data = "-1 -2 -1.34 -2 -1.1 -12.2".split()
            data = numpy.array(data, dtype=numpy.float)
            data = MV2.array(data)
            # mock errors
            error = "0.2 0.1 0.1 0.3 0.4 0.1".split()
            error = numpy.array(error, dtype=numpy.float)
            # Create default error bars
            errorbars = vcs.createerrorbars('eb')
            # Create a yx 1D plot
            yx = vcs.createyxvsx()
            yx.errorbars = errorbars
            # plot
            x.plot(data, yx, error)

    .. describe:: Create a new instance of errorbars:

        .. code-block:: python

            # Copies content of 'old' to 'new'
            eb = a.createerrorbars('new', 'old')
            # Copies content of 'default' to 'new'
            eb = a.createerrorbars('new')

    .. describe:: Modify an existing errorbars:

        .. code-block:: python

            eb = a.geterrorbars('eb')

    .. describe:: Overview of errorbars attributes:

        * List all the errorbars attribute values:

            .. code-block:: python

                eb.list()
                # Range from 1 to 256
                eb.color = 100
                # One of "x", "y" or "xy"
                eb.type = "y"

        * Specify the errorbars type:

            .. code-block:: python

                eb.type = 'x'
                eb.type = 'y'

    .. pragma: skip-doctest
    """
    __slots__ = [
        'name',
        's_name',
        'color',
        'type',
        '_name',
        '_color',
        '_type'
    ]

    def _getname(self):
        return self._name

    def _setname(self, value):
        value = VCS_validation_functions.checkname(self, 'name', value)
        if value is not None:
            self._name = value
    name = property(_getname, _setname)

    def _getcolor(self):
        return self._color

    def _setcolor(self, value):
        if isinstance(value, int):
            value = [value, ]
        if value is not None:
            value = VCS_validation_functions.checkColorList(
                self,
                'color',
                value)
        self._color = value
    color = property(_getcolor, _setcolor)

    def _gettype(self):
        return self._type

    def _settype(self, value):
        if value is not None:
            value = VCS_validation_functions.checkErrorBarsType(
                self,
                'type',
                value)
        self._type = value
    type = property(_gettype, _settype)

    def __init__(self, Te_name, Te_name_src='default'):
        if (Te_name is None):
            raise ValueError('Must provide an errorbar name.')
        self._name = Te_name
        self.s_name = 'Te'
        if Te_name == "default":
            self._type = "y"
            self._color = [0, 0, 0, 100]
        else:
            if isinstance(Te_name_src, Te):
                Te_name_src = Te_name_src.name
            if Te_name_src not in vcs.elements["errorbars"]:
                raise ValueError(
                    "The errorbars object '%s' does not exist" %
                    Te_name_src)
            src = vcs.elements["errorbars"][Te_name_src]
            for att in ['type', 'color']:
                setattr(self, att, getattr(src, att))
        # Ok now we need to stick it in the elements
        vcs.elements["errorbars"][Te_name] = self

    def list(self):
        if (self.name == '__removed_from_VCS__'):
            raise ValueError('This instance has been removed from VCS.')
        print "---------- ErrorBars (Te) member (attribute) listings ----------"
        print "secondary method =", self.s_name
        print "name =", self.name
        print "type =", self.type
        print "color =", self.color
    list.__doc__ = listdoc.format(name="errorbars", parent="")

    def script(self, script_filename=None, mode=None):
        if (script_filename is None):
            raise ValueError(
                'Error - Must provide an output script file name.')

        if (mode is None):
            mode = 'a'
        elif (mode not in ('w', 'a')):
            raise ValueError(
                'Error - Mode can only be "w" for replace or "a" for append.')

        # By default, save file in json
        scr_type = script_filename.split(".")
        if len(scr_type) == 1 or len(scr_type[-1]) > 5:
            scr_type = "json"
            if script_filename != "initial.attributes":
                script_filename += ".json"
        else:
            scr_type = scr_type[-1]
        if scr_type == '.scr':
            raise vcs.VCSDeprecationWarning("scr script are no longer generated")
        elif scr_type == "py":
            mode = mode + '+'
            py_type = script_filename[
                len(script_filename) -
                3:len(script_filename)]
            if (py_type != '.py'):
                script_filename = script_filename + '.py'

            # Write to file
            fp = open(script_filename, mode)
            if (fp.tell() == 0):  # Must be a new file, so include below
                fp.write("#####################################\n")
                fp.write("#                                 #\n")
                fp.write("# Import and Initialize VCS     #\n")
                fp.write("#                             #\n")
                fp.write("#############################\n")
                fp.write("import vcs\n")
                fp.write("v=vcs.init()\n\n")

            unique_name = '__Te__' + self.name
            fp.write("#----------Errorbars (Te) member (attribute) listings ----------\n")
            fp.write("tm_list=v.listelements('errorbars')\n")
            fp.write("if ('%s' in tm_list):\n" % self.name)
            fp.write("   %s = v.geterrorbars('%s')\n" % (unique_name, self.name))
            fp.write("else:\n")
            fp.write("   %s = v.createerrorbars('%s')\n" % (unique_name, self.name))
            fp.write("%s.type = %s\n" % (unique_name, self.type))
            fp.write("%s.color = %s\n\n" % (unique_name, self.color))
        else:
            # Json type
            mode += "+"
            f = open(script_filename, mode)
            vcs.utils.dumpToJson(self, f)
            f.close()
    script.__doc__ = scriptdocs['errorbars']
