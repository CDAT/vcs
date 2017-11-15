import basevcstest


class TestVCSProjectionBasics(basevcstest.VCSBaseTest):
    def testProjectionBasics(self):
        s = self.clt("clt", slice(0, 1), squeeze=1)
        i = self.x.createisofill()
        p = self.x.getprojection("polar")
        i.projection = p
        for zoom in ['none', 'subset', 'datawc0', 'datawc1', 'datawc2']:
            if (zoom == 'none'):
                self.x.plot(s, i, bg=self.bg)
            elif (zoom == 'subset'):
                self.x.plot(
                    s(latitude=(-50, 90), longitude=(30, -30)), i, bg=self.bg)
            else:
                i.datawc_x1 = 30
                i.datawc_x2 = -30
                i.datawc_y1 = -50
                i.datawc_y2 = 90
                if (zoom == 'datawc1'):
                    i.datawc_x1, i.datawc_x2 = i.datawc_x2, i.datawc_x1
                if (zoom == 'datawc2'):
                    i.datawc_y1, i.datawc_y2 = i.datawc_y2, i.datawc_y1
                self.x.plot(s, i, bg=self.bg)

            self.checkImage("test_vcs_polar_zoom_" + zoom + ".png")
            self.x.clear()
