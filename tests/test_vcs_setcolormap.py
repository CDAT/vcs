import basevcstest

class TestVCSColormap(basevcstest.VCSBaseTest):
    def test_Colormap(self):
        data = self.clt('clt')
        t=self.x.gettemplate('default')
        self.x.plot(data, t, bg=True)

        # This should force the image to update
        self.x.setcolormap('blue2darkorange')
        self.checkImage("test_vcs_setcolormap.png")
