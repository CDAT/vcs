"""
# VCS Visualization and Control System - (VCS) module
#
#################################################################################
#                                                                               #
# Module:       vcs module                                                      #
#                                                                               #
# Authors:      PCMDI Software Team                                             #
#               support@pcmdi.llnl.gov                                          #
#               http://cdat.sf.net/cdat                                         # 
#                                                                               #
# Description:  Python command wrapper for VCS's functionality. VCS is computer #
#               software for the selection, manipulation, and display of        #
#               scientific data. By specification of the desired data, the      #
#               graphics method, and the display template, the VCS user gains   #
#               virtually complete control of the appearance of the data        #
#               display and associated text and animation.                      #
#                                                                               #
# Upgrade to VTK:                                                               #
# Author: Charles Doutriaux                                                     #
# Description: Took out all C code and used VTK's python bindings instead       #
#                                                                               #
#################################################################################
"""
import cdat_info
cdat_info.pingPCMDIdb("cdat","vcs")
import thread
import time
import Canvas
from vcshelp import *
from queries import *
from pauser import pause
from utils import *
import install_vcs
from install_vcs import list_printers, add_printer, remove_printer
from Canvas import dictionarytovcslist

_default_time_units='days since 2000'

#from _vcs import polygons
#from vcs import Meshes

#################################################################################
#                                                                               #
# Set up the User's  directory if necessary. Copy files from      #
# $PYTHONHOME/bin to the newly created $HOME/.uvcdat directory.          #
#                                                                               #
#################################################################################
install_vcs._files()

#################################################################################
#                                                                               #
# Set the user's XGKSFontDir environment variable.                              #
#                                                                               #
#################################################################################
install_vcs._XGKSFontDir()

#################################################################################
#                                                                               #
# Construct a VCS Canvas Object.                                                #
#                                                                               #
#################################################################################

# Initialize the list of taylor diagrams objects

def init(gui = 0, mode=1, pause_time=0, call_from_gui=0, size=None):
    '''
 Function: init                 # Initialize, Construct a VCS Canvas Object

 Description of Function:
    Construct the VCS Canas object. There can only be at most 8 VCS
    Canvases open at any given time.

    Graphics User Interface Mode:                                         
            gui = 0|1    if ==1, create the canvas with GUI controls       
                         (Default setting is *not* to display GUI controls)

 Example of Use:
    import vcs,cu

    file=cu.open('filename.nc')
    slab=file.getslab('variable')
    a=vcs.init()                        # This examples constructs 4 VCS Canvas 
    a.plot(slab)                        # Plot slab using default settings
    b=vcs.init()                        # Construct VCS object
    template=b.gettemplate('AMIP')      # Get 'example' template object
    b.plot(slab,template)               # Plot slab using template 'AMIP'
    c=vcs.init()                        # Construct new VCS object
    isofill=c.getisofill('quick')       # Get 'quick' isofill graphics method
    c.plot(slab,template,isofill)       # Plot slab using template and isofill objects
    d=vcs.init()                        # Construct new VCS object
    isoline=c.getisoline('quick')       # Get 'quick' isoline graphics method
    c.plot(isoline,slab,template)       # Plot slab using isoline and template objects
'''
    initQt()
    canvas = Canvas.Canvas(gui=gui, mode=mode, pause_time=pause_time, call_from_gui=call_from_gui, size=size)
    global canvaslist
    canvaslist.append(canvas)
    return canvas
    
def initQt():
    #_vcs.startQtApp()
    return

elements = { "boxfill" : {},
             "isofill" : {},
             "isoline" : {},
             "meshfill" : {},
             "outfill": {},
             "outline" : {},
             "template" : {},
             "taylordiagram" :{},
             "oneD":{},
             "vector":{},
             "yxvsx":{},
             "xyvsy":{},
             "xvsy" :{},
             "scatter" :{},
             "list": {},
             "projection": {},
             "fillarea":{},
             "texttable":{},
             "textorientation":{},
             "line":{},
             }
p=projection.Proj("default")
p = projection.Proj("linear")
line.Tl("default")
line.Tl("deftaylordot")
line.type=["dot"]
texttable.Tt("default")
textorientation.To("default")
to = textorientation.To("defcenter")
to.halign = "center"
to = textorientation.To("defright")
to.path = "right"
warnings.warn("Please edit line for vcs.elements")
boxfill.Gfb("default")
isofill.Gfi("default")
isoline.Gi("default")
unified1D.G1d("default")
yx = unified1D.G1d("default_yxvsx")
vcs.elements["yxvsx"]["default"]=yx
xy = unified1D.G1d("default_xyvsy")
xy.flip = True
vcs.elements["xyvsy"]["default"]=xy
sc = unified1D.G1d("default_scatter")
vcs.elements["scatter"]["default"]=sc
xvy = unified1D.G1d("default_xvsy")
vcs.elements["xvsy"]["default"]=xvy



for nm in ["mercator","orthographic","lambert","polar","polyconic","robinson",
    "mollweide",]:
  p = projection.Proj(nm)
  p.type=nm

fillarea.Tf("default")
template.P("default")

taylordiagrams=[taylor.Gtd()]

canvaslist = []
#meshfills=[meshfill.Gfm()]
