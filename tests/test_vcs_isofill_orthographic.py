import basevcstest
import vcs


class TestVCSIsofill(basevcstest.VCSBaseTest):
    def isofillOrthographic(self, centerlatitude):

        a = self.clt("clt")

        p = self.x.getprojection('orthographic')
        p.centerlatitude = centerlatitude
        b = self.x.createisofill()
        b.projection = p
        self.x.plot(a(latitude=(90, -90)), b, bg=self.bg)
        fnm = "test_vcs_isofill_orthographic_%i.png" % centerlatitude
        self.checkImage(fnm)

    def testIsofill(self):
        for lat in [45, 90]:
            self.isofillOrthographic(lat)
