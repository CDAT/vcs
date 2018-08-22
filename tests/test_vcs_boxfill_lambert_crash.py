import basevcstest
import cdms2
import os
import vcs


class TestVCSBoxfill(basevcstest.VCSBaseTest):
    def testboxfillDecreasingLatitude(self):

        f = cdms2.open(os.path.join(self.basedatadir, "NCEP_09_climo.nc"))
        a = f("Z3")

        p = self.x.getprojection("lambert")
        b = self.x.createboxfill()
        b.projection = p
        self.x.plot(a(latitude=(20, 60), longitude=(-160, -120)),
                    b, bg=self.bg)
        self.checkImage("test_vcs_boxfill_lambert_crash.png")
