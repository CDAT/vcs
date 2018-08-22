import basevcstest
import cdms2
import vcs
import os


class TestVCSMeshfill(basevcstest.VCSBaseTest):
    def testVCSMeshfillDrawMesh(self):
        fnmcurv = os.path.join(vcs.sample_data, 'sampleCurveGrid4.nc')
        f = cdms2.open(fnmcurv)
        s = f("sample")
        m = self.x.createmeshfill()
        m.mesh = True

        self.x.plot(s, m, bg=self.bg)
        self.checkImage("test_vcs_meshfill_draw_mesh.png")
