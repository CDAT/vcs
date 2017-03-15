import basevcstest

class TestVCSClose(basevcstest.VCSBaseTest):
    def testClose(self):
        data = self.clt('clt')
        self.x.plot(data, bg=1)
        self.x.close()
