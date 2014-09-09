"""
# Outfill (Gfo) module
"""
###############################################################################
#                                                                             #
# Module:       outfill (Gfo) module                                          #
#                                                                             #
# Copyright:    2000, Regents of the University of California                 #
#               This software may not be distributed to others without        #
#               permission of the author.                                     #
#                                                                             #
# Author:       PCMDI Software Team                                           #
#               Lawrence Livermore NationalLaboratory:                        #
#               support@pcmdi.llnl.gov                                        #
#                                                                             #
# Description:  Python command wrapper for VCS's outfill graphics method.     #
#                                                                             #
# Version:      5.0                                                           #
#                                                                             #
###############################################################################
#
#
#
import queries, vcs, VCS_validation_functions, cdtime
import Canvas
from types import *
import AutoAPI
import xmldocs

###############################################################################
#                                                                             #
# Function:	setGfomember                                                  #
#                                                                             #
# Description of Function:                                                    #
# 	Private function to update the VCS canvas plot. If the canvas mode is #
#       set to 0, then this function does nothing.              	      #
#                                                                             #
#                                                                             #
# Example of Use:                                                             #
#      setGfomember(self,name,value)					      #
#              where: self is the class (e.g., Gfo)                           #
#                     name is the name of the member that is being changed    #
#                     value is the new value of the member (or attribute)     #
#                                                                             #
###############################################################################
def setGfomember(self,member,value):
     # If the VCS Canvas is displayed, then bring the canvas to the front before 
     # redisplaying the updated contents.
     if (self.parent.mode == 1) and (self.parent.iscanvasdisplayed()):
        Canvas.finish_queued_X_server_requests( self.parent )
        self.parent.canvas.BLOCK_X_SERVER()
        self.parent.canvasraised()

     _vcs.setGfomember(self, member, value, self.parent.mode)

     # If the VCS Canvas is displayed, then update the backing store
     if (self.parent.mode == 1) and (self.parent.iscanvasdisplayed()):
        self.parent.flush()
        self.parent.backing_store()
        self.parent.canvas.UNBLOCK_X_SERVER()
setmember = setGfomember

###############################################################################
#                                                                             #
# Function:     getGfomember                                                  #
#                                                                             #
# Description of Function:                                                    #
#       Private function that retrieves the outfill members from the C        #
#       structure and passes it back to Python.                               #
#                                                                             #
#                                                                             #
# Example of Use:                                                             #
#      return_value =							      #
#      getGfomember(self,name)                                                #
#              where: self is the class (e.g., Gfo)                           #
#                     name is the name of the member that is being found      #
#                                                                             #
###############################################################################
def getGfomember(self,member):
     return _vcs.getGfomember(self,member)
getmember = getGfomember

###############################################################################
#                                                                             #
# Function:     renameGfo                                                     #
#                                                                             #
# Description of Function:                                                    #
#       Private function that renames the name of an existing outfill         #
#       graphics method.                                                      #
#                                                                             #
#                                                                             #
# Example of Use:                                                             #
#      renameGfo(old_name, new_name)                                          #
#              where: old_name is the current name of outfill graphics method #
#                     new_name is the new name for the outfill graphics method#
#                                                                             #
###############################################################################
def renameGfo(self, old_name, new_name):
     return _vcs.renameGfo(old_name, new_name)

