import basevcstest

class TestVCSVerify(basevcstest.VCSBaseTest):
    def testReadIsofill(self):
        iso = self.x.getisofill("a_isofill")
        assert(iso.levels!=[])
