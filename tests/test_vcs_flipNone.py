import basevcstest
import cdms2
import os
import vcs

class TestVCSFlip(basevcstest.VCSBaseTest):
    def testFlipNone(self):
        f=cdms2.open(os.path.join(vcs.sample_data,"ta_ncep_87-6-88-4.nc"))
        s=f("ta",slice(0,1),longitude=slice(90,91),squeeze=1,level=(0,10000))
        self.x.plot(s,bg=self.bg)
        self.checkImage('test_vcs_flipNone.png')
