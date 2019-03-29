import basevcstest
import vcs

class VCSTestTextTransparency(basevcstest.VCSBaseTest):
    def testTransparentText(self):
        fa = self.x.createfillarea()
        fa.x = [.4,.6,.6,.4]
        fa.y = [.4,.4,.6,.6]
        fa.color="red"

        self.x.plot(fa)

        txt = self.x.createtext()
        txt.string = "TRANSPARENT STRING"
        txt.angle = -45
        txt.x = .5
        txt.y = .5
        txt.halign="center"
        txt.valign = "half"
        txt.color = [0, 0, 100, 30]
        txt.height = 35
        self.x.plot(txt)

        self.checkImage("test_vcs_text_transparency.png")
