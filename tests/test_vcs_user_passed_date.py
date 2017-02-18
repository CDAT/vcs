import basevcstest
import cdtime

class TestVCSDate(basevcstest.VCSBaseTest):
    def testVCSDateAsCdtime(self):
        s=self.clt("clt",squeeze=1)
        self.x.plot(s,bg=1,time=cdtime.comptime(2015))
        fnm= "test_vcs_user_passed_date.png"
        self.checkImage(fnm)
