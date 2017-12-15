import basevcstest
import cdms2
import vcs
import os


class TestVCSAnimateIsofill(basevcstest.VCSBaseTest):
    def testVCSAnimateIsofill(self):
        f = cdms2.open(os.path.join(vcs.sample_data, "clt.nc"))
        # read only 12 times steps to speed up things
        s = f("clt", slice(0, 12))

        gm = self.x.createisofill()
        self.x.plot(s, gm, bg=self.bg)
        self.x.animate.create()
        prefix = os.path.splitext(os.path.split(__file__)[1])[0]
        self.x.animate.save("%s.mp4" % prefix)
        # so we can look at them again
        pngs = self.x.animate.close(preserve_pngs=True)
        ret = 0
        for p in pngs:
            print("Checking:", p)
            ret += self.checkImage(p,
                                   os.path.join(self.basedir,
                                                'test_vcs_animate_isofill',
                                                os.path.basename(p)),
                                   pngReady=True)
        if ret == 0:
            os.removedirs(os.path.split(p)[0])
            os.remove("%s.mp4" % prefix)
