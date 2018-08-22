import basevcstest
import os
import cdms2


class TestVCSIsofill(basevcstest.VCSBaseTest):
    def testIsoCelinePart2(self):
        pth = os.path.join(self.basedatadir, "vcs")
        f = cdms2.open(os.path.join(pth, "celine.nc"))
        s = f("data")
        self.x.scriptrun(os.path.join(pth, "celine.json"))
        self.x.setcolormap("classic")
        i = self.x.getisofill("celine")
        b = self.x.createboxfill()
        b.levels = i.levels
        b.fillareacolors = i.fillareacolors
        b.boxfill_type = "custom"
        self.x.plot(s, b, bg=self.bg)
        self.checkImage("test_vcs_iso_celine_part2.png")
