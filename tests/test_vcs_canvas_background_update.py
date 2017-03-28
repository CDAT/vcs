import basevcstest

class TestVCSBg(basevcstest.VCSBaseTest):
    def __init__(self,*a,**k):
        k["geometry"]={"width":500,"height":500}
        super(TestVCSBg,self).__init__(*a,**k)

    def testBgUpdate(self):
        self.x.backgroundcolor = (255, 255, 255)
        self.x.open()
        self.x.backgroundcolor = (255, 255, 0)
        self.x.update()
        self.checkImage("test_vcs_canvas_background_update.png")
