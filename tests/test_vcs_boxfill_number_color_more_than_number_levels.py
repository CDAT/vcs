import basevcstest
import vcs
import warnings
warnings.filterwarnings('error')


class TestVCSBoxfill(basevcstest.VCSBaseTest):
    def testBoxfillNumberColorMoreNumberLevs(self):
        clt = self.clt("clt",latitude=(-90.0, 90.0), longitude=(-180., 175.), squeeze=1,
                  time=('1979-1-1 0:0:0.0', '1988-12-1 0:0:0.0'))
        boxfill = self.x.createboxfill()
        # Change the type
        boxfill.boxfill_type = 'custom'
        levels = range(20,81,10)
        boxfill.levels=levels
        boxfill.ext_1="y"
        levels = range(20,81,5)
        boxfill.fillareacolors=vcs.getcolors(levels)

        try:
            self.x.plot(clt, boxfill, bg=self.bg)
            failed = False
        except Warning:
            failed = True
        except:
            failed = False
            raise

        self.assertTrue(failed,"This test did not issue warning as expected")

