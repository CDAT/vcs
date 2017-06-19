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
            V.evenlyspaced = False
            V.integratortype = 2 # rk45
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
            if (len(params) >= 3 and params[2] == 'evenlyspaced'):
                fnm += "_evenlyspaced"
                V.evenlyspaced = True
                V.integratortype = 1 # rk4
        else:
            V = self.x.createvector()
        p = self.x.createprojection()
        p.type = "robinson"
        V.projection = p
        self.x.plot(u,v,V, bg=1)
        fnm += "_robinson.png"
        self.checkImage(fnm)

    def testVCSVectorsRobinson(self):
        self.allTests(params=['vectors'])
        self.allTests(params=['streamline'])
        self.allTests(params=['streamline', 'colored'])
        self.allTests(params=['streamline', 'colored', 'count'])
        self.allTests(params=['streamline', 'colored', 'evenlyspaced'])
