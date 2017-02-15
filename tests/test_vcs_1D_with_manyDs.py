
_multiprocess_can_split_ = True

import basevcstest
import numpy
import MV2
import os

class TestVCS1DMany(basevcstest.VCSBaseTest):
    def test1DMany(self):

        d = numpy.sin(numpy.arange(100))
        d=numpy.reshape(d,(10,10))


        one = self.x.create1d()

        self.x.plot(d,one,bg=1)


        fnm = "test_vcs_1D_with_manyDs.png"
        self.checkImage(fnm)
