import basevcstest
import vcs

import numpy

class TestVCSBasicText(basevcstest.VCSBaseTest):
	def testBasicText(self):
		txt = self.x.createtext()
		txt.x = [.0000005,.00000005,.5,.99999,.999999]
		txt.y = [0.05,.9,.5,.9,0.05]
		txt.string = ["SAMPLE TEXT A","SAMPLE TEXT B","SAMPLE TEXT C","SAMPLE TEXT D","SAMPLE TEXT E"]
		txt.halign = "center"
		txt.valign = "base"
		txt.angle = 45
		self.x.plot(txt, bg=self.bg)
		self.checkImage("test_vcs_basic_text.png")
