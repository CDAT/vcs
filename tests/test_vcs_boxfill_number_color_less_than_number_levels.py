import basevcstest
import vcs

class TestVCSBoxfill(basevcstest.VCSBaseTest):
    def testBoxfillNumberCOlorLessNumberLevs(self):
        clt = self.clt("clt",latitude=(-90.0, 90.0), longitude=(-180., 175.), squeeze=1,
                  time=('1979-1-1 0:0:0.0', '1988-12-1 0:0:0.0'))
        boxfill = self.x.createboxfill()
        # Change the type
        boxfill.boxfill_type = 'custom'
        levels = range(20,81,10)
        boxfill.levels=levels
        boxfill.ext_1="y"
        boxfill.fillareacolors=vcs.getcolors(levels)
        with self.assertRaises(Exception):
            self.x.plot(clt, boxfill, bg=self.bg)

