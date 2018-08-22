import basevcstest
import os
import cdms2


class TestVCSIsofill(basevcstest.VCSBaseTest):
    def testIsoCelinePart1(self):
        pth = os.path.join(self.basedatadir, "vcs")
        f = cdms2.open(os.path.join(pth, "celine.nc"))
        s = f("data")
        self.x.setcolormap("classic")
        self.x.scriptrun(os.path.join(pth, "celine.json"))
        i = self.x.getisofill("celine")
        self.x.plot(s, i, bg=1)
        self.checkImage("test_vcs_iso_celine_part1.png")
