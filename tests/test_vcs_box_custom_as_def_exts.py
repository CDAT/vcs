import basevcstest
import vcs

class TestVCSBoxCustomAsDefExts(basevcstest.VCSBaseTest):
	def testBoxCustomAsDefExts(self):
		gm = self.x.createboxfill()
		gm.boxfill_type = "custom"
		gm.levels = [1.e20,1.e20]
		gm.ext_1 = "y"
		gm.ext_2 = "y"
		s = self.clt("clt", slice(0, 1))
		self.x.plot(s, gm, bg=self.bg)
		self.checkImage("test_box_custom_as_def_exts.png")
