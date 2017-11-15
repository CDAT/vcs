import basevcstest


class TestVCSMeshfill(basevcstest.VCSBaseTest):
    def testVCSMeshfillRegularGrid(self):

        s = self.clt("clt")
        self.x.meshfill(s, bg=self.bg)
        self.checkImage("test_vcs_meshfill_regular_grid.png")
