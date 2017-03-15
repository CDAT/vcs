import basevcstest

class TestVCSFillarea(basevcstest.VCSBaseTest):
    def testFATransparecny(self):

        fa1 = self.x.createfillarea()

        fa1.x=[.2,.8,.8,.2]
        fa1.y = [.2,.2,.8,.8]
        fa1.color = 242

        fa2=self.x.createfillarea(source = fa1)

        fa2.x = [.1,.9,.9,.1]
        fa2.y = [.1,.1,.9,.9]

        cmap = self.x.createcolormap()
        cmap.setcolorcell(242,0,0,100,50)

        fa2.colormap = cmap

        self.x.plot(fa1,bg=self.bg)
        self.x.plot(fa2,bg=self.bg)
        
        self.checkImage("test_vcs_fillarea_transparency.png")
