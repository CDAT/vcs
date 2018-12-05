import basevcstest
import cdms2
import vcs
import MV2


class TestVCSVectorsMissing(basevcstest.VCSBaseTest):
    def testVCSVectorMissing(self):
        u = self.clt['u']
        v = self.clt['v']

        gm = self.x.createvector()
        gm.datawc_x1 = -180
        gm.datawc_x2 = 360
        gm.scale = 8

        self.x.plot(gm, u[::5, ::5], v[::5, ::5])
        fnm = "test_vcs_vectors_warp.png"
        self.checkImage(fnm)
