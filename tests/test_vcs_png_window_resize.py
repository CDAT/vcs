import basevcstest
import vcs
import os

class TestVCSPNG(basevcstest.VCSBaseTest):
    def __init__(self,*args,**kargs):
        kargs['bg']=0
        kargs['geometry'] = {"width": 1200, "height": 790}
        super(TestVCSPNG,self).__init__(*args,**kargs)

    def testPngResizeWindow(self, *args, **kwargs):
        self.x.open(814,628)
        self.x.plot([1,2,3,4,5,6,7])
        fnm = os.path.splitext(__file__)[0] + ".png"
        self.x.png(fnm)
        self.checkImage(fnm,pngReady=True)
