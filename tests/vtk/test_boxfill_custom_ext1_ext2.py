import basevcstest
import vcs

class TestVCSBoxfillCustomExt1Ext2(basevcstest.VCSBaseTest):
    def testBoxfillCustomExt1Ext2(self):
        clt = self.clt("clt")
        clt = clt(latitude=(-90.0, 90.0), longitude=(-180., 175.), squeeze=1,
                  time=('1979-1-1 0:0:0.0', '1988-12-1 0:0:0.0'))
        boxfill = self.x.createboxfill()
        boxfill.boxfill_type = 'custom'
        levels = range(20, 81, 10)
        boxfill.levels = levels
        boxfill.ext_1 = "y"
        boxfill.ext_2 = "y"
        boxfill.fillareacolors = vcs.getcolors(boxfill.levels)
        self.x.plot(clt, boxfill, bg=self.bg)
        self.checkImage("test_vcs_boxfill_custom_ext1_ext2.png")
