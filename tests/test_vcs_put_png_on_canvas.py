import os
import vcs
import basevcstest

class TestVCSPNG(basevcstest.VCSBaseTest):
    def __init__(self, *args, **kwargs):
        kwargs['geometry'] = {"width": 1200, "height": 800}
        self.png = os.path.join(vcs.sample_data,"BlueMarble.ppm")
        super(TestVCSPNG, self).__init__(*args, **kwargs)

    def putPNGOnCanvas(self,fitToHeight=True,units="percent",xoffset=0.,yoffset=0.,zoom=1.):
        self.x.clear()
        self.x.put_png_on_canvas(self.png,zoom,xoffset,yoffset,units,fitToHeight)
        fnm = "test_vcs_put_png_on_canvas_%s_%s_%s_%s_%s.png" % (zoom,xoffset,yoffset,units,fitToHeight)
        self.checkImage(fnm,threshold=20.)

    def testPutPng(self):
        self.x.open()
        self.putPNGOnCanvas()
        self.putPNGOnCanvas(units="pixels",fitToHeight=False)
        for zoom in [.5, 1.5]:
            for xoff in [-25,25]:
                for yoff in [25.,-25.]:
                    self.putPNGOnCanvas(zoom=zoom,xoffset=xoff,yoffset=yoff)
            for xoff in [-250.,250.]:
                for yoff in [250.,-250.]:
                    self.putPNGOnCanvas(zoom=zoom,xoffset=xoff,yoffset=yoff)

