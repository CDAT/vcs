
import basevcstest
import numpy
import MV2


class TestVCSFonts(basevcstest.VCSBaseTest):
    def test_set_default_font(self):
        txt = self.x.createtext()
        txt.string = "MY DEFAULT FONT"
        txt.x = .3
        txt.y = .5
        txt.height = 15
        txt.halign = "center"
        self.x.plot(txt)
        self.x.setdefaultfont("Times")
        txt = self.x.createtext()
        txt.string = "MY NEW DEFAULT FONT"
        txt.x = .7
        txt.y = .5
        txt.height = 15
        txt.halign = "center"
        self.x.plot(txt)
        fnm = "test_vcs_defaultfont.png"
        self.checkImage(fnm)


