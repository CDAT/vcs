import basevcstest
import cdms2
import os
import vcs


class TestVCSMeshfillZoom(basevcstest.VCSBaseTest):
    def testVCSMeshfillZoom(self):

        for flip in [True, False]:
            flip = False

            f = cdms2.open(
                os.path.join(
                    vcs.sample_data,
                    "sampleCurveGrid4.nc"))
            s = f("sample")
            m = self.x.createmeshfill()
            m.datawc_x1 = -20
            m.datawc_x2 = 20
            if (flip):
                m.datawc_x1, m.datawc_x2 = m.datawc_x2, m.datawc_x1
            m.datawc_y1 = -20
            m.datawc_y2 = 20
            self.x.clear()
            self.x.plot(s, m, bg=self.bg)

            fileName = "test_vcs_meshfill_zoom"
            if (flip):
                fileName = fileName + '_flip'
            fileName = fileName + '.png'
            self.checkImage(fileName)
