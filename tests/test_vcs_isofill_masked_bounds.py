import basevcstest
import os
import cdms2


class TestVCSIsofill(basevcstest.VCSBaseTest):
    def testIsofill(self):

        data = os.path.join(self.basedatadir, "coads_climatology.nc")
        f = cdms2.open(data)
        s = f["SST"]
        t = s.getTime()
        tc = t.asComponentTime()
        print("TC:",tc[:3])
        iso = self.x.getisofill('a_robinson_isofill')
        self.x.plot(s, iso, bg=self.bg)
        self.checkImage("test_vcs_isofill_masked_bounds.png")
