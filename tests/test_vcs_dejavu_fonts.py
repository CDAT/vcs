import basevcstest


class TestVCSTextsExtents(basevcstest.VCSBaseTest):
    def testDejaVuFonts(self):

        assert(self.x.getfont("DejaVuSans") == 21)
