import basevcstest
import vcs
import warnings
#warnings.filterwarnings('error')


class TestVCSBoxfill(basevcstest.VCSBaseTest):
    def testBoxfillNumberColorMoreNumberLevs(self):
        print("SELF",self.clt)
        clt = self.clt("clt", latitude=(-90.0, 90.0), longitude=(-180., 175.), squeeze=1,
                       time=('1979-1-1 0:0:0.0', '1988-12-1 0:0:0.0'))
        boxfill = self.x.createboxfill()
        # Change the type
        boxfill.boxfill_type = 'custom'
        levels = list(range(20, 81, 10))
        boxfill.levels = levels
        boxfill.ext_1 = "y"
        levels = list(range(20, 81, 5))
        boxfill.fillareacolors = vcs.getcolors(levels)

        warned = False
        with warnings.catch_warnings(record=True) as w:
            self.x.plot(clt, boxfill, bg=self.bg)
            for subw in w:
                if "You asked for 7 levels but provided 12 colors, extra ones will be ignored" in str(subw.message):
                    warned = True

        self.assertTrue(warned, "This test did not issue warning as expected")
