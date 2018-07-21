import basevcstest

class TestVCSIsofill(basevcstest.VCSBaseTest):

    def testIsofillLevels(self):
        data = self.clt("clt")
        iso = self.x.createisofill()
        iso.projection = 'polar'
        self.x.plot(data,iso)
        self.checkImage("test_vcs_isofill_gap.png")
