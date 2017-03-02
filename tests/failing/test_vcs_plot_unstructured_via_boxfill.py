import basevcstest
import os
import cdms2
import vcs

class TestVCSUnstructuredBoxfill(basevcstest.VCSBaseTest):
    def testVCSUnstructuredBoxfill(self):
        f = cdms2.open(os.path.join(vcs.sample_data,"sampleCurveGrid4.nc"))
        s = f("sample")
        self.x.plot(s,bg=self.bg)
        fnm = os.path.split(__file__)[1][:-3] + ".png"
        self.checkImage(fnm)
