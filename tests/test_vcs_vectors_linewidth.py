import basevcstest
import numpy as np
import cdms2


class TestVCSVectorLineWidth(basevcstest.VCSBaseTest):
    def lineWidthTest(self, lineWidth=1.0):
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
        gv.linewidth = lineWidth
        self.x.plot(u, v, gv, bg=self.bg, ratio=1)
        label = lineWidth
        outFilename = 'test_vcs_vectors_linewidth_%s.png' % label
        self.checkImage(outFilename)
        self.x.clear()

    def testVCSVectorLineWidthOptions(self):
        for lw in [1.0, 5.0, 10.0]:
            self.lineWidthTest(lineWidth=lw)
