import basevcstest

class TestVCSTextsExtents(basevcstest.VCSBaseTest):
    def testUpdateDoesNotTriggerContinents(self):
        s = self.clt["clt"][0]
        self.x.plot(s, continents=0)
        self.x.setcolormap("viridis")
        self.checkImage("test_vcs_update_triggers_continents.png")

