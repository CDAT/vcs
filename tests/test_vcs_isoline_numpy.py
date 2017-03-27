import basevcstest

class TestVCSIsolines(basevcstest.VCSBaseTest):
    def testIsolineNumpy(self):
        s = self.clt("clt")
        gm = self.x.createisofill()
        self.x.plot(s.filled(),gm,bg=self.bg)
        fnm = "test_vcs_isoline_numpy.png"
        self.checkImage(fnm)
