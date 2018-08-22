import basevcstest


class TestVCSDateAsString(basevcstest.VCSBaseTest):
    def testVCSDateAsString(self):
        s = self.clt("clt", squeeze=1)
        self.x.plot(s, bg=self.bg, time='2015-02-23')
        fnm = "test_vcs_user_passed_date_as_string.png"
        self.checkImage(fnm)
