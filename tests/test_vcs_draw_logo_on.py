import basevcstest
import numpy


class TestVCSDrawLogo(basevcstest.VCSBaseTest):
    def __init__(self, *args, **kargs):
        kargs["geometry"] = {"width": 814, "height": 606}
        super(TestVCSDrawLogo, self).__init__(*args, **kargs)

    def testDrawLogoOn(self):
        a = numpy.arange(100)
        a.shape = (10, 10)
        self.x.drawlogoon()
        self.x.plot(a, bg=self.bg)
        fnm = "test_vcs_draw_logo_on.png"
        self.checkImage(fnm)

        self.x.clear()
        self.x.drawlogoon()
        self.x.geometry(800, 400)
        self.x.plot(a, bg=self.bg)
        fnm = "test_vcs_draw_logo_on_wide.png"
        self.checkImage(fnm)

        self.x.clear()
        self.x.drawlogoon()
        self.x.geometry(400, 800)
        self.x.plot(a, bg=self.bg)
        fnm = "test_vcs_draw_logo_on_tall.png"
        self.checkImage(fnm)
