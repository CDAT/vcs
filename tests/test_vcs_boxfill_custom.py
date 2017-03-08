import basevcstest
import vcs

class TestVCSBoxfillCustom(basevcstest.VCSBaseTest):
    def testBoxfillCustom(self):
        clt = self.clt(latitude=(-90.0, 90.0), longitude=(-180., 175.), squeeze=1,
                       time=('1979-1-1 0:0:0.0', '1988-12-1 0:0:0.0'))
        boxfill = self.x.createboxfill()
        boxfill.boxfill_type = 'custom'
        self.x.plot(clt, boxfill, bg=self.bg)
        self.checkImage("test_boxfill_custom.png")