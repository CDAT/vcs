import basevcstest
import cdms2
import os
import vcs


class TestVCSBoxfill(basevcstest.VCSBaseTest):
    def testBoxfillLev1Lev2Ext2(self):
        f = cdms2.open(vcs.sample_data + "/ta_ncep_87-6-88-4.nc")
        s = f("ta", slice(0, 1), longitude=slice(34, 35), squeeze=1) - 273.15
        s = cdms2.MV2.masked_less(s, -45.)
        b = self.x.createboxfill()
        b.level_1 = -40
        b.level_2 = 40
        self.x.plot(s, b, bg=self.bg)
        self.checkImage("test_vcs_boxfill_lev1_lev2_ta_missing.png")
