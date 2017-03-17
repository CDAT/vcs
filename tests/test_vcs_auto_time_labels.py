import basevcstest

class TestVCSAutot(basevcstest.VCSBaseTest):
    def testAutotimelevel(self):
        s = self.clt("clt",longitude=slice(34,35),squeeze=1)
        self.x.plot(s,bg=self.bg)
        self.checkImage("test_vcs_auto_time_labels.png")
