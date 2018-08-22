import basevcstest


class TestVCSVerify(basevcstest.VCSBaseTest):
    def testset_ext_2_on_default(self):
        iso = self.x.createisofill()
        iso.levels = [[1.e20, 1.e20]]
        iso.ext_2 = "n"
        assert(iso.levels == [[1.e20, 1.e20]])
