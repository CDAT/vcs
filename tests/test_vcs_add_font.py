
import basevcstest
import numpy
import MV2


class TestVCSAddFont(basevcstest.VCSBaseTest):
    def test_add_font(self):
        nFonts = len(self.x.listelements("font"))
        name = self.x.addfont("docs/Jupyter/FFF_Tusj.ttf")
        # Make sure we added a font
        nFontsAdded = len(self.x.listelements("font")) - nFonts
        self.assertEqual(nFontsAdded, 1)
        self.assertEqual(name, "FFF_Tusj")
        txt = self.x.createtext()
        txt.string = "MY TEST FONT"
        txt.x = .4
        txt.y = .5
        txt.height = 15
        txt.halign = "center"
        self.x.plot(txt)
        txt.font = name
        txt.x = .6
        self.x.plot(txt)
        fnm = "test_vcs_add_font.png"
        self.checkImage(fnm)


