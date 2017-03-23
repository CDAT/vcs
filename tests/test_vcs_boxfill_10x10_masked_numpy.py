import basevcstest
import vcs

import numpy

class TestVCSBoxfill10x10MaskedNumpy(basevcstest.VCSBaseTest):
    def testBoxfill10x10MaskedNumpy(self):
        s = numpy.sin(numpy.arange(100))
        s = numpy.reshape(s,(10,10))
        s = numpy.ma.masked_greater(s,.5)
        self.x.plot(s, bg=self.bg)
        self.checkImage("test_vcs_boxfill_10x10_masked_numpy.png")

