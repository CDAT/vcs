import basevcstest
import cdms2
import vcs
import os

class TestVCSAnimateBoxfill(basevcstest.VCSBaseTest):
    def testVCSAnimateBoxfill(self):
        f=cdms2.open(os.path.join(vcs.sample_data,"clt.nc"))
        s=f("clt",slice(0,12)) # read only 12 times steps to speed up things

        gm=self.x.createboxfill()
        self.x.plot(s,gm,bg=1)
        self.x.animate.create()
        prefix= os.path.split(__file__)[1][:-3]
        print "PREFIX MMP4:",prefix
        self.x.animate.save("%s.mp4"%prefix)
        pngs = self.x.animate.close(preserve_pngs = True) # so we can look at them again
        ret = 0
        for p in pngs:
            print "CHECKINGGG>>>>"
            ret += self.checkImage(p,os.path.join(self.basedir,'test_vcs_animate_boxfill',os.path.basename(p)))
        if ret == 0:
            os.removedirs(os.path.split(p)[0])
            os.remove("%s.mp4" % prefix)
