import basevcstest


class TestVCSColors1D(basevcstest.VCSBaseTest):
    def test_ColorRGBA1D(self):
        data = self.clt("clt")[:, 5, 8]
        gm = self.x.create1d()
        gm.linecolor = "salmon"
        gm.markercolor = [0, 0, 100]
        self.x.plot(data, gm, bg=self.bg)
        self.checkImage('test_vcs_settings_color_name_rgba_1d.png')
