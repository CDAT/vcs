import basevcstest
import numpy

class TestVCS1DBoxfill(basevcstest.VCSBaseTest):
    def testVCS1DBoxfill(self):
        d = numpy.sin(numpy.arange(100))

        b = self.x.createboxfill()

        self.x.plot(d+1,b,bg=1)


        fnm = "test_vcs_1d_in_boxfill.png"
        self.checkImage(fnm)
