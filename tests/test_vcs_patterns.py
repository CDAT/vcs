import basevcstest
import vcs


class TestVCSPatterns(basevcstest.VCSBaseTest):
    def testPatterns(self):
        s = self.clt("clt", time=slice(0, 1), squeeze=1)
        iso = self.x.createisofill("isoleg")
        iso.levels = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
        iso.fillareastyle = "pattern"
        iso.fillareacolors = vcs.getcolors(
            [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100])
        iso.fillareaindices = [1, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20]
        self.x.plot(s, iso, bg=self.bg)
        fnm = "test_vcs_patterns.png"
        self.checkImage(fnm)
