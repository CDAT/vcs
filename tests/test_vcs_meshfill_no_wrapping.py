import basevcstest
import cdms2
import os


class TestVCSMeshfill(basevcstest.VCSBaseTest):
    def testVCSMeshfillNoWrap(self):

        f = cdms2.open(os.path.join(self.basedatadir, "heat.nc"))
        h = f("heat")
        self.x.plot(h, bg=self.bg)
        self.checkImage("test_vcs_meshfill_no_wrapping.png")
