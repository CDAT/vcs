import basevcstest
import vcs
import os
import cdms2
import cdutil


class TestVCSOnedLevelAxis(basevcstest.VCSBaseTest):
    def test1dLevelAxis(self):
        f = cdms2.open(os.path.join(vcs.sample_data, "ta_ncep_87-6-88-4.nc"))
        ta = f("ta", time=slice(0, 1), squeeze=1)
        ta = cdutil.averager(ta, axis="yx")
        ta.id = 'ta'
        self.x.plot(ta, bg=self.bg)
        fnm = os.path.splitext(os.path.split(__file__)[1])[0] + ".png"
        self.checkImage(fnm)
