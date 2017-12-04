import basevcstest

class TestVCSTextsExtents(basevcstest.VCSBaseTest):
    def drawBox(self,text):
        extents = self.x.gettextextent(text)[0]
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
        bln = self.x.createline()
        vp = t.viewport
        bln.x = [vp[0],vp[1],vp[1],vp[0],vp[0]]
        bln.y = [vp[2],vp[2],vp[3],vp[3],vp[2]]
        bln.color = ["blue",]
        bln.width = 4
        self.x.plot(bln)
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
                    ln.viewport = t.viewport
                    ln.worldcoordinate = t.worldcoordinate
                    ln.x = [t.worldcoordinate[0],t.worldcoordinate[1]]
                    ln.y = [y, y]
                    self.x.plot(ln)
                t.y = y
                t.valign = valign
                t.string = ["test_{}_{}".format(halign,valign)]
                self.drawBox(t)
    def testExtentsAlignments(self):
        t = self.x.createtext()
        self.alignments(t,[.2,.6,.8],[.2,.35,.46,.6,.8])
        self.checkImage("test_vcs_textextents_reg.png")
        t.viewport = [.2,.6,.3,.8]
        t.height = 9
        self.alignments(t,[.2,.6,.8],[.2,.35,.46,.6,.8])
        self.checkImage("test_vcs_textextents_vp.png")
        t.height = 14
        t.viewport = [0,1,0,1]
        t.worldcoordinate = [0.,360.,0.,1.]
        self.alignments(t,[50, 150,300],[.2,.35,.46,.6,.8])
        self.checkImage("test_vcs_textextents_xwc.png")
        t.worldcoordinate = [0.,360.,-20,10.]
        self.alignments(t,[50, 150,300],[-17,-12,-2,5,8])
        self.checkImage("test_vcs_textextents_xywc.png")
        t.worldcoordinate=[0,1,0,1]
        t.angle = 90 
        self.alignments(t,[.2,.6,.8],[.2,.35,.46,.6,.8])
        self.checkImage("test_vcs_textextents_90angle.png")
        t.angle = -90 
        self.alignments(t,[.2,.6,.8],[.2,.35,.46,.6,.8])
        self.checkImage("test_vcs_textextents_neg90angle.png")
        t.angle = 60 
        self.alignments(t,[.2,.6,.8],[.2,.35,.46,.6,.8])
        self.checkImage("test_vcs_textextents_60angle.png")
        t.angle = -60 
        self.alignments(t,[.2,.6,.8],[.2,.35,.46,.6,.8])
        self.checkImage("test_vcs_textextents_neg60angle.png")
        t.angle = 150 
        self.alignments(t,[.2,.6,.8],[.2,.35,.46,.6,.8])
        self.checkImage("test_vcs_textextents_150angle.png")
        t.angle = 199 
        self.alignments(t,[.2,.6,.8],[.2,.35,.46,.6,.8])
        self.checkImage("test_vcs_textextents_199angle.png")
        t.angle = 300
        self.alignments(t,[.2,.6,.8],[.2,.35,.46,.6,.8])
        self.checkImage("test_vcs_textextents_300angle.png")
        t.angle = -120
        self.alignments(t,[.2,.6,.8],[.2,.35,.46,.6,.8])
        self.checkImage("test_vcs_textextents_neg120angle.png")

