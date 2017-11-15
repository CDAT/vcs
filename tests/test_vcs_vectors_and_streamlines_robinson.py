import basevcstest


class VCSRobinson(basevcstest.VCSBaseTest):
    def runOne(self, params):
        f = self.clt
        self.x.clear()
        u = f("u")
        v = f("v")
        fnm = "test_vcs_" + params[0]
        if (params[0] == 'streamline'):
            V = self.x.createstreamline()
            V.evenlyspaced = False
            V.integratortype = 2  # rk45
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
                V.integratortype = 1  # rk4
        else:
            V = self.x.createvector()
        p = self.x.createprojection()
        p.type = "robinson"
        V.projection = p
        self.x.plot(u, v, V, bg=1)
        fnm += "_robinson.png"
        self.checkImage(fnm)

    def testVCSVectorsRobinson(self):
        self.runOne(params=['streamline'])
        self.runOne(params=['streamline', 'colored'])
        self.runOne(params=['streamline', 'colored', 'count'])
        self.runOne(params=['streamline', 'colored', 'evenlyspaced'])
        self.runOne(params=['vectors'])
    testVCSVectorsRobinson.vectors = 1  # Nose attribute
    testVCSVectorsRobinson.projection = 1  # Nose attribute
    testVCSVectorsRobinson.robinson = 1  # Nose attribute
    testVCSVectorsRobinson.streamlines = 1  # Nose attribute
