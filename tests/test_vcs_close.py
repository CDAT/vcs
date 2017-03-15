import basevcstest
import vcs

class TestVCSClose(basevcstest.VCSBaseTest):
    def testCloseBg(self):
        self.x=vcs.init()
        data = self.clt('clt')
        self.assertFalse(self.x.isopened())
        self.x.plot(data, bg=True)
        self.assertFalse(self.x.isopened())
        self.x.close()
        self.assertFalse(self.x.isopened())
    def testCloseNoBg(self):
        self.x=vcs.init()
        data = self.clt('clt')
        self.assertFalse(self.x.isopened())
        self.x.plot(data, bg=False)
        self.assertTrue(self.x.isopened())
        self.x.close()
        self.assertFalse(self.x.isopened())
