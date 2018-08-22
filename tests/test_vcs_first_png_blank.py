import basevcstest


class TestVCSBlnk(basevcstest.VCSBaseTest):
    def testFirstBlank(self):
        T = self.clt('clt')
        self.x.plot(T, bg=self.bg)
        self.checkImage('first_png_blank.png')
