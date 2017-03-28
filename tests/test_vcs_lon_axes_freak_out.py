import basevcstest

class TestVCSLon(basevcstest.VCSBaseTest):
    def testVCSLongitudeFreakOut(self):
        ## Must have historical for plotting and clearing 's'
        s = self.clt("clt")
        s3 = self.clt("clt",longitude=(0,360))

        self.x.plot(s,bg=self.bg)
        self.x.clear()
        self.x.plot(s3,bg=self.bg)
        fnm = "test_vcs_lon_axes_freak_out.png"
        self.checkImage(fnm)
