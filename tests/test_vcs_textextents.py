import basevcstest

class TestVCSTextsExtents(basevcstest.VCSBaseTest):
    def drawBox(self,text):
        extents = self.x.gettextextent(text)[0]
        print("EXTENTS:",text.halign,text.valign,text.viewport,extents)
        fa = self.x.createfillarea()
        fa.color = "red"
        fa.worldcoordinate = text.worldcoordinate
        fa.viewport = text.viewport
        fa.x = [extents[0],extents[1],extents[1],extents[0]]
        fa.y = [extents[2],extents[2],extents[3],extents[3]]
        self.x.plot(fa)
        self.x.plot(text)

    def alignments(self, t, xs, ys):
        self.x.clear()
        for x, halign in zip(xs,[0,1,2]):
            t.x = x
            t.halign = halign
            ln = self.x.createline()
            ln.viewport = t.viewport
            ln.worldcoordinate = t.worldcoordinate
            ln.y = [t.worldcoordinate[1],t.worldcoordinate[2]]
            ln.x = [x,x]
            self.x.plot(ln)
            for y, valign in zip(ys,[0,1,2,3,4]):
                if halign == 0:
                    ln = self.x.createline()
                    ln.x = [t.worldcoordinate[0],t.worldcoordinate[1]]
                    ln.y = [y, y]
                    self.x.plot(ln)
                t.y = y
                t.valign = valign
                t.string = ["test_{}_{}".format(halign,valign)]
                self.drawBox(t)
    def testExtentsAlignments(self):
        t = self.x.createtext()
        #self.alignments(t,[.2,.6,.8],[.2,.35,.46,.6,.8])
        #self.checkImage("test_vcs_textextents_reg.png")
        t.viewport = [.2,.6,.3,.8]
        self.alignments(t,[.2,.6,.8],[.2,.35,.46,.6,.8])
        self.checkImage("test_vcs_textextents_vp.png")
