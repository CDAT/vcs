import sys
# Adapted for numpy/ma/cdms2 by convertcdms.py
#
# Test Yxvsx (GYx) module
#
############################################################################
#                                                                          #
# Module:       testyxvsx module                                           #
#                                                                          #
# Copyright:    2000, Regents of the University of California              #
#               This software may not be distributed to others without     #
#               permission of the author.                                  #
#                                                                          #
# Authors:      PCMDI Software Team                                        #
#               Lawrence Livermore NationalLaboratory:                     #
#               support@pcmdi.llnl.gov                                     #
#                                                                          #
# Description:  Used to test VCS's Yxvsx graphics method.                  #
#                                                                          #
# Version:      4.0                                                        #
#                                                                          #
############################################################################
#
#
#
############################################################################
#                                                                          #
# Import: VCS and cdms modules.                                            #
#                                                                          #
############################################################################


def test():
    import vcs
    import cdms2 as cdms
    import os
    import support          # import vcs and cdms

    bg = support.bg

    f = cdms.open(os.path.join(vcs.sample_data, 'clt.nc'))  # open clt file
    u = f('u')  			        # get slab u
    x = vcs.init()                         # construct vcs canvas

    x.plot(u, 'default', 'yxvsx', 'ASD7', bg=bg)  # plot slab the old way
    support.check_plot(x)
    if support.dogui:
        x.geometry(450, 337, 100, 0)		# change the geometry and location
        x.flush()
        support.check_plot(x)

    a = x.getyxvsx('ASD7')		    	# get 'ASD7' yxvsx
    # test object 'a' for graphics method
    if not vcs.isgraphicsmethod(a):
        raise Exception("Error not a gm")
    else:
        if not vcs.isyxvsx(a):                  # test object 'a' if yxvsx
            raise Exception("Error wrong type of gm")

    # save 'ASD7' yxvsx as a Python script
    a.script('test', 'w')

    a.xticlabels('', '')                  # remove the x-axis
    support.check_plot(x)
    a.xticlabels('*')                    # put the x-axis
    support.check_plot(x)

    ##########################################################################
    # Change the yxvsx line                                                    #
    ##########################################################################
    a.line = 0        			# same as 'solid'
    support.check_plot(x)
    a.line = 1        			# same as 'dash'
    support.check_plot(x)
    a.line = 2        			# same as 'dot'
    support.check_plot(x)
    a.line = 3        			# same as 'dash-dot'
    support.check_plot(x)
    a.line = 4        			# same as 'long-dash'
    support.check_plot(x)

    if '--extended' not in sys.argv:
        print '\n************* PARTIAL TEST *****************'
        print 'FOR COMPLETE TEST OF THIS MODULE USE '
        print '   -F (--full) or -E (--extended) option'
        print '************* PARTIAL TEST *****************\n'
        sys.exit()

    ##########################################################################
    # Change the yxvsx line color                                              #
    ##########################################################################
    a.linecolor = (77)
    support.check_plot(x)
    a.linecolor = 16
    support.check_plot(x)
    a.linecolor = 44  			# same as a.color=(44)
    support.check_plot(x)
    a.linecolor = None
    support.check_plot(x)

    ##########################################################################
    # Change the yxvsx marker                                                  #
    ##########################################################################
    a.marker = 1                        	# Same as a.marker='dot'
    support.check_plot(x)
    a.marker = 2                       	# Same as a.marker='plus'
    support.check_plot(x)
    a.marker = 3                       	# Same as a.marker='star'
    support.check_plot(x)
    a.marker = 4                       	# Same as a.marker='circle'
    support.check_plot(x)
    a.marker = 5                        	# Same as a.marker='cross'
    support.check_plot(x)
    a.marker = 6                        	# Same as a.marker='diamond'
    support.check_plot(x)
    a.marker = 7                        	# Same as a.marker='triangle_up'
    support.check_plot(x)
    a.marker = 8                        	# Same as a.marker='triangle_down'
    support.check_plot(x)
    a.marker = 9                        	# Same as a.marker='triangle_left'
    support.check_plot(x)
    a.marker = 10                       	# Same as a.marker='triangle_right'
    support.check_plot(x)
    a.marker = 11                       	# Same as a.marker='square'
    support.check_plot(x)
    a.marker = 12                       	# Same as a.marker='diamond_fill'
    support.check_plot(x)
    a.marker = 13                       	# Same as a.marker='triangle_up_fill'
    support.check_plot(x)
    # Same as a.marker='triangle_down_fill'
    a.marker = 14
    support.check_plot(x)
    # Same as a.marker='triangle_left_fill'
    a.marker = 15
    support.check_plot(x)
    # Same as a.marker='triangle_right_fill'
    a.marker = 16
    support.check_plot(x)
    a.marker = 17                       	# Same as a.marker='square_fill'
    support.check_plot(x)
    a.marker = None                     	# Draw no markers
    support.check_plot(x)

    ##########################################################################
    # Change the yxvsx marker color                                            #
    ##########################################################################
    a.marker = 'dot'
    support.check_plot(x)
    a.markercolor = 16
    support.check_plot(x)
    a.markercolor = 44        		# same as a.markercolor=(44)
    support.check_plot(x)
    a.markercolor = None
    support.check_plot(x)

    ##########################################################################
    # Change the yxvsx marker size                                             #
    ##########################################################################
    a.markersize = 5
    support.check_plot(x)
    a.markersize = 55
    support.check_plot(x)
    a.markersize = 10
    support.check_plot(x)
    a.markersize = 100
    support.check_plot(x)
    a.markersize = 300
    support.check_plot(x)
    a.markersize = None
    support.check_plot(x)

    x.clear()                            # clear the VCS Canvas
    x.yxvsx(u, a, 'default', bg=bg)		# plot yxvsx using 'default' template
    support.check_plot(x)

    # show the list of templates
    # create template 'test' from 'default' template
    t = x.createtemplate('test')
    # test whether 't' is a template or not
    if not vcs.istemplate(t):
        raise Exception("Error creating tmeplate")

    x.clear()                            # clear the VCS Canvas
    # plot yxvsx template 't', outline 'a', and arrays 'u':'v'
    x.plot(t, a, u, bg=bg)
    support.check_plot(x)
    x.clear()                            # clear the VCS Canvas
    # plot using outline 'a', array 'u':'v', and template 't'
    x.yxvsx(a, u, t, bg=bg)
    support.check_plot(x)

    # show the list of line secondary objects
    l = x.getline('red')                	# get line 'red'
    # check to see if it is a secondary object
    if not vcs.issecondaryobject(l):
        raise Exception("Error did not get line")
    else:
        if not vcs.isline(l):                  	# check to see if it is a line
            raise Exception("Error object created is not line")

    ###########################################################################
    # Use the create line object 'm' from above and modify the line object    #
    ###########################################################################
    a.line = l                             # use the line object
    support.check_plot(x)
    l.color = 44                         # change the line color
    support.check_plot(x)
    l.type = 'dot'                       # change the line type
    support.check_plot(x)
    l.width = 4 				# change the line size
    support.check_plot(x)

    # show the list of marker secondary objects
    m = x.getmarker('red')                 # get marker 'red'
    # check to see if it is a secondary object
    if not vcs.issecondaryobject(m):
        raise Exception("Error did not get marker")
    else:
        # check to see if it is a line
        if not vcs.ismarker(m):
            raise Exception("Error object created is not marker")

    ###########################################################################
    # Use the create marker object 'm' from above and modify the line object  #
    ###########################################################################
    a.marker = m                           # use the marker object
    support.check_plot(x)
    m.color = 44                         # change the marker color
    support.check_plot(x)
    m.type = 'square'                     # change the marker type
    support.check_plot(x)
    m.size = 20                            # change the marker size
    support.check_plot(x)

    a = x.listelements('yxvsx')                      # show list of xyvsy
    r = x.createyxvsx('test2', 'ASD1')     # create xyvsy 'test2'
    a2 = x.listelements('yxvsx')                      # show list of xyvsy
    if a2 == a:
        raise "error gm not created or not added to list"
    x.removeobject(r)                    # remove xyvsy 'test2'
    a3 = x.listelements('yxvsx')                      # show list of xyvsy
    if a3 != a:
        raise "error gm not removed"

    ##########################################################################
    # to see how x.update and x.mode work, see testoutline.py                       #
    ##########################################################################
    # x.update()
    # x.mode=1
    # x.mode=0
    print '*************************************************************************************'
    print '******                                                                         ******'
    print '******   Y x v s x   T E S T   C O M P L E T E D   S U C E S S F U L L Y       ******'
    print '******                                                                         ******'
    print '*************************************************************************************'

if __name__ == "__main__":
    test()
