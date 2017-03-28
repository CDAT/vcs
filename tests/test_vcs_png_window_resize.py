import basevcstest
import vcs

class TestVCSPNG(basevcstest.VCSBaseTest):
    def __init__(self,*args,**kargs):
        kargs['bg']=0
        super(TestVCSPNG,self).__init__(*args,**kargs)

    def testPngResizeWindow(self, *args, **kwargs):
        self.x.open(814,628)
        self.x.plot([1,2,3,4,5,6,7])
        fnm = __file__[:-3]+".png"
        self.x.png(fnm)
        self.checkImage(fnm,pngReady=True)
