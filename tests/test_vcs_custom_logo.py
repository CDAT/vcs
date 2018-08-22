import basevcstest
import vcs
import os
import sys


class TestVCSLogo(basevcstest.VCSBaseTest):
    def __init__(self, *args, **kargs):
        kargs["geometry"] = {"width": 814, "height": 606}
        super(TestVCSLogo, self).__init__(*args, **kargs)

    def testCustomLogo(self):

        self.x.drawlogoon()
        logo1 = vcs.utils.Logo("My Test Logo")
        logo1.x = .2
        logo1.y = .2
        logo1.plot(self.x, bg=self.bg)

        png_pth = os.path.join("tests", "share", "uvcdat.png")
        print("PNG:", png_pth)
        logo2 = vcs.utils.Logo(png_pth)
        logo2.x = .7
        logo2.y = .8
        logo2.plot(self.x, bg=self.bg)

        fnm = "test_vcs_custom_logo.png"
        self.checkImage(fnm)
