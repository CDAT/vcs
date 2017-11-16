import basevcstest


class TestVCSIsolines(basevcstest.VCSBaseTest):
    def testIsolineWidthStipple(self):

        data = self.clt("clt")
        isoline = self.x.createisoline()
        isoline.label = "y"
        texts = []
        colors = []
        levels = []
        for i in range(7):
            levels.append(i * 10)
            text = self.x.createtext()
            text.color = 255 - 20 * i
            text.height = 12
            colors.append(10 + 10 * i)
            if i % 2 == 0:
                texts.append(text.name)
            else:
                texts.append(text)
        isoline.levels = levels
        isoline.text = texts
        isoline.linecolors = colors
        isoline.linewidths = (1, 2, 3, 4, 1)
        isoline.linetypes = (
            'dot',
            'dash',
            'solid',
            'dash-dot',
            'long-dash',
            'dot',
            'dash')
        # Next plot the isolines with labels
        self.x.plot(data, isoline, bg=self.bg)
        self.checkImage("test_vcs_isoline_width_stipple.png")
