import basevcstest


class TestVCSBoxfill(basevcstest.VCSBaseTest):
    def testBoxfillLev1Lev2(self):
        s = self.clt("clt", slice(0, 1), squeeze=1)
        b = self.x.createboxfill()
        b.level_1 = .5
        b.level_2 = 14.5
        self.x.plot(s, b, bg=self.bg)
        self.checkImage("test_vcs_boxfill_lev1_lev2.png")
