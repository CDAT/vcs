import basevcstest
import vcs

import numpy


class TestVCSAxisConvert(basevcstest.VCSBaseTest):
    def testAxisConvertBoxfill(self):
        data = self.clt("clt")
        gm = vcs.createboxfill()
        gm.yaxisconvert = 'area_wt'
        self.x.plot(data,gm)
        self.checkImage("test_vcs_axisconvert_boxfill_area_wt.png")
