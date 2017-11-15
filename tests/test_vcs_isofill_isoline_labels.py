import basevcstest


class TestVCSIsofill(basevcstest.VCSBaseTest):
    def testIsofillIsolineLabels(self):

        data = self.clt("clt")
        isofill = self.x.createisofill()
        self.x.plot(data, isofill, bg=self.bg)
        isoline = self.x.createisoline()
        isoline.label = "y"
        texts = []
        colors = []
        for i in range(10):
            text = self.x.createtext()
            text.color = 255 - 20 * i
            text.height = 12
            colors.append(60 + 5 * i)
            if i % 2 == 0:
                texts.append(text.name)
            else:
                texts.append(text)
        isoline.text = texts
        isoline.linecolors = colors

        # Plot the isolines with labels
        self.x.plot(data, isoline, bg=self.bg)
        self.checkImage("test_vcs_isofill_isoline_labels.png")
