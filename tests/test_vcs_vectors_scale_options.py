import basevcstest

class TestVCSVectorScale(basevcstest.VCSBaseTest):
    def coreTest(self,scalingType,scale=None,inc=1):
        v = self.clt['v'][...,::inc,::inc]
        u = self.clt['u'][...,::inc,::inc]

        gv = self.x.createvector()

        gv.scaletype = scalingType
        if scale is not None:
            gv.scale = scale
        self.x.plot(u, v, gv, bg=1)
        outFilename = 'test_vcs_vectors_scale_options_%s.png' % scalingType
        self.checkImage(outFilename)
        self.x.clear()

    def testVCSVectorScalingOptions(self):
        self.coreTest("off",None,10)
        self.coreTest("constant",.1,4)
        self.coreTest("linear",1.)
        self.coreTest("normalize",1.)
        self.coreTest("constantNLinear",1.)
        self.coreTest("constantNNormalize",1.)
