import basevcstest


class TestVCSLabels(basevcstest.VCSBaseTest):
    def testLabelIssue960(self):
        s = self.clt("clt", time=slice(0, 1), latitude=(-7, 5), squeeze=1)
        self.x.plot(s, bg=self.bg)
        fnm = "test_vcs_issue_960_labels_1.png"
        self.checkImage(fnm)
        b = self.x.createboxfill()
        b.datawc_y1 = -7
        b.datawc_y2 = 5
        self.x.plot(s, b, bg=self.bg)
        fnm = "test_vcs_issue_960_labels_2.png"
        self.checkImage(fnm)
