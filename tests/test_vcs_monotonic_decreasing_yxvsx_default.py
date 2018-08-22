import basevcstest
import cdms2
import numpy


class TestVCSYxMontonic(basevcstest.VCSBaseTest):
    def testYxMonotonicDecreasing(self):
        t = cdms2.createAxis(numpy.arange(120))
        t.designateTime()
        t.id = "time"
        t.units = "months since 2014"
        data = cdms2.MV2.arange(120, 0, -1)
        data.id = "data"
        data.setAxis(0, t)
        self.x.plot(data, bg=self.bg)
        fnm = 'test_vcs_monotonic_decreasing_yxvsx_default.png'
        self.checkImage(fnm)
