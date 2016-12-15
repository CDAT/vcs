#####################################
#                                 #
# Import and Initialize VCS     #
#                             #
#############################
import vcs
v=vcs.init()

#----------Boxfill (Gfb) member (attribute) listings ----------
gfb_list=v.listelements('boxfill')
if ('default' in gfb_list):
   __Gfb__default = v.getboxfill('default')
else:
   __Gfb__default = v.createboxfill('default')
__Gfb__default.projection = 'linear'
__Gfb__default.xticlabels1 = '*'
__Gfb__default.xticlabels2 = '*'
__Gfb__default.xmtics1 = ''
__Gfb__default.xmtics2 = ''
__Gfb__default.yticlabels1 = '*'
__Gfb__default.yticlabels2 = '*'
__Gfb__default.ymtics1 = ''
__Gfb__default.ymtics2 = ''
__Gfb__default.datawc_x1 = 1e+20
__Gfb__default.datawc_y1 = 1e+20
__Gfb__default.datawc_x2 = 1e+20
__Gfb__default.datawc_y2 = 1e+20
__Gfb__default.xaxisconvert = 'linear'
__Gfb__default.yaxisconvert = 'linear'
__Gfb__default.boxfill_type = 'linear'
__Gfb__default.level_1 = 1e+20
__Gfb__default.level_2 = 1e+20
__Gfb__default.levels = [1e+20, 1e+20]
__Gfb__default.color_1 = 0
__Gfb__default.color_2 = 255
__Gfb__default.fillareacolors = None
__Gfb__default.fillareastyle = 'solid'
__Gfb__default.fillareaindices = [1]
__Gfb__default.fillareaopacity = []
__Gfb__default.legend = None
__Gfb__default.ext_1 = 'False'
__Gfb__default.ext_2 = 'False'
__Gfb__default.missing = (0.0, 0.0, 0.0, 100.0)
__Gfb__default.datawc_calendar = 135441
__Gfb__default.datawc_timeunits = 'days since 2000'

__Gfb__default.colormap = 'None'

