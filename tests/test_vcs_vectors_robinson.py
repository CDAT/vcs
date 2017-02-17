import basevcstest

class TestVCSVectorsRobinsonWrap(basevcstest.VCSBaseTest):
    def testVCSVectorRobinsonWrap(self):
        f = self.clt
        u = f("u")
        v = f("v")
        V = self.x.createvector()
        p = self.x.createprojection()
        p.type = "robinson"
        V.projection = p
        self.x.plot(u,v,V, bg=1)

        fnm = "test_vcs_vectors_robinson.png"
        self.checkImage(fnm)
