import basevcstest
import MV2
import cdms2

class TestVCS1DBoxfill(basevcstest.VCSBaseTest):
    def testVCS1DBoxfill(self):
        data = MV2.array([4,5,6,7,1,3,7,9,])+230.

        p = cdms2.createAxis([2,5,100,200,500,800,850,1000])

        data.setAxis(0,p)

        data.id="jim"

        gm=self.x.create1d()

        gm.linewidth=0
        gm.datawc_x1=1000
        gm.datawc_x2=0

        gm.markersize=30

        self.x.plot(data,gm,bg=self.bg)

        fnm = "test_vcs_1d_marker_not_shown_if_xaxis_flipped.png"
        self.checkImage(fnm)
