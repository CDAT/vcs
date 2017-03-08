import basevcstest
import vcs

class TestVCSBoxfillCustom(basevcstest.VCSBaseTest):
    def testBoxfillCustom(self):
    	clt = self.clt('clt')
        clt = clt(latitude=(-90.0, 90.0), longitude=(-180., 175.), squeeze=1,
                  time=('1979-1-1 0:0:0.0', '1988-12-1 0:0:0.0'))
        boxfill = self.x.createboxfill()
        default_ext_1 = boxfill.ext_1

        boxfill.boxfill_type = 'custom'
        self.x.plot(clt, boxfill, bg=self.bg)
        self.checkImage("test_vcs_boxfill_custom.png")
        self.x.clear()

        levels = range(20, 81, 10)
        boxfill.levels = levels
        boxfill.fillareacolors = vcs.getcolors(boxfill.levels)
        self.x.plot(clt, boxfill, bg=self.bg)
        self.checkImage("test_vcs_boxfill_custom_non_default_levels.png")
        self.x.clear()

        boxfill.ext_1 = "y"
        boxfill.fillareacolors = vcs.getcolors(boxfill.levels)
        self.x.plot(clt, boxfill, bg=self.bg)
        self.checkImage("test_vcs_boxfill_custom_ext1.png")
        self.x.clear()

        boxfill.ext_1 = default_ext_1
        boxfill.ext_2 = "y"
        boxfill.fillareacolors = vcs.getcolors(boxfill.levels)
        self.x.plot(clt, boxfill, bg=self.bg)
        self.checkImage("test_vcs_boxfill_custom_ext2.png")
        self.x.clear()

        boxfill.ext_1 = "y"
        boxfill.fillareacolors = vcs.getcolors(boxfill.levels)
        self.x.plot(clt, boxfill, bg=self.bg)
        self.checkImage("test_vcs_boxfill_custom_ext1_ext2.png")