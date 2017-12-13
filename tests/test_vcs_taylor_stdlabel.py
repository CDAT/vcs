import basetaylortest


class TestVCSTaylor(basetaylortest.VCSTaylorBaseTest):
    def testVCSTaylor(self):
        self.taylor.standard_deviation_label = "Normalized STD Bla Bla"
        self.x.plot(self.data, self.taylor)
        self.checkImage("test_vcs_taylor_stdlbl.png")

    testVCSTaylor.taylordiagrams = 1