class Gfo(object,AutoAPI.AutoAPI):
    """
    Options:::
%s
%s
%s
:::

 Class:	Gfo				# Outfill

 Description of Gfo Class:
    The outfill graphics method fills a set of integer values in any data array.
    Its primary purpose is to display continents by filling their area as defined
    by a surface type array that indicates land, ocean, and sea-ice points. The
    example below shows how to apply the outfill graphics method and how to modify 
    Fillarea and outfill attributes.

 Other Useful Functions:
	    a=vcs.init()		# Constructor
	    a.show('outfill')		# Show predefined outfill graphics methods
	    a.show('line')		# Show predefined VCS line objects
	    a.setcolormap("AMIP")	# Change the VCS color map
	    a.outfill(s,o,'default') 	# Plot data 's' with outfill 'o' and
				               'default' template
	    a.update()		 	# Updates the VCS Canvas at user's request
	    a.mode=1, or 0 		# If 1, then automatic update, else if
				          0, then use update function to
				          update the VCS Canvas.

 Example of Use:
    a=vcs.init()
    To Create a new instance of outfill use:
     out=a.createoutfill('new','quick') # Copies content of 'quick' to 'new'
     out=a.createoutfill('new') 	# Copies content of 'default' to 'new'

    To Modify an existing outfill use:
     out=a.getoutfill('AMIP_psl')

    out.list()  			# Will list all the outfill attribute values
    out.projection='linear'
    lon30={-180:'180W',-150:'150W',0:'Eq'}
    out.xticlabels1=lon30
    out.xticlabels2=lon30
    out.xticlabels(lon30, lon30)  	# Will set them both
    out.xmtics1=''
    out.xmtics2=''
    out.xmtics(lon30, lon30)  		# Will set them both
    out.yticlabels1=lat10
    out.yticlabels2=lat10
    out.yticlabels(lat10, lat10)  	# Will set them both
    out.ymtics1=''
    out.ymtics2=''
    out.ymtics(lat10, lat10)  		# Will set them both
    out.datawc_y1=-90.0
    out.datawc_y2=90.0
    out.datawc_x1=-180.0
    out.datawc_x2=180.0
    out.datawc(-90, 90, -180, 180)  	# Will set them all
    xaxisconvert='linear'
    yaxisconvert='linear'
    out.xyscale('linear', 'area_wt')	# Will set them both

 Specify the outfill fill values:
    out.outfill=([0,1,2,3,4])   	# Same as below
    out.outfill=(0,1,2,3,4)		# Will specify the outfill values

 There are four possibilities for setting the color index (Ex):
    out.fillareacolor=22 		# Same as below
    out.fillareacolor=(22) 		# Same as below
    out.fillareacolor=([22]) 		# Will set the outfill to a specific
					#  	color index
    out.fillareacolor=None		# Turns off the color index
"""
    rename=renameGfo # Alias for VCS_Validation_Functions
    __slots__=[
         'parent',
         'name',
         'g_name',
         'xaxisconvert',
         'yaxisconvert',
         'fillareacolor',
         'fillareastyle',
         'fillareaindex',
         'outfill',
         'projection',
         'xticlabels1',
         'xticlabels2',
         'yticlabels1',
         'yticlabels2',
         'xmtics1',
         'xmtics2',
         'ymtics1',
         'ymtics2',
         'datawc_x1',
         'datawc_x2',
         'datawc_y1',
         'datawc_y2',
         'datawc_timeunits',
         'datawc_calendar',
         '_name',
         '_xaxisconvert',
         '_yaxisconvert',
         '_fillareacolor',
         '_fillareastyle',
         '_fillareaindex',
         '_outfill',
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
         ]
 
    def _getname(self):
         return self._name
    def _setname(self,value):
         value=VCS_validation_functions.checkname(self,'name',value)
         if value is not None:
              self._name=value
              setmember(self,'name',value)
    name=property(_getname,_setname)

    def _getcalendar(self):
         return self._datawc_calendar
    def _setcalendar(self,value):
         value=VCS_validation_functions.checkCalendar(self,'datawc_calendar',value)
         setmember(self,'datawc_calendar',value)
         self._datawc_calendar=value
    datawc_calendar=property(_getcalendar,_setcalendar)

    def _gettimeunits(self):
         return self._datawc_timeunits
    def _settimeunits(self,value):
         value=VCS_validation_functions.checkTimeUnits(self,'datawc_timeunits',value)
         setmember(self,'datawc_timeunits',value)
         self._datawc_timeunits=value
    datawc_timeunits=property(_gettimeunits,_settimeunits)

    def _getxaxisconvert(self):
         return self._xaxisconvert
    def _setxaxisconvert(self,value):
         value=VCS_validation_functions.checkAxisConvert(self,'xaxisconvert',value)
         self._xaxisconvert=value
         setmember(self,'xaxisconvert',value)
    xaxisconvert=property(_getxaxisconvert,_setxaxisconvert)

    def _getyaxisconvert(self):
         return self._yaxisconvert
    def _setyaxisconvert(self,value):
         value=VCS_validation_functions.checkAxisConvert(self,'yaxisconvert',value)
         self._yaxisconvert=value
         setmember(self,'yaxisconvert',value)
    yaxisconvert=property(_getyaxisconvert,_setyaxisconvert)


    def _getfillareacolor(self):
         return self._fillareacolor
    def _setfillareacolor(self,value):
         if not value is None:
              value = VCS_validation_functions.checkColor(self,'fillareacolor',value)
         self._fillareacolor=value
         setmember(self,'outfill',self.outfill)
    fillareacolor=property(_getfillareacolor,_setfillareacolor)

    def _getfillareaindex(self):
         return self._fillareaindex
    def _setfillareaindex(self,value):
         if value is not None:
              value = VCS_validation_functions.checkIndex(self,'fillareaindex',value)
         self._fillareaindex=value
         setmember(self,'outfill',self.outfill)
    fillareaindex=property(_getfillareaindex,_setfillareaindex)

    def _getfillareastyle(self):
         return self._fillareastyle
    def _setfillareastyle(self,value):
         if value is not None:
              value=VCS_validation_functions.checkFillAreaStyle(self,'fillareastyle',value)
         else:
              value='solid'
         self._fillareastyle=value
         setmember(self,'outfill',self.outfill)
    fillareastyle=property(_getfillareastyle,_setfillareastyle)

    def _getoutfill(self):
         return self._outfill
    def _setoutfill(self,value):
         if (type(value) in (ListType, TupleType, IntType, FloatType)):
              value = list(value)  # make sure that values list is a list
              if (len(value) > 10):
                   raise ValueError, 'The outfill attribute must have less than 10 values.'
              else:
                   self._outfill=value
                   setmember(self,'outfill',value) # update the plot
         else:
              raise ValueError, 'The outfill attribute must be a tuple or list of values.'
    outfill=property(_getoutfill,_setoutfill)

    def _getprojection(self):
         return self._projection
    def _setprojection(self,value):
         value=VCS_validation_functions.checkProjection(self,'projection',value)
         self._projection=value
         setmember(self,'projection',value)
    projection=property(_getprojection,_setprojection)

    def _getxticlabels1(self):
         return self._xticlabels1
    def _setxticlabels1(self,value):
         value=VCS_validation_functions.checkStringDictionary(self,'xticlabels1',value)
         self._xticlabels1=value
         setmember(self,'xticlabels1',value)
    xticlabels1=property(_getxticlabels1,_setxticlabels1)

    def _getxticlabels2(self):
         return self._xticlabels2
    def _setxticlabels2(self,value):
         value=VCS_validation_functions.checkStringDictionary(self,'xticlabels2',value)
         self._xticlabels2=value
         setmember(self,'xticlabels2',value)
    xticlabels2=property(_getxticlabels2,_setxticlabels2)

    def _getyticlabels1(self):
         return self._yticlabels1
    def _setyticlabels1(self,value):
         value=VCS_validation_functions.checkStringDictionary(self,'yticlabels1',value)
         self._yticlabels1=value
         setmember(self,'yticlabels1',value)
    yticlabels1=property(_getyticlabels1,_setyticlabels1)

    def _getyticlabels2(self):
         return self._yticlabels2
    def _setyticlabels2(self,value):
         value=VCS_validation_functions.checkStringDictionary(self,'yticlabels2',value)
         self._yticlabels2=value
         setmember(self,'yticlabels2',value)
    yticlabels2=property(_getyticlabels2,_setyticlabels2)

    def _getxmtics1(self):
         return self._xmtics1
    def _setxmtics1(self,value):
         value=VCS_validation_functions.checkStringDictionary(self,'xmtics1',value)
         self._xmtics1=value
         setmember(self,'xmtics1',value)
    xmtics1=property(_getxmtics1,_setxmtics1)

    def _getxmtics2(self):
         return self._xmtics2
    def _setxmtics2(self,value):
         value=VCS_validation_functions.checkStringDictionary(self,'xmtics2',value)
         self._xmtics2=value
         setmember(self,'xmtics2',value)
    xmtics2=property(_getxmtics2,_setxmtics2)

    def _getymtics1(self):
         return self._ymtics1
    def _setymtics1(self,value):
         value=VCS_validation_functions.checkStringDictionary(self,'ymtics1',value)
         self._ymtics1=value
         setmember(self,'ymtics1',value)
    ymtics1=property(_getymtics1,_setymtics1)

    def _getymtics2(self):
         return self._ymtics2
    def _setymtics2(self,value):
         value=VCS_validation_functions.checkStringDictionary(self,'ymtics2',value)
         self._ymtics2=value
         setmember(self,'ymtics2',value)
    ymtics2=property(_getymtics2,_setymtics2)

    def _getdatawc_x1(self):
         if getmember(self,'_tdatawc_x1') :
              return cdtime.reltime(self._datawc_x1,self.datawc_timeunits).tocomp(self.datawc_calendar)
         else:
              return self._datawc_x1
    def _setdatawc_x1(self,value):
         value=VCS_validation_functions.checkDatawc(self,'datawc_x1',value)
         self._datawc_x1=value[0]
         setmember(self,'datawc_x1',value[0])
         setmember(self,'_tdatawc_x1',value[1])
    datawc_x1=property(_getdatawc_x1,_setdatawc_x1)

    def _getdatawc_x2(self):
         if getmember(self,'_tdatawc_x2') :
              return cdtime.reltime(self._datawc_x2,self.datawc_timeunits).tocomp(self.datawc_calendar)
         else:
              return self._datawc_x2
    def _setdatawc_x2(self,value):
         value=VCS_validation_functions.checkDatawc(self,'datawc_x2',value)
         self._datawc_x2=value[0]
         setmember(self,'datawc_x2',value[0])
         setmember(self,'_tdatawc_x2',value[1])
    datawc_x2=property(_getdatawc_x2,_setdatawc_x2)
    
    def _getdatawc_y1(self):
         if getmember(self,'_tdatawc_y1') :
              return cdtime.reltime(self._datawc_y1,self.datawc_timeunits).tocomp(self.datawc_calendar)
         else:
              return self._datawc_y1
    def _setdatawc_y1(self,value):
         value=VCS_validation_functions.checkDatawc(self,'datawc_y1',value)
         self._datawc_y1=value[0]
         setmember(self,'datawc_y1',value[0])
         setmember(self,'_tdatawc_y1',value[1])
    datawc_y1=property(_getdatawc_y1,_setdatawc_y1)

    def _getdatawc_y2(self):
         if getmember(self,'_tdatawc_y2') :
              return cdtime.reltime(self._datawc_y2,self.datawc_timeunits).tocomp(self.datawc_calendar)
         else:
              return self._datawc_y2
    def _setdatawc_y2(self,value):
         value=VCS_validation_functions.checkDatawc(self,'datawc_y2',value)
         self._datawc_y2=value[0]
         setmember(self,'datawc_y2',value[0])
         setmember(self,'_tdatawc_y2',value[1])
    datawc_y2=property(_getdatawc_y2,_setdatawc_y2)

    def __init__(self, parent, Gfo_name=None, Gfo_name_src='default', createGfo=0):
	#                                                         #
        ###########################################################
	# Initialize the outfill class and its members            #
        #							  #
	# The getGfomember function retrieves the values of the   #
        # outfill members in the C structure and passes back the  #
	# appropriate Python Object.                              #
        ###########################################################
	#                                                         #
        self.parent=parent
        if (createGfo == 0):
           if (Gfo_name == None):
              raise ValueError, 'Must provide a outfill name.'
           else:
              _vcs.copyGfo(Gfo_name_src, Gfo_name)
              self._name = Gfo_name
        else:
              self._name = Gfo_name_src
        self._projection=getmember(self, 'projection')
        self._xticlabels1=getmember(self, 'xticlabels1')
        self._xticlabels2=getmember(self, 'xticlabels2')
        self._xmtics1=getmember(self, 'xmtics1')
        self._xmtics2=getmember(self, 'xmtics2')
        self._yticlabels1=getmember(self, 'yticlabels1')
        self._yticlabels2=getmember(self, 'yticlabels2')
        self._ymtics1=getmember(self, 'ymtics1')
        self._ymtics2=getmember(self, 'ymtics2')
        self._datawc_y1=getmember(self, 'datawc_y1')
        self._datawc_y2=getmember(self, 'datawc_y2')
        self._datawc_x1=getmember(self, 'datawc_x1')
        self._datawc_x2=getmember(self, 'datawc_x2')
        self.g_name='Gfo'
        self._xaxisconvert=getmember(self, 'xaxisconvert')
        self._yaxisconvert=getmember(self, 'yaxisconvert')
        self._fillareastyle='solid'
        self._fillareaindex=None
        self._fillareacolor=None
        self._outfill=getmember(self,'outfill')
        self._datawc_timeunits=getmember(self, 'datawc_timeunits')
        self._datawc_calendar=getmember(self, 'datawc_calendar')
        self.info=AutoAPI.Info(self)
        self.info.expose=['ALL']
        #self.info.hide+=["fillareastyle","fillareaindices"]
        self.__doc__ = self.__doc__ % (xmldocs.graphics_method_core,xmldocs.fillareadoc,xmldocs.outfilldoc)


