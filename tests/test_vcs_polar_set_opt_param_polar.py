import basevcstest


class TestVCSPolar(basevcstest.VCSBaseTest):
    def testPolarOptParamPolar(self):

        s = self.clt("clt", slice(0, 1), squeeze=1)
        i = self.x.createisofill()
        p = self.x.getprojection("polar")
        i.projection = p
        self.x.plot(s, i, bg=self.bg)
        fnm = "test_vcs_polar_set_opt_param_polar.png"
        self.checkImage(fnm)
