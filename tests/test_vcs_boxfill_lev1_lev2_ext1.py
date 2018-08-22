import basevcstest


class TestVCSBoxfill(basevcstest.VCSBaseTest):
    def testBoxfillLev1Lev2Ext1(self):
        s = self.clt("clt", slice(0, 1), squeeze=1)
        b = self.x.createboxfill()
        b.level_1 = 20
        b.level_2 = 80
        b.ext_1 = "y"
        self.x.plot(s, b, bg=self.bg)
        self.checkImage("test_vcs_boxfill_lev1_lev2_ext1.png")
