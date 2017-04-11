import basevcstest
import vcs
import os

class TestVCSAnimateIsoline(basevcstest.VCSBaseTest):
    def testVCSAnimateIsoline(self):
        s=self.clt("clt",slice(0,12)) # read only 12 times steps to speed up things
        gm=self.x.createisoline()
        self.x.plot(s,gm,bg=self.bg)
        self.x.animate.create()
        prefix= os.path.splitext(os.path.split(__file__)[1])[0]
        self.x.animate.save("%s.mp4"%prefix)
        pngs = self.x.animate.close(preserve_pngs = True) # so we can look at them again
        ret = 0
        for p in pngs:
            ret += self.checkImage(p,os.path.join(self.basedir,'test_vcs_animate_isoline',os.path.basename(p)),pngReady=True)
        if ret == 0:
            os.removedirs(os.path.split(p)[0])
            os.remove("%s.mp4" % prefix)
