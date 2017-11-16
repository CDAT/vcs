import basevcstest
import vcs

import numpy


class TestVCSBoxfill10x10Numpy(basevcstest.VCSBaseTest):
    def testBoxfill10x10Numpy(self):
        s = numpy.sin(numpy.arange(100))
        s = numpy.reshape(s, (10, 10))
        self.x.plot(s, bg=self.bg)
        self.checkImage("test_vcs_boxfill_10x10_numpy.png")
