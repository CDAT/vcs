import basevcstest

class TestVCSLambert(basevcstest.VCSBaseTest):
    def testLambert(self):
        s = self.clt("clt")
        iso = self.x.createisofill()
        p=self.x.createprojection()
        p.type="lambert"
        iso.projection = p
        self.x.plot(s(latitude=(20, 60),longitude=(-140,-20)), iso, bg=self.bg)
        self.checkImage("test_vcs_lambert.png")
