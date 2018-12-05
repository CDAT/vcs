"""
# Streamline (Gs) module
"""
###############################################################################
#                                                                             #
# Module:       streamline (Gs) module                                        #
#                                                                             #
# Copyright:    2000, Regents of the University of California                 #
#               This software may not be distributed to others without        #
#               permission of the author.                                     #
#                                                                             #
# Authors:      PCMDI Software Team                                           #
#               Lawrence Livermore NationalLaboratory:                        #
#               support@pcmdi.llnl.gov                                        #
#                                                                             #
# Description:  Python command wrapper for VCS's streamline graphics method.  #
#                                                                             #
# Version:      4.0                                                           #
#                                                                             #
###############################################################################
#
#
#
from __future__ import print_function
import vcs
from . import VCS_validation_functions
from .xmldocs import scriptdocs


class Gs(vcs.bestMatch):

    """
    The streamline graphics method displays a streamline plot of a 2D
    streamline field. A streamline is a path that a massless particle
    takes in a vector field. Streamlines are computed through numerical
    integration. Vcs can draw regular streamlines or evenly spaced streamlines.

    This class is used to define an streamline table entry used in VCS, or it
    can be used to change some or all of the streamline attributes in an
    existing streamline table entry.

    .. describe:: Useful Functions:

        .. code-block:: python

            # Constructor
            a=vcs.init()
            # Show predefined streamline graphics methods
            a.show('streamline')
            # Show predefined VCS line objects
            a.show('line')
            # Change the VCS color Map
            a.setcolormap("AMIP")
            # Plot 's1', and 's2' with streamline 'v' and 'default' template
            a.streamline(s1, s2, v,'default')
            # Updates the VCS Canvas at user's request
            a.update()

    .. describe:: Make a Canvas object to work with:

        .. code-block:: python

            a=vcs.init()

    .. describe:: Create a new instance of streamline:

        .. code-block:: python

            # Copies content of 'quick' to 'new'
            vc=a.createstreamline('new','quick')
            # Copies content of 'default' to 'new'
            vc=a.createstreamline('new')

    .. describe:: Modify an existing streamline:

        .. code-block:: python

            vc=a.getstreamline('AMIP_psl')

    .. describe:: Overview of streamline attributes:

        * List all attributes:

            .. code-block:: python

                # Will list all the streamline attribute values
                vc.list()

        * Set axis attributes:

            .. code-block:: python

                # Can only be 'linear'
                vc.projection='linear'
                lon30={-180:'180W',-150:'150W',0:'Eq'}
                vc.xticlabels1=lon30
                vc.xticlabels2=lon30
                # Will set them both
                vc.xticlabels(lon30, lon30)
                vc.xmtics1=''
                vc.xmtics2=''
                # Will set them both
                vc.xmtics(lon30, lon30)
                vc.yticlabels1=lat10
                vc.yticlabels2=lat10
                # Will set them both
                vc.yticlabels(lat10, lat10)
                vc.ymtics1=''
                vc.ymtics2=''
                # Will set them both
                vc.ymtics(lat10, lat10)
                vc.datawc_y1=-90.0
                vc.datawc_y2=90.0
                vc.datawc_x1=-180.0
                vc.datawc_x2=180.0
                # Will set them all
                vc.datawc(-90, 90, -180, 180)
                xaxisconvert='linear'
                yaxisconvert='linear'
                # Will set them both
                vc.xyscale('linear', 'area_wt')

        * Specify the line style:

            .. code-block:: python

                # Same as vc.line='solid'
                vc.line=0
                # Same as vc.line='dash'
                vc.line=1
                # Same as vc.line='dot'
                vc.line=2
                # Same as vc.line='dash-dot'
                vc.line=3
                # Same as vc.line='long-dot'
                vc.line=4

        * Specify the line color of the streamlines:

            .. code-block:: python

                # Color range: 16 to 230, default line color is black
                vc.linecolor=16
                # Width range: 1 to 100, default size is 1
                vc.linewidth=1

        * Specify the streamline reference:

            .. code-block:: python

                # Can be an integer or float
                vc.reference=4
        *

    """
    __slots__ = [
        'g_name',
        '_name',
        '_xaxisconvert',
        '_yaxisconvert',
        '_levels',
        '_ext_1',
        '_ext_2',
        '_fillareacolors',
        '_fillareastyle',
        '_linecolor',
        '_linetype',
        '_linewidth',
        '_projection',
        '_xticlabels1',
        '_xticlabels2',
        '_yticlabels1',
        '_yticlabels2',
        '_xmtics1',
        '_xmtics2',
        '_ymtics1',
        '_ymtics2',
        '_datawc_x1',
        '_datawc_x2',
        '_datawc_y1',
        '_datawc_y2',
        '_datawc_timeunits',
        '_datawc_calendar',
        '_reference',
        '_colormap',
        '_evenlyspaced',
        '_numberofseeds',
        '_startseed',
        '_separatingdistance',
        '_separatingdistanceratio',
        '_closedloopmaximumdistance',
        '_integratortype',
        '_integrationdirection',
        '_integrationstepunit',
        '_initialsteplength',
        '_minimumsteplength',
        '_maximumsteplength',
        '_maximumsteps',
        '_maximumstreamlinelength',
        '_terminalspeed',
        '_maximumerror',
        '_glyphscalefactor',
        '_glyphbasefactor',
        '_filledglyph',
        '_coloredbyvector',
        '_numberofglyphs',
    ]

    colormap = VCS_validation_functions.colormap

    def _getname(self):
        return self._name

    def _setname(self, value):
        value = VCS_validation_functions.checkname(self, 'name', value)
        if value is not None:
            self._name = value
    name = property(_getname, _setname)

    def _getcalendar(self):
        return self._datawc_calendar

    def _setcalendar(self, value):
        value = VCS_validation_functions.checkCalendar(
            self,
            'datawc_calendar',
            value)
        self._datawc_calendar = value
    datawc_calendar = property(_getcalendar, _setcalendar)

    def _gettimeunits(self):
        return self._datawc_timeunits

    def _settimeunits(self, value):
        value = VCS_validation_functions.checkTimeUnits(
            self,
            'datawc_timeunits',
            value)
        self._datawc_timeunits = value
    datawc_timeunits = property(_gettimeunits, _settimeunits)

    def _getxaxisconvert(self):
        return self._xaxisconvert

    def _setxaxisconvert(self, value):
        value = VCS_validation_functions.checkAxisConvert(
            self,
            'xaxisconvert',
            value)
        self._xaxisconvert = value
    xaxisconvert = property(_getxaxisconvert, _setxaxisconvert)

    def _getyaxisconvert(self):
        return self._yaxisconvert

    def _setyaxisconvert(self, value):
        value = VCS_validation_functions.checkAxisConvert(
            self,
            'yaxisconvert',
            value)
        self._yaxisconvert = value
    yaxisconvert = property(_getyaxisconvert, _setyaxisconvert)

    levels = VCS_validation_functions.levels
    ext_1 = VCS_validation_functions.ext_1
    ext_2 = VCS_validation_functions.ext_2
    fillareacolors = VCS_validation_functions.fillareacolors

    def _getfillareastyle(self):
        return self._fillareastyle
    fillareastyle = property(_getfillareastyle)

    def _getprojection(self):
        return self._projection

    def _setprojection(self, value):
        value = VCS_validation_functions.checkProjection(
            self,
            'projection',
            value)
        self._projection = value
    projection = property(_getprojection, _setprojection)

    def _getxticlabels1(self):
        return self._xticlabels1

    def _setxticlabels1(self, value):
        value = VCS_validation_functions.checkStringDictionary(
            self,
            'xticlabels1',
            value)
        self._xticlabels1 = value
    xticlabels1 = property(_getxticlabels1, _setxticlabels1)

    def _getxticlabels2(self):
        return self._xticlabels2

    def _setxticlabels2(self, value):
        value = VCS_validation_functions.checkStringDictionary(
            self,
            'xticlabels2',
            value)
        self._xticlabels2 = value
    xticlabels2 = property(_getxticlabels2, _setxticlabels2)

    def _getyticlabels1(self):
        return self._yticlabels1

    def _setyticlabels1(self, value):
        value = VCS_validation_functions.checkStringDictionary(
            self,
            'yticlabels1',
            value)
        self._yticlabels1 = value
    yticlabels1 = property(_getyticlabels1, _setyticlabels1)

    def _getyticlabels2(self):
        return self._yticlabels2

    def _setyticlabels2(self, value):
        value = VCS_validation_functions.checkStringDictionary(
            self,
            'yticlabels2',
            value)
        self._yticlabels2 = value
    yticlabels2 = property(_getyticlabels2, _setyticlabels2)

    def _getxmtics1(self):
        return self._xmtics1

    def _setxmtics1(self, value):
        value = VCS_validation_functions.checkStringDictionary(
            self,
            'xmtics1',
            value)
        self._xmtics1 = value
    xmtics1 = property(_getxmtics1, _setxmtics1)

    def _getxmtics2(self):
        return self._xmtics2

    def _setxmtics2(self, value):
        value = VCS_validation_functions.checkStringDictionary(
            self,
            'xmtics2',
            value)
        self._xmtics2 = value
    xmtics2 = property(_getxmtics2, _setxmtics2)

    def _getymtics1(self):
        return self._ymtics1

    def _setymtics1(self, value):
        value = VCS_validation_functions.checkStringDictionary(
            self,
            'ymtics1',
            value)
        self._ymtics1 = value
    ymtics1 = property(_getymtics1, _setymtics1)

    def _getymtics2(self):
        return self._ymtics2

    def _setymtics2(self, value):
        value = VCS_validation_functions.checkStringDictionary(
            self,
            'ymtics2',
            value)
        self._ymtics2 = value
    ymtics2 = property(_getymtics2, _setymtics2)

    def _getdatawc_x1(self):
        return self._datawc_x1

    def _setdatawc_x1(self, value):
        VCS_validation_functions.checkDatawc(self, 'datawc_x1', value)
        self._datawc_x1 = value
    datawc_x1 = property(_getdatawc_x1, _setdatawc_x1)

    def _getdatawc_x2(self):
        return self._datawc_x2

    def _setdatawc_x2(self, value):
        VCS_validation_functions.checkDatawc(self, 'datawc_x2', value)
        self._datawc_x2 = value
    datawc_x2 = property(_getdatawc_x2, _setdatawc_x2)

    def _getdatawc_y1(self):
        return self._datawc_y1

    def _setdatawc_y1(self, value):
        VCS_validation_functions.checkDatawc(self, 'datawc_y1', value)
        self._datawc_y1 = value
    datawc_y1 = property(_getdatawc_y1, _setdatawc_y1)

    def _getdatawc_y2(self):
        return self._datawc_y2

    def _setdatawc_y2(self, value):
        VCS_validation_functions.checkDatawc(self, 'datawc_y2', value)
        self._datawc_y2 = value
    datawc_y2 = property(_getdatawc_y2, _setdatawc_y2)

    def _getreference(self):
        return self._reference

    def _setreference(self, value):
        value = VCS_validation_functions.checkNumber(self, 'reference', value)
        self._reference = value
    reference = property(_getreference, _setreference)

    """Display evenly spaced streamlines.

    """
    def _getevenlyspaced(self):
        return self._evenlyspaced

    def _setevenlyspaced(self, value):
        value = VCS_validation_functions.checkBoolean(self, 'evenlyspaced', value)
        self._evenlyspaced = value
        if (self._integratortype == 2):
            self._integratortype = 1
    evenlyspaced = property(_getevenlyspaced, _setevenlyspaced)

    """Number of random seeds for starting streamlines. Default is 500.
       Not used for evenly spaced streamlines.

    """
    def _getnumberofseeds(self):
        return self._numberofseeds

    def _setnumberofseeds(self, value):
        value = VCS_validation_functions.checkNumber(self,
                                                     'numberofseeds', value)
        self._numberofseeds = value
    numberofseeds = property(_getnumberofseeds, _setnumberofseeds)

    """
       Position of the start seed. Used only for evenly spaced streamlines.
       By default is set to None which is taken to mean the middle of the domain.

    """
    def _getstartseed(self):
        return self._startseed

    def _setstartseed(self, value):
        if (value):
            value = VCS_validation_functions.checkListOfNumbers(
                self, 'startseed', value)
        self._startseed = value
    startseed = property(_getstartseed, _setstartseed)

    """Separating distance between equaly spaced streamlines at seeding time.
       It is expressed in integrationstepunit.

    """
    def _getseparatingdistance(self):
        return self._separatingdistance

    def _setseparatingdistance(self, value):
        value = VCS_validation_functions.checkNumber(self,
                                                     'separatingdistance', value)
        self._separatingdistance = value
    separatingdistance = property(_getseparatingdistance, _setseparatingdistance)

    """If the current streamline gets closer than
       separatingdistance * separatingdistanceratio to other streamlines the
       current streamline is terminated.

    """
    def _getseparatingdistanceratio(self):
        return self._separatingdistanceratio

    def _setseparatingdistanceratio(self, value):
        value = VCS_validation_functions.checkNumber(self,
                                                     'separatingdistanceratio', value)
        self._separatingdistanceratio = value
    separatingdistanceratio = property(_getseparatingdistanceratio, _setseparatingdistanceratio)

    """Maximum distance between two points that form a closed loop.
       Used only for evenly spaced streamlines. Should be set about the same as
       self.initialsteplength. Expressed in integrationstepunit.

    """
    def _getclosedloopmaximumdistance(self):
        return self._closedloopmaximumdistance

    def _setclosedloopmaximumdistance(self, value):
        value = VCS_validation_functions.checkNumber(self,
                                                     'closedloopmaximumdistance', value)
        self._closedloopmaximumdistance = value
    closedloopmaximumdistance = property(_getclosedloopmaximumdistance, _setclosedloopmaximumdistance)

    """Integrator type. Can be 0 for Runge-Kutta 2, 1 for Runge-Kutta 4
        and 2 for Runge-Kutta 4-5. Default is 1 - Runge-Kutta 4 for evenly
        spaced streamlines and 2 - Runge-Kutta 4-5 for regular streamlines.

    """
    def _getintegratortype(self):
        return self._integratortype

    def _setintegratortype(self, value):
        value = VCS_validation_functions.checkNumber(
            self, 'integratortype', value, 0, 2)
        self._integratortype = value
    integratortype = property(_getintegratortype, _setintegratortype)

    """Integration direction. Can be 0 - forward, 1 - backward or 2 -
        both. Default is 2 - both.
        For evenly spaced streamlines integration direction is always 2.

    """
    def _getintegrationdirection(self):
        return self._integrationdirection

    def _setintegrationdirection(self, value):
        value = VCS_validation_functions.checkNumber(
            self, 'integrationdirection', value, 0, 2)
        self._integrationdirection = value
    integrationdirection = property(_getintegrationdirection, _setintegrationdirection)

    """Integration stepunit. Can be 1 - length or 2 - cell
        length. Default is 2 - cell length.

    """
    def _getintegrationstepunit(self):
        return self._integrationstepunit

    def _setintegrationstepunit(self, value):
        value = VCS_validation_functions.checkNumber(
            self, 'integrationstepunit', value, 0, 2)
        self._integrationstepunit = value
    integrationstepunit = property(_getintegrationstepunit, _setintegrationstepunit)

    """This property specifies the initial integration step size
        expressed in integrationstepunit.  For
        non-adaptive integrators (Runge-Kutta 2 and Runge-Kutta 4), it
        is fixed (always equal to this initial value) throughout the
        integration.  For an adaptive integrator (Runge-Kutta 4-5),
        the actual step size varies such that the numerical error is
        less than a specified threshold.  Default is 0.2

    """
    def _getinitialsteplength(self):
        return self._initialsteplength

    def _setinitialsteplength(self, value):
        value = VCS_validation_functions.checkNumber(
            self, 'initialsteplength', value)
        self._initialsteplength = value
    initialsteplength = property(_getinitialsteplength, _setinitialsteplength)

    """When using the Runge-Kutta 4-5 integrator, this property specifies
       the minimum integration step size. Default is 0.1
       Not used for evenly spaced streamlines. Expressed in integrationstepunit.

    """
    def _getminimumsteplength(self):
        return self._minimumsteplength

    def _setminimumsteplength(self, value):
        value = VCS_validation_functions.checkNumber(
            self, 'minimumsteplength', value)
        self._minimumsteplength = value
    minimumsteplength = property(_getminimumsteplength, _setminimumsteplength)

    """When using the Runge-Kutta 4-5 integrator, this property specifies
       the maximum integration step size. Default is 0.5
       Not used for evenly spaced streamlines.  Expressed in integrationstepunit.

    """
    def _getmaximumsteplength(self):
        return self._maximumsteplength

    def _setmaximumsteplength(self, value):
        value = VCS_validation_functions.checkNumber(
            self, 'maximumsteplength', value)
        self._maximumsteplength = value
    maximumsteplength = property(_getmaximumsteplength, _setmaximumsteplength)

    """This property specifies the maximum number of steps, beyond which
    streamline integration is terminated. Default is 200.

    """
    def _getmaximumsteps(self):
        return self._maximumsteps

    def _setmaximumsteps(self, value):
        value = VCS_validation_functions.checkNumber(
            self, 'maximumsteps', value)
        self._maximumsteps = value
    maximumsteps = property(_getmaximumsteps, _setmaximumsteps)

    """This property specifies the maximum streamline length (i.e.,
       physical arc length), beyond which line integration is
       terminated.  This is specified as a percentage of the diagonal of
       the dataset. The default is 0.25.

    """
    def _getmaximumstreamlinelength(self):
        return self._maximumstreamlinelength

    def _setmaximumstreamlinelength(self, value):
        value = VCS_validation_functions.checkNumber(
            self, 'maximumstreamlinelength', value)
        self._maximumstreamlinelength = value
    maximumstreamlinelength = property(_getmaximumstreamlinelength, _setmaximumstreamlinelength)

    """This property specifies the terminal speed, below which particle
    advection/integration is terminated.

    """
    def _getterminalspeed(self):
        return self._terminalspeed

    def _setterminalspeed(self, value):
        value = VCS_validation_functions.checkNumber(
            self, 'terminalspeed', value)
        self._terminalspeed = value
    terminalspeed = property(_getterminalspeed, _setterminalspeed)

    """This property specifies the maximum error (for Runge-Kutta 4-5)
       tolerated throughout streamline integration. The Runge-Kutta
       4-5 integrator tries to adjust the step size such that the
       estimated error is less than this threshold.
       Not used for evenly spaced streamlines.

    """
    def _getmaximumerror(self):
        return self._maximumerror

    def _setmaximumerror(self, value):
        value = VCS_validation_functions.checkNumber(
            self, 'maximumerror', value)
        self._maximumerror = value
    maximumerror = property(_getmaximumerror, _setmaximumerror)

    """The constant multiplier used to scale the glyph showing the
        direction of the flow. One represents the diagonal of the
        bounding box of the dataset. Default value is 0.01
    """
    def _getglyphscalefactor(self):
        return self._glyphscalefactor

    def _setglyphscalefactor(self, value):
        value = VCS_validation_functions.checkNumber(
            self, 'glyphscalefactor', value)
        self._glyphscalefactor = value
    glyphscalefactor = property(_getglyphscalefactor, _setglyphscalefactor)

    """The constant multiplier used to scale the glyph base for the
        arrow showing the flow. The default is 0.75 for which the width of
        the arrow is 0.75 of its height.
    """
    def _getglyphbasefactor(self):
        return self._glyphbasefactor

    def _setglyphbasefactor(self, value):
        value = VCS_validation_functions.checkNumber(
            self, 'glyphbasefactor', value)
        self._glyphbasefactor = value
    glyphbasefactor = property(_getglyphbasefactor, _setglyphbasefactor)

    """ Do we draw the arrow glyph filled or we draw only edges
    """
    def _getfilledglyph(self):
        return self._filledglyph

    def _setfilledglyph(self, value):
        value = VCS_validation_functions.checkNumber(
            self, 'filledglyph', value)
        self._filledglyph = value
    filledglyph = property(_getfilledglyph, _setfilledglyph)

    """ If true streamlines are colored by vector magnitude.
        The mapping between vector magnitude and colors is controlled
        by levels, ext_1, ext_2 and fillareacolors. If false,
        streamlines have only one color linecolor.
    """
    def _getcoloredbyvector(self):
        return self._coloredbyvector

    def _setcoloredbyvector(self, value):
        value = VCS_validation_functions.checkBoolean(
            self, 'coloredbyvector', value)
        self._coloredbyvector = value
    coloredbyvector = property(_getcoloredbyvector, _setcoloredbyvector)

    """ Number of glyphs per streamline. The default is one, in which
        case the glyph is placed at the position where the streamline was
        seeded. Otherwise glyphs are placed equally spaced along the streamline.
        Not all streamlines will contain all glyphs as streamlines have
        different lenghts.
    """
    def _getnumberofglyphs(self):
        return self._numberofglyphs

    def _setnumberofglyphs(self, value):
        value = VCS_validation_functions.checkNumber(
            self, 'numberofglyphs', value)
        self._numberofglyphs = value
    numberofglyphs = property(_getnumberofglyphs, _setnumberofglyphs)

    def _getlinewidth(self):
        return self._linewidth

    def _setlinewidth(self, value):
        if value is not None:
            value = VCS_validation_functions.checkNumber(
                self,
                'linewidth',
                value,
                0,
                300)
        self._linewidth = value
    linewidth = property(_getlinewidth, _setlinewidth)

    def _getlinecolor(self):
        return self._linecolor

    def _setlinecolor(self, value):
        if value is not None:
            value = VCS_validation_functions.checkColor(
                self,
                'linecolor',
                value)
        self._linecolor = value
    linecolor = property(_getlinecolor, _setlinecolor)

    def _getlinetype(self):
        return self._linetype

    def _setlinetype(self, value):
        if value is not None:
            value = VCS_validation_functions.checkLineType(self, 'linetype', value)
        self._linetype = value
    linetype = property(_getlinetype, _setlinetype)

    def setLineAttributes(self, line):
        '''
        Set attributes linecolor, linewidth and linetype from line l.
        l can be a line name defined in vcs.elements or a line object
        '''
        vcs.setLineAttributes(self, line)

    def __init__(self, Gs_name, Gs_name_src='default'):
                #                                                         #
                ###########################################################
                # Initialize the streamline class and its members             #
                #                                                         #
                # The getGsmember function retrieves the values of the    #
                # streamline members in the C structure and passes back the   #
                # appropriate Python Object.                              #
                ###########################################################
                #                                                         #
        if Gs_name in vcs.elements["streamline"]:
            raise ValueError(
                "The streamline method '%s' already exists" % Gs_name)
        self.g_name = 'Gs'
        self._name = Gs_name
        if Gs_name == 'default':
            self._projection = "linear"
            self._xticlabels1 = "*"
            self._xticlabels2 = "*"
            self._xmtics1 = ""
            self._xmtics2 = ""
            self._yticlabels1 = "*"
            self._yticlabels2 = "*"
            self._ymtics1 = ""
            self._ymtics2 = ""
            self._datawc_y1 = 1.e20
            self._datawc_y2 = 1.e20
            self._datawc_x1 = 1.e20
            self._datawc_x2 = 1.e20
            self._xaxisconvert = "linear"
            self._yaxisconvert = "linear"
            self._linetype = None
            self._linecolor = None
            self._linewidth = None
            self._reference = 1.e20
            self._datawc_timeunits = "days since 2000"
            self._datawc_calendar = 135441
            self._colormap = None
            self._levels = ([1.0000000200408773e+20, 1.0000000200408773e+20],)
            self._ext_1 = False
            self._ext_2 = False
            self._fillareacolors = [1, ]
            self._fillareastyle = 'solid'
            self._evenlyspaced = True
            self._numberofseeds = 500
            self._startseed = None
            self._separatingdistance = 1
            self._separatingdistanceratio = 0.4
            self._closedloopmaximumdistance = 0.2
            self._integratortype = 1        # runge-kutta4
            self._integrationdirection = 2  # both
            self._integrationstepunit = 2   # cell length
            self._initialsteplength = 0.2
            self._minimumsteplength = 0.1
            self._maximumsteplength = 0.5
            self._maximumsteps = 200
            self._maximumstreamlinelength = 0.25
            self._terminalspeed = 0.1
            self._maximumerror = 0.1
            self._glyphscalefactor = 0.01
            self._glyphbasefactor = 0.75
            self._filledglyph = True
            self._coloredbyvector = True
            self._numberofglyphs = 1
        else:
            if isinstance(Gs_name_src, Gs):
                Gs_name_src = Gs_name_src.name
            if Gs_name_src not in vcs.elements['streamline']:
                raise ValueError(
                    "The streamline method '%s' does not exists" %
                    Gs_name_src)
            src = vcs.elements["streamline"][Gs_name_src]
            for att in\
                ['projection',
                 'xticlabels1', 'xticlabels2', 'xmtics1', 'xmtics2',
                 'yticlabels1', 'yticlabels2', 'ymtics1', 'ymtics2',
                 'datawc_y1', 'datawc_y2', 'datawc_x1',
                 'datawc_x2', 'xaxisconvert', 'yaxisconvert', 'levels',
                 'ext_1', 'ext_2', 'fillareacolors',
                 'linetype', 'linecolor', 'linewidth', 'datawc_timeunits',
                 'datawc_calendar', 'colormap', 'integratortype', 'evenlyspaced',
                 'numberofseeds',
                 'startseed', 'separatingdistance', 'separatingdistanceratio',
                 'closedloopmaximumdistance', 'integrationdirection',
                 'integrationstepunit', 'initialsteplength', 'minimumsteplength',
                 'maximumsteplength', 'maximumsteps', 'maximumstreamlinelength',
                 'terminalspeed', 'maximumerror', 'glyphscalefactor',
                 'glyphbasefactor', 'filledglyph', 'coloredbyvector',
                 'numberofglyphs', 'reference']:

                setattr(self, att, getattr(src, att))
        # Ok now we need to stick in the elements
        vcs.elements["streamline"][Gs_name] = self

    def xticlabels(self, xtl1='', xtl2=''):
        mode = self.parent.mode
        self.parent.mode = 0
        self.xticlabels1 = xtl1
        self.parent.mode = mode
        self.xticlabels2 = xtl2

    def xmtics(self, xmt1='', xmt2=''):
        mode = self.parent.mode
        self.parent.mode = 0
        self.xmtics1 = xmt1
        self.parent.mode = mode
        self.xmtics2 = xmt2

    def yticlabels(self, ytl1='', ytl2=''):
        mode = self.parent.mode
        self.parent.mode = 0
        self.yticlabels1 = ytl1
        self.parent.mode = mode
        self.yticlabels2 = ytl2

    def ymtics(self, ymt1='', ymt2=''):
        mode = self.parent.mode
        self.parent.mode = 0
        self.ymtics1 = ymt1
        self.parent.mode = mode
        self.ymtics2 = ymt2

    def datawc(self, dsp1=1e20, dsp2=1e20, dsp3=1e20, dsp4=1e20):
        mode = self.parent.mode
        self.parent.mode = 0
        self.datawc_y1 = dsp1
        self.datawc_y2 = dsp2
        self.datawc_x1 = dsp3
        self.parent.mode = mode
        self.datawc_x2 = dsp4

    def xyscale(self, xat='', yat=''):
        mode = self.parent.mode
        self.parent.mode = 0
        self.xaxisconvert = xat
        self.parent.mode = mode
        self.yaxisconvert = yat

    def colors(self, color1=16, color2=239):
        self.fillareacolors = list(range(color1, color2))

    def exts(self, ext1='n', ext2='y'):
        self.ext_1 = ext1
        self.ext_2 = ext2

    def list(self):
        print("", "--------Streamline (Gs) member (attribute) listings --------")
        print("graphics method =", self.g_name)
        print("name =", self.name)
        print("projection =", self.projection)
        print("xticlabels1 =", self.xticlabels1)
        print("xticlabels2 =", self.xticlabels2)
        print("xmtics1 =", self.xmtics1)
        print("xmtics2 =", self.xmtics2)
        print("yticlabels1 =", self.yticlabels1)
        print("yticlabels2 =", self.yticlabels2)
        print("ymtics1 = ", self.ymtics1)
        print("ymtics2 = ", self.ymtics2)
        print("datawc_x1 =", self.datawc_x1)
        print("datawc_y1 = ", self.datawc_y1)
        print("datawc_x2 = ", self.datawc_x2)
        print("datawc_y2 = ", self.datawc_y2)
        print("datawc_timeunits = ", self.datawc_timeunits)
        print("datawc_calendar = ", self.datawc_calendar)
        print("xaxisconvert = ", self.xaxisconvert)
        print("yaxisconvert = ", self.yaxisconvert)
        print("levels = ", self.levels)
        print("ext_1 = ", self.ext_1)
        print("ext_2 = ", self.ext_2)
        print('fillareacolors =', self.fillareacolors)
        print("linetype = ", self.linetype)
        print("linecolor = ", self.linecolor)
        print("linewidth = ", self.linewidth)
        print("reference = ", self.reference)
        print("evenlyspaced = ", self.evenlyspaced)
        print("numberofseeds = ", self.numberofseeds)
        print("startseed = ", self.startseed)
        print("separatingdistance = ", self.separatingdistance)
        print("separatingdistanceratio = ", self.separatingdistanceratio)
        print("closedloopmaximumdistance = ", self.closedloopmaximumdistance)
        print("integratortype = ", self.integratortype)
        print("integrationdirection = ", self.integrationdirection)
        print("integrationstepunit = ", self.integrationstepunit)
        print("initialsteplength = ", self.initialsteplength)
        print("minimumsteplength = ", self.minimumsteplength)
        print("maximumsteplength = ", self.maximumsteplength)
        print("maximumsteps = ", self.maximumsteps)
        print("maximumstreamlinelength = ", self.maximumstreamlinelength)
        print("terminalspeed = ", self.terminalspeed)
        print("maximumerror = ", self.maximumerror)
        print("glyphscalefactor = ", self.glyphscalefactor)
        print("glyphbasefactor = ", self.glyphbasefactor)
        print("filledglyph = ", self.filledglyph)
        print("coloredbyvector = ", self.coloredbyvector)
        print("numberofglyphs = ", self.numberofglyphs)

    ##########################################################################
    #                                                                         #
    # Script streamline (Gs) object to a file.                                #
    #                                                                         #
    ##########################################################################
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
                fp.write("#                                   #\n")
                fp.write("# Import and Initialize VCS         #\n")
                fp.write("#                                   #\n")
                fp.write("#####################################\n")
                fp.write("import vcs\n")
                fp.write("v=vcs.init()\n\n")

            unique_name = '__Gs__' + self.name
            fp.write(
                "#------Streamline (Gs) member (attribute) listings ------\n")
            fp.write("gv_list=v.listelements('streamline')\n")
            fp.write("if ('%s' in gv_list):\n" % self.name)
            fp.write(
                "   %s = v.getstreamline('%s')\n" % (unique_name, self.name))
            fp.write("else:\n")
            fp.write(
                "   %s = v.createstreamline('%s')\n" %
                (unique_name, self.name))
            # Common core graphics method attributes
            fp.write("%s.projection = '%s'\n" % (unique_name, self.projection))
            fp.write(
                "%s.xticlabels1 = '%s'\n" %
                (unique_name, self.xticlabels1))
            fp.write(
                "%s.xticlabels2 = '%s'\n" %
                (unique_name, self.xticlabels2))
            fp.write("%s.xmtics1 = '%s'\n" % (unique_name, self.xmtics1))
            fp.write("%s.xmtics2 = '%s'\n" % (unique_name, self.xmtics2))
            fp.write(
                "%s.yticlabels1 = '%s'\n" %
                (unique_name, self.yticlabels1))
            fp.write(
                "%s.yticlabels2 = '%s'\n" %
                (unique_name, self.yticlabels2))
            fp.write("%s.ymtics1 = '%s'\n" % (unique_name, self.ymtics1))
            fp.write("%s.ymtics2 = '%s'\n" % (unique_name, self.ymtics2))
            if isinstance(self.datawc_x1, (int, float)):
                fp.write("%s.datawc_x1 = %g\n" % (unique_name, self.datawc_x1))
            else:
                fp.write(
                    "%s.datawc_x1 = '%s'\n" %
                    (unique_name, self.datawc_x1))
            if isinstance(self.datawc_y1, (int, float)):
                fp.write("%s.datawc_y1 = %g\n" % (unique_name, self.datawc_y1))
            else:
                fp.write(
                    "%s.datawc_y1 = '%s'\n" %
                    (unique_name, self.datawc_y1))
            if isinstance(self.datawc_x2, (int, float)):
                fp.write("%s.datawc_x2 = %g\n" % (unique_name, self.datawc_x2))
            else:
                fp.write(
                    "%s.datawc_x2 = '%s'\n" %
                    (unique_name, self.datawc_x2))
            if isinstance(self.datawc_y2, (int, float)):
                fp.write("%s.datawc_y2 = %g\n" % (unique_name, self.datawc_y2))
            else:
                fp.write(
                    "%s.datawc_y2 = '%s'\n" %
                    (unique_name, self.datawc_y2))
            fp.write(
                "%s.datawc_calendar = %g\n" %
                (unique_name, self.datawc_calendar))
            fp.write(
                "%s.datawc_timeunits = '%s'\n\n" %
                (unique_name, self.datawc_timeunits))
            fp.write(
                "%s.xaxisconvert = '%s'\n" %
                (unique_name, self.xaxisconvert))
            fp.write(
                "%s.yaxisconvert = '%s'\n" %
                (unique_name, self.yaxisconvert))
            fp.write("%s.levels = '%s'\n" % (unique_name, self.levels))
            fp.write("%s.ext_1 = '%s'\n" % (unique_name, self.ext_1))
            fp.write("%s.ext_2 = '%s'\n" % (unique_name, self.ext_2))
            fp.write("%s.fillareacolors = '%s'\n" %
                     (unique_name, self.fillareacolors))
            fp.write("%s.fillareastyle = '%s'\n" %
                     (unique_name, self.fillareastyle))

            # Unique attribute for streamline
            fp.write("%s.linetype = %s\n" % (unique_name, self.linetype))
            fp.write("%s.linecolor = %s\n" % (unique_name, self.linecolor))
            fp.write("%s.linewidth = %s\n" % (unique_name, self.linewidth))
            fp.write("%s.reference = %s\n\n" % (unique_name, self.reference))
            fp.write(
                "%s.colormap = '%s'\n\n" %
                (unique_name, repr(
                    self.colormap)))
            fp.write("%s.evenlyspaced = %r\n" % (unique_name, self.evenlyspaced))
            fp.write("%s.numberofseeds = %d\n" % (unique_name, self.numberofseeds))
            if self.startseed is not None:
                fp.write("%s.startseed = [%d,%d,%d]\n" % (unique_name, self.startseed[0],
                                                          self.startseed[1], self.startseed[2]))
            else:
                fp.write("%s.startseed = None\n")
            fp.write("%s.separatingdistance = %d\n" % (unique_name, self.separatingdistance))
            fp.write("%s.separatingdistanceratio = %d\n" % (unique_name, self.separatingdistanceratio))
            fp.write("%s.closedloopmaximumdistance = %d\n" % (unique_name, self.closedloopmaximumdistance))
            fp.write("%s.integratortype = %d\n" % (unique_name, self.integratortype))
            fp.write("%s.integrationdirection = %d\n" % (unique_name, self.integrationdirection))
            fp.write("%s.integrationstepunit = %d\n" % (unique_name, self.integrationstepunit))
            fp.write("%s.initialsteplength = %d\n" % (unique_name, self.initialsteplength))
            fp.write("%s.minimumsteplength = %d\n" % (unique_name, self.minimumsteplength))
            fp.write("%s.maximumsteplength = %d\n" % (unique_name, self.maximumsteplength))
            fp.write("%s.maximumsteps = %d\n" % (unique_name, self.maximumsteps))
            fp.write("%s.maximumstreamlinelength = %d\n" % (unique_name, self.maximumstreamlinelength))
            fp.write("%s.terminalspeed = %d\n" % (unique_name, self.terminalspeed))
            fp.write("%s.maximumerror = %d\n" % (unique_name, self.maximumerror))
            fp.write("%s.glyphscalefactor = %d\n" % (unique_name, self.glyphscalefactor))
            fp.write("%s.glyphbasefactor = %d\n" % (unique_name, self.glyphbasefactor))
            fp.write("%s.filledglyph = %r\n" % (unique_name, self.filledglyph))
            fp.write("%s.coloredbyvector = %r\n" % (unique_name, self.coloredbyvector))
            fp.write("%s.numberofglyphs = %d\n" % (unique_name, self.numberofglyphs))
        else:
            # Json type
            mode += "+"
            f = open(script_filename, mode)
            vcs.utils.dumpToJson(self, f)
            f.close()
    script.__doc__ = scriptdocs['streamline']  # noqa
