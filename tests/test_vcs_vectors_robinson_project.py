import basevcstest


class TestVCSVectorsRobinsonProject(basevcstest.VCSBaseTest):
    def testVCSVectorRobinsonProject(self):
        f = self.clt

        tmp = self.x.createtemplate()
        tmp.ytic1.x1 = tmp.data.x1
        tmp.ytic1.x2 = tmp.data.x1 - .02

        gm = self.x.createvector()
        gm.scale = 10
        u = f("u")
        gm.projection = "robinson"
        gm.datawc_x1 = -180
        gm.datawc_x2 = -50
        gm.datawc_y1 = 0
        gm.datawc_y2 = 90

        self.x.plot(u-u, u, gm, tmp, ratio="autot")

        fnm = "test_vcs_vectors_robinson_project.png"
        self.checkImage(fnm)
    testVCSVectorRobinsonProject.projection = 1
    testVCSVectorRobinsonProject.robinson = 1
    testVCSVectorRobinsonProject.vectors = 1
