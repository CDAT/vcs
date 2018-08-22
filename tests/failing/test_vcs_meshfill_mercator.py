import basevcstest
import cdms2
import vcs
import os

class TestVCSMeshfill(basevcstest.VCSBaseTest):
    def testVCSMeshfillMercator(self):
        f=cdms2.open(os.path.join(vcs.sample_data,"sampleCurveGrid4.nc"))
        s=f("sample")
        m=self.x.createmeshfill()
        m.datawc_y1=-85
        m.datawc_y2=85
        p=self.x.createprojection()
        p.type="mercator"
        m.projection=p
        self.x.plot(s,m,bg=self.bg)
        self.checkImage("meshfill_mercator.png")
