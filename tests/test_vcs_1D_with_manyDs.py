
_multiprocess_can_split_ = True

import basevcstest
import numpy
import MV2
import os
import vcs

class TestVCS1DMany(basevcstest.VCSBaseTest):
    def test1DMany(self):

        d = numpy.sin(numpy.arange(100))
        d = numpy.reshape(d, (10, 10))

        one = self.x.create1d()

        print("glob min mac::", vcs.minmax(d))
        print("plt minmax: ", vcs.minmax(d[0]))
        self.x.plot(d, one, bg=self.bg)

        fnm = "test_vcs_1D_with_manyDs.png"
        self.checkImage(fnm)
