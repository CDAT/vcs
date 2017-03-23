import basevcstest

class TestVCSColorsIsofill(basevcstest.VCSBaseTest):
    def test_ColorRGBAIsofill(self):
        data = self.clt("clt",slice(0,1,))
        gm = self.x.createisofill()
        gm.levels = range(0,110,10)
        gm.fillareacolors = ["green","red","blue","bisque","yellow","grey",
                [100,0,0,50], [0,100,0],"salmon",[0,0,100,75]]
        self.x.plot(data,gm,bg=self.bg)
        self.checkImage("test_vcs_settings_color_name_rgba_isofill.png")