# 
# Doesn't make sense to inherit. This would mean more coding in C.
# I put this code back.                                 
#
    def xticlabels(self, xtl1='', xtl2=''):
        mode=self.parent.mode
        self.parent.mode=0
        self.xticlabels1 = xtl1
        self.parent.mode=mode
        self.xticlabels2 = xtl2
    xticlabels.__doc__ = xmldocs.xticlabelsdoc

    def xmtics(self,xmt1='', xmt2=''):
        mode=self.parent.mode
        self.parent.mode=0
        self.xmtics1 = xmt1
        self.parent.mode=mode
        self.xmtics2 = xmt2
    xmtics.__doc__ = xmldocs.xmticsdoc

    def yticlabels(self, ytl1='', ytl2=''):
        mode=self.parent.mode
        self.parent.mode=0
        self.yticlabels1 = ytl1
        self.parent.mode=mode
        self.yticlabels2 = ytl2
    yticlabels.__doc__ = xmldocs.yticlabelsdoc

    def ymtics(self, ymt1='', ymt2=''):
        mode=self.parent.mode
        self.parent.mode=0
        self.ymtics1 = ymt1
        self.parent.mode=mode
        self.ymtics2 = ymt2
    ymtics.__doc__ = xmldocs.ymticsdoc

    def datawc(self, dsp1=1e20, dsp2=1e20, dsp3=1e20, dsp4=1e20):
        mode=self.parent.mode
        self.parent.mode=0
        self.datawc_y1 = dsp1
        self.datawc_y2 = dsp2
        self.datawc_x1 = dsp3
        self.parent.mode=mode
        self.datawc_x2 = dsp4
    datawc.__doc__ = xmldocs.datawcdoc

    def xyscale(self, xat='', yat=''):
        mode=self.parent.mode
        self.parent.mode=0
        self.xaxisconvert = xat
        self.parent.mode=mode
        self.yaxisconvert = yat
    xyscale.__doc__= xmldocs.xyscaledoc

    def list(self):
        if (self.name == '__removed_from_VCS__'):
           raise ValueError, 'This instance has been removed from VCS.'
        print "","----------Outfill (Gfo) member (attribute) listings ----------"
        print 'Canvas Mode =',self.parent.mode
        print "graphics method =", self.g_name
        print "name =", self.name
        print "projection =", self.projection
        print "xticlabels1 =", self.xticlabels1
        print "xticlabels2 =", self.xticlabels2
        print "xmtics1 =", self.xmtics1
        print "xmtics2 =", self.xmtics2
        print "yticlabels1 =", self.yticlabels1
        print "yticlabels2 =", self.yticlabels2
        print "ymtics1 = ", self.ymtics1
        print "ymtics2 = ", self.ymtics2
        print "datawc_x1 =", self.datawc_x1
        print "datawc_y1 = ", self.datawc_y1
        print "datawc_x2 = ", self.datawc_x2
        print "datawc_y2 = ", self.datawc_y2
        print "datawc_timeunits = ", self.datawc_timeunits
        print "datawc_calendar = ", self.datawc_calendar
        print "xaxisconvert = ", self.xaxisconvert
        print "yaxisconvert = ", self.yaxisconvert
        print "fillareastyle = ", self.fillareastyle
        print "fillareaindex = ", self.fillareaindex
        print "fillareacolor = ", self.fillareacolor
        print "outfill = ", self.outfill
    list.__doc__ = xmldocs.listdoc

    #############################################################################
    #                                                                           #
    # Script out primary outfill graphics method in VCS to a file.              #
    #                                                                           #
    #############################################################################
    def script(self, script_filename, mode='a'):
        """
%s
 Function:     script                           # Calls _vcs.scriptGfo

 Description of Function:
       Saves out a outfill graphics method in Python or VCS script form to a
       designated file.

 Example of Use:
    script(scriptfile_name)
              where: scriptfile_name is the output name of the script file.
                     mode is either "w" for replace or "a" for append.

              Note: If the the filename has a ".py" at the end, it will produce a
                    Python script. If the filename has a ".scr" at the end, it will
                    produce a VCS script. If neither extensions are give, then by
                    default a Python script will be produced.

    a=vcs.init()
    out=a.createoutfill('temp')
    out.script('filename.py')         # Append to a Python file "filename.py"
    out.script('filename.scr')        # Append to a VCS file "filename.scr"
    out.script('filename','w')
"""
        if (script_filename == None):
          raise ValueError, 'Error - Must provide an output script file name.'

        if (mode == None):
           mode = 'a'
        elif (mode not in ('w', 'a')):
          raise ValueError, 'Error - Mode can only be "w" for replace or "a" for append.'

        # By default, save file in python script mode
        scr_type = script_filename[len(script_filename)-4:len(script_filename)]
        if (scr_type == '.scr'):
           print _vcs.scriptGfo(self.name,script_filename,mode)
        else:
           mode = mode + '+'
           py_type = script_filename[len(script_filename)-3:len(script_filename)]
           if (py_type != '.py'):
              script_filename = script_filename + '.py'

           # Write to file
           fp = open(script_filename,mode)
           if (fp.tell() == 0): # Must be a new file, so include below
              fp.write("#####################################\n")
              fp.write("#                                 #\n")
              fp.write("# Import and Initialize VCS     #\n")
              fp.write("#                             #\n")
              fp.write("#############################\n")
              fp.write("import vcs\n")
              fp.write("v=vcs.init()\n\n")

           unique_name = '__Gfo__' + self.name
           fp.write("#----------Outfill (Gfo) member (attribute) listings ----------\n")
           fp.write("gfo_list=v.listelements('outfill')\n")
           fp.write("if ('%s' in gfo_list):\n" % self.name)
           fp.write("   %s = v.getoutfill('%s')\n" % (unique_name, self.name))
           fp.write("else:\n")
           fp.write("   %s = v.createoutfill('%s')\n" % (unique_name, self.name))
           # Common core graphics method attributes
           fp.write("%s.projection = '%s'\n" % (unique_name, self.projection))
           fp.write("%s.xticlabels1 = '%s'\n" % (unique_name, self.xticlabels1))
           fp.write("%s.xticlabels2 = '%s'\n" % (unique_name, self.xticlabels2))
           fp.write("%s.xmtics1 = '%s'\n" % (unique_name, self.xmtics1))
           fp.write("%s.xmtics2 = '%s'\n" % (unique_name, self.xmtics2))
           fp.write("%s.yticlabels1 = '%s'\n" % (unique_name, self.yticlabels1))
           fp.write("%s.yticlabels2 = '%s'\n" % (unique_name, self.yticlabels2))
           fp.write("%s.ymtics1 = '%s'\n" % (unique_name, self.ymtics1))
           fp.write("%s.ymtics2 = '%s'\n" % (unique_name, self.ymtics2))
           if isinstance(self.datawc_x1,(int,long,float)):
                fp.write("%s.datawc_x1 = %g\n" % (unique_name, self.datawc_x1))
           else:
                fp.write("%s.datawc_x1 = '%s'\n" % (unique_name, self.datawc_x1))
           if isinstance(self.datawc_y1,(int,long,float)):
                fp.write("%s.datawc_y1 = %g\n" % (unique_name, self.datawc_y1))
           else:
                fp.write("%s.datawc_y1 = '%s'\n" % (unique_name, self.datawc_y1))
           if isinstance(self.datawc_x2,(int,long,float)):
                fp.write("%s.datawc_x2 = %g\n" % (unique_name, self.datawc_x2))
           else:
                fp.write("%s.datawc_x2 = '%s'\n" % (unique_name, self.datawc_x2))
           if isinstance(self.datawc_y2,(int,long,float)):
                fp.write("%s.datawc_y2 = %g\n" % (unique_name, self.datawc_y2))
           else:
                fp.write("%s.datawc_y2 = '%s'\n" % (unique_name, self.datawc_y2))
           fp.write("%s.datawc_calendar = %g\n" % (unique_name, self.datawc_calendar))
           fp.write("%s.datawc_timeunits = '%s'\n\n" % (unique_name, self.datawc_timeunits))
           fp.write("%s.xaxisconvert = '%s'\n" % (unique_name, self.xaxisconvert))
           fp.write("%s.yaxisconvert = '%s'\n" % (unique_name, self.yaxisconvert))
           # Unique attribute for outfill
           fp.write("%s.fillareastyle = '%s'\n" % (unique_name, self.fillareastyle))
           fp.write("%s.fillareaindex = %s\n" % (unique_name, self.fillareaindex))
           fp.write("%s.fillareacolor = %s\n" % (unique_name, self.fillareacolor))
           fp.write("%s.outfill = %s\n\n" % (unique_name, self.outfill))
    script.__doc__ = script.__doc__ % xmldocs.scriptdoc


#################################################################################
#        END OF FILE								#
#################################################################################
