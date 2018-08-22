import basevcstest


class TestVCSIsolines(basevcstest.VCSBaseTest):
    def testIsolineExtendAttributes(self):
        isoline = self.x.createisoline()
        s = self.clt("clt")
        isoline.linetypes = ["dash-dot"]
        isoline.linecolors = [250]
        isoline.linewidths = [5]
        self.x.plot(s, isoline, bg=self.bg)
        fnm = "test_vcs_isoline_extend_attributes.png"
        self.checkImage(fnm)
