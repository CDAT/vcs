import basevcstest

class TestVCSBadTime(basevcstest.VCSBaseTest):
    def testBadTimeunits(self):
        s = self.clt("clt",slice(0,1))
        s.getTime().units="XXX-))rvv"
        self.x.plot(s, bg=self.bg)
