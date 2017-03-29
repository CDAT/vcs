import basevcstest

class AllTests(basevcstest.VCSBaseTest):
    def allTests(self, params):
        f = self.clt
        self.x.clear()
        u = f("u")
        v = f("v")
        fnm = "test_vcs_" + params[0]
        if (params[0] == 'streamline'):
            V = self.x.createstreamline()
            if (len(params) >= 2 and params[1] == 'colored'):
                fnm += "_colored"
                V.coloredbyvector = True
            else:
                V.coloredbyvector = False
            if (len(params) >= 3 and params[2] == 'count'):
                fnm += "_count"
                V.numberofglyphs = 10
                V.numberofseeds = 3
                V.filledglyph = False
        else:
            V = self.x.createvector()
        p = self.x.createprojection()
        p.type = "robinson"
        V.projection = p
        self.x.plot(u,v,V, bg=1)
        fnm += "_robinson.png"
        self.checkImage(fnm)

    def test_vcs_vectors_robinson(self):
        self.allTests(params=['vectors'])

    def test_vcs_streamline_robinson(self):
        self.allTests(params=['streamline'])

    def test_vcs_streamline_colored_robinson(self):
        self.allTests(params=['streamline', 'colored'])

    def test_vcs_streamline_colored_count_robinson(self):
        self.allTests(params=['streamline', 'colored', 'count'])
