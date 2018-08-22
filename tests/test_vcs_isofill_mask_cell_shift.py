import basevcstest
import MV2


class TestVCSIsofill(basevcstest.VCSBaseTest):
    def testIsofillMaskCellShift(self):
        s = self.clt("clt", slice(0, 1), latitude=(
            30, 70), longitude=(-130, -60))
        s2 = MV2.masked_greater(s, 65.)
        self.x.plot(s2, "default", "isofill", bg=self.bg)
        self.checkImage("test_vcs_isofill_mask_cell_shift.png")
