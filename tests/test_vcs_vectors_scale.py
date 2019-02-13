import basevcstest
import numpy as np
import cdms2

# use syntetic data to test vector scaling and vector legend


class TestVCSVectorScale(basevcstest.VCSBaseTest):
    def coreTest(self, scalingType, scale=None, scalerange=None, ref=None):
        u = cdms2.createAxis(np.array([[1, 1, 0, 1, 1, 1, 0, 1],
                                       [1, 1, 0, 1, 1, 1, 0, 1],
                                       [1, 1, 0, 1, 1, 1, 0, 1],
                                       [1, 1, 0, 1, 1, 1, 0, 1],
                                       [1, 1, 0, 1, 1, 1, 0, 1],
                                       [1, 1, 0, 1, 1, 1, 0, 1],
                                       [1, 1, 0, 1, 1, 1, 0, 1],
                                       [1, 1, 0, 1, 1, 1, 0, 1]]))
        u.id = "u"
        v = cdms2.createAxis(np.array([[1, 0, 1, 0.5, 1, 0, 1, 0.5],
                                       [1, 0, 1, 0.5, 1, 0, 1, 0.5],
                                       [1, 0, 1, 0.5, 1, 0, 1, 0.5],
                                       [1, 0, 1, 0.5, 1, 0, 1, 0.5],
                                       [1, 0, 1, 0.5, 1, 0, 1, 0.5],
                                       [1, 0, 1, 0.5, 1, 0, 1, 0.5],
                                       [1, 0, 1, 0.5, 1, 0, 1, 0.5],
                                       [1, 0, 1, 0.5, 1, 0, 1, 0.5]]))
        v.id = "v"

        gv = self.x.createvector()
        gv.scaletype = scalingType
        if (scalerange):
            gv.scalerange = scalerange
        if scale is not None:
            gv.scale = scale
        if ref is not None:
            gv.reference = ref
        self.x.plot(u, v, gv, bg=self.bg, ratio=1)
        label = scalingType
        if (scalingType == "constant"):
            label += "_" + str(scale)
        outFilename = 'test_vcs_vectors_scale_%s.png' % label
        if ref is not None:
            outFilename = 'test_vcs_vectors_scale_%s_ref_%s.png' % (label, ref)
        self.checkImage(outFilename)
        self.x.clear()

    def testVCSVectorScalingOptions(self):
        self.coreTest("off")
        self.coreTest("constant", scale=0.5)
        self.coreTest("linear", scalerange=[0.5, 1])
        self.coreTest("normalize")
        self.coreTest("constantNLinear", scale=0.5, scalerange=[0.5, 1])
        self.coreTest("constantNNormalize", scale=2)
        # test clamping
        self.coreTest("constant", scale=0.1)
        self.coreTest("constant", scale=2)
        # test reference
        self.coreTest("constant", scale=0.5, ref=1)
        self.coreTest("constant", scale=0.1, ref=5)
        self.coreTest("constant", scale=2, ref=0.5)
    testVCSVectorScalingOptions.vectors = 1
