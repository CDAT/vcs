import basevcstest


class TestVCSLegend(basevcstest.VCSBaseTest):
    def legend(self, extensions, orientation, arrow=None, offset=None):

        iso = self.x.createisofill()
        iso.levels = [
            210,
            220,
            230,
            240,
            250,
            260,
            270,
            275,
            280,
            285,
            290,
            295,
            300,
            305,
            310]
        if extensions in [1, 3]:
            iso.ext_1 = True
        if extensions in [2, 3]:
            iso.ext_2 = True
        t = self.x.createtemplate()
        if orientation == "v":
            t.scale(.7, 'x')
            t.legend.x1 = t.data.x2 + .03
            t.legend.x2 = t.legend.x1 + .1
            t.legend.y1 = t.data.y1
            t.legend.y2 = t.data.y2
        else:
            t.legend.y1 = .05
            t.legend.y2 = .15
            t.legend.x1 = t.data.x1
            t.legend.x2 = t.data.x2
        if offset is not None:
            t.legend.offset = offset
        if arrow is not None:
            t.legend.arrow = arrow
        line = self.x.createline()
        line.color = ["red"]
        line.type = ["dash"]
        line.width = [4]
        t.legend.line = line
        self.x.clear()
        self.x.plot(self.s, t, iso, bg=self.bg)
        fnm = "test_vcs_legend_%s_%s_%s_%s.png" % (
            orientation, offset, extensions, arrow)
        self.checkImage(fnm)

    def testLegend2(self):
        self.s = self.clt("clt", slice(0, 1)) + 210.
        for orientation in ('h', 'v'):
            for offset in (-0.05, 0.015):
                for extension in (0, 1, 2, 3):
                    for arrow in (0.05, 0.25):
                        self.legend(extension, orientation, arrow, offset)
