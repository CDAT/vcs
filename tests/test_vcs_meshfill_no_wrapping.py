import basevcstest
import numpy

class TestVCSMeshfill(basevcstest.VCSBaseTest):
    def testVCSMeshfillNoWrap(self):

        f = cdms2.open()
        h = f("heat")
        self.x.plot(h, bg=self.bg)
        self.checkImage("test_vcs_meshfill_no_wrapping.png")
