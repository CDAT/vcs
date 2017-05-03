import basevcstest
import numpy

class TestVCS1DBoxfill(basevcstest.VCSBaseTest):
    def testVCS1DBoxfill(self):
        d = numpy.sin(numpy.arange(100))

        b = self.x.createboxfill()

        self.x.plot(d,b,bg=self.bg)


        fnm = "test_vcs_1d_in_boxfill.png"
        self.checkImage(fnm)
