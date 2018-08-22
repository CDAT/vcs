import basevcstest


class TestVCSPatterns(basevcstest.VCSBaseTest):
    def testLargePatterns(self):
        fillarea = self.x.createfillarea()
        fillarea.x = [[0, .33, .33, 0], [.33, .67, .67, .33], [.67, 1, 1, .67]]
        fillarea.y = [[0, 0, 1, 1]] * 3
        fillarea.style = ["solid", "pattern", "hatch"]
        fillarea.index = [1, 5, 5]
        fillarea.color = [50, 50, 50]
        self.x.plot(fillarea, bg=self.bg)
        fnm = "test_vcs_large_pattern_hatch.png"
        self.checkImage(fnm)
