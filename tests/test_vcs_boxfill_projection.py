import basevcstest

class TestVCSBoxfill(basevcstest.VCSBaseTest):
    def boxfillProjection(self,projection,zoom):
        a = self.clt("clt")

        self.x.clear()
        p = self.x.getprojection(projection)
        b = self.x.createboxfill()
        b.projection = p
        if zoom is None:
            self.x.plot(a(latitude=(90,-90)), b, bg=self.bg)
            zm = ""
        elif zoom == 'subset':
            self.x.plot(a(latitude=(-50,90), longitude=(30, -30)), b, bg=self.bg)
            zm = "_%s" % zoom
        else:
            b.datawc_x1 = 30
            b.datawc_x2 = -30
            b.datawc_y1 = -50
            b.datawc_y2 = 90
            self.x.plot(a, b, bg=self.bg)
            zm = "_%s" % zoom

        fileName = "test_vcs_boxfill_%s%s.png" % (projection,zm)
        self.checkImage(fileName)
    def testBoxfillProjection(self):
        for proj in "polar mollweide lambert orthographic mercator polyconic robinson".split():
            for zoom in [None,"datawc","subset"]:
                self.boxfillProjection(proj,zoom)

