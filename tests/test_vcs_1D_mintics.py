import basevcstest
import numpy
import MV2


class TestVCSMinTics(basevcstest.VCSBaseTest):
    def testMintics(self):
        angle = numpy.arange(0, 360, 10) # in degrees
        s = numpy.sin(angle/180.*numpy.pi) # sin takes radians as input
        line = self.x.create1d()
        line.linecolor = "red"  # Red color obviously
        line.linewidth = 2.  # A bit thicker
        line.marker = "circle"  #
        line.markersize = 1
        s = MV2.array(s)
        s.id = "sine"
        xaxis = s.getAxis(0)
        xaxis.id = "angle"
        xaxis.units="radians"
        # let's make them radians as well
        xaxis[:] = xaxis[:]/18.*numpy.pi
        # That means we need to match or symbols to new values
        angles = {0:'0',numpy.pi/2.:r'$\pi/2$',numpy.pi:r'$\pi$', 3*numpy.pi/2.:r'$3\pi/2$',2*numpy.pi:r'$2\pi$'}
        line.xticlabels1 = angles
        thick = self.x.createline()  # for thick ticks
        thick.width = 1.5  # A bit thicker
        thick.color = ["grey"]
        dots = self.x.createline()  # for thin/sub ticks
        dots.type = ["dot"]
        dots.color = ["blue"]
        tmpl = self.x.createtemplate()
        tmpl.xtic1.y2 = tmpl.data.y2  # Ticks extends all the way accross the data section
        tmpl.xtic1.line = thick
        tmpl.xmintic1.y2 = tmpl.data.y2  # Ticks extends all the way accross the data section
        tmpl.xmintic1.priority = 1
        tmpl.xmintic1.line = dots
        tmpl.ytic1.x2 = tmpl.data.x2  # Ticks extends all the way accross the data section
        tmpl.ytic1.line = thick
        tmpl.ymintic1.x2 = tmpl.data.x2  # Ticks extends all the way accross the data section
        tmpl.ymintic1.priority = 1
        tmpl.ymintic1.line = dots
        line.xmtics1 = {numpy.pi/4.:"",3*numpy.pi/4:"",5*numpy.pi/4:"",7*numpy.pi/4:""}
        line.yticlabels1 = {-1.:"-1",-.5:"-0.5",0:"0",.5:"0.5",1:"1"}
        line.ymtics1 = {-.75:"", -.25:"", .25:"", .75:""}
        tmpl.blank("mean")
        self.x.plot(s,line,tmpl,bg=self.bg)
        self.checkImage("test_vcs_1D_mintics.png")

