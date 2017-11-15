import basevcstest


class TestVCSIsolines(basevcstest.VCSBaseTest):
    def testIsolineLabelSkip(self):

        data = self.clt("clt")
        isoline = self.x.createisoline()
        isoline.label = "y"
        isoline.labelskipdistance = 15.0
        texts = []
        colors = []
        for i in range(10):
            text = self.x.createtext()
            text.color = 20 * i
            text.height = 12
            colors.append(255 - text.color)
            if i % 2 == 0:
                texts.append(text.name)
            else:
                texts.append(text)
        isoline.text = texts
        isoline.linecolors = colors

        # Next plot the isolines with labels
        self.x.plot(data, isoline, bg=self.bg)
        self.checkImage("test_vcs_isoline_labelskipdistance.png")
