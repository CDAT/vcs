import basevcstest
import cdms2
import cdat_info
import os


class TestVCSBoxfillPickFrame(basevcstest.VCSBaseTest):
    def testBoxfillPickFrame(self):
        f = cdms2.open(os.path.join(cdat_info.get_sampledata_path(), "ta_ncep_87-6-88-4.nc"))
        ta = f("ta")
        # skip first time and second level on second time
        gm = self.x.createisofill()
        self.x.plot(ta, gm, frame=19, bg=self.bg)
        self.checkImage("test_vcs_isofill_pick_frame.png")
