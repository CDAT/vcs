import basevcstest
import numpy


class TestVCSInfinty(basevcstest.VCSBaseTest):
    def testInfinity(self):

        s = numpy.sin(numpy.arange(100))
        s = numpy.reshape(s, (10, 10))

        s[4, 6] = numpy.inf
        s[7, 9] = numpy.NINF
        s[9, 2] = numpy.nan

        self.x.plot(s, bg=self.bg)
        self.checkImage("test_vcs_infinity.png")
