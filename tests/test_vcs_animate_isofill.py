import basevcstest
import cdms2
import vcs
import os

class TestVCSAnimateIsofill(basevcstest.VCSBaseTest):
    def testVCSAnimateIsofill(self):
        f=cdms2.open(os.path.join(vcs.sample_data,"clt.nc"))
        s=f("clt",slice(0,12)) # read only 12 times steps to speed up things

        gm=self.x.createisofill()
        self.x.plot(s,gm,bg=1)
        self.x.animate.create()
        prefix= os.path.split(__file__)[1][:-3]
        self.x.animate.save("%s.mp4"%prefix)
        pngs = self.x.animate.close(preserve_pngs = True) # so we can look at them again
        ret = 0
        for p in pngs:
          print "Checking:",p
          ret += self.checkImage(p,os.path.join(self.basedir,'test_vcs_animate_isofill',os.path.basename(p)),pngReady=True)
        if ret == 0:
            os.removedirs(os.path.split(p)[0])
            os.remove("%s.mp4" % prefix)
