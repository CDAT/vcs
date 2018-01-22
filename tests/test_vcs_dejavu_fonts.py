import basevcstest


class TestVCSTextsExtents(basevcstest.VCSBaseTest):
    def testDejaVuFonts(self):

        self.x.switchfonts("default", "DejaVuSans")
        assert(self.x.getfontname(1) == "DejaVuSans")
