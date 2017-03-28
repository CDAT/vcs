import basevcstest

class TestVCSVectorsRobinsonWrap(basevcstest.VCSBaseTest):
    def testVCSVectorRobinsonWrap(self):
        f = self.clt
        lon1 = -180
        u = f("clt")
        v = f("clt")
        u = u(longitude=(lon1,lon1+360.))
        v = v(longitude=(lon1,lon1+360.))
        V = self.x.createvector()
        p = self.x.createprojection()
        p.type = "robinson"
        V.projection = p
        self.x.plot(u,v,V, bg=self.bg)

        fnm = "test_vcs_vectors_robinson_wrap.png"
        self.checkImage(fnm)
