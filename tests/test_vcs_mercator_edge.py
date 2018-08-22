import basevcstest


class TestVCSMercator(basevcstest.VCSBaseTest):
    def testVCSMercator(self):
        s = self.clt("clt")
        iso = self.x.createisofill()
        iso.projection = "mercator"
        self.x.plot(s(latitude=(-90, 90)), iso, bg=self.bg)
        self.checkImage("test_vcs_mercator_edge.png")
