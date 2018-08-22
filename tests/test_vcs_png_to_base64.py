import vcs
import basevcstest


class TestVCSPNG64(basevcstest.VCSBaseTest):
    def testPng2Base64(self):
        m = self.x.createmarker()

        m.type = "star"
        m.x = [.1]
        m.y = [.1]
        m.color = 200
        m.size = 50
        display = self.x.plot(m, bg=self.bg)

        display._repr_png_()
