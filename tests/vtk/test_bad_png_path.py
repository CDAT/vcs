import os

import basevcstest
import vcs

class TestVCSBadPngPath(basevcstest.VCSBaseTest):
	def testBadPngPath(self):
		self.x.plot([1,2,3,4,5], bg=1)
		try:
		  x.png(os.path.join("b","c","c","test.png"))
		  failed = False
		except:
		  failed = True
		assert(failed)
