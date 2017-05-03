import basevcstest
import vcs

class TestVCSBoxfill(basevcstest.VCSBaseTest):
    def boxfillOrthographic(self,centerlatitude):

        a = self.clt("clt")

        p = self.x.getprojection('orthographic')
        p.centerlatitude = centerlatitude
        b = self.x.createboxfill()
        b.projection = p
        self.x.plot(a(latitude=(90,-90)), b, bg=self.bg)
        fnm = "test_vcs_boxfill_orthographic_%i.png" % centerlatitude
        self.checkImage(fnm)

    def testBoxfill(self):
        for lat in [45,90]:
            self.boxfillOrthographic(lat)
