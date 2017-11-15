import basevcstest
import vcs


class TestVCSBadExt2Setting(basevcstest.VCSBaseTest):
    def testBadExt2Setting(self):
        iso = self.x.createisofill()
        iso.levels = [[1.e20, 1.e20]]
        iso.ext_2 = "n"

        assert(iso.levels == [[1.e20, 1.e20]])
