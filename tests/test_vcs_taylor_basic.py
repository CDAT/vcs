import basetaylortest

class TestVCSTaylor(basetaylortest.VCSTaylorBaseTest):
    def testVCSTaylor(self):
        self.x.plot(self.data,self.taylor)
        self.checkImage("test_vcs_taylor_basic.png")
        self.taylor.referencevalue=1.2
        self.x.clear()
        self.x.plot(self.data,self.taylor)
        self.checkImage("test_vcs_taylor_basic_ref.png")

    testVCSTaylor.taylordiagrams = 1
