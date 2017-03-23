import basevcstest

class TestVCSFileVariable(basevcstest.VCSBaseTest):
    def testPlotFileVariable(self):
        V = self.clt["clt"]
        self.x.plot(V, bg=self.bg)
