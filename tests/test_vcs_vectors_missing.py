import basevcstest
import MV2

class TestVCSVectorsMissing(basevcstest.VCSBaseTest):
    def testVCSVectorMissing(self):
        self.x.setcolormap("rainbow")
        gm=self.x.createvector()
        gm.scale = 1.
        f = self.clt
        u=f("u")
        v=f("v")
        u=MV2.masked_greater(u,35.)
        v=MV2.masked_greater(v,888.)
        self.x.plot(u,v,gm,bg=1)
        fnm = "test_vcs_vectors_missing.png" 
        self.checkImage(fnm)
        
