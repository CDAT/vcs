import basevcstest

class TestVCSIsolines(basevcstest.VCSBaseTest):
    def testIsolineLabel(self):
        data = self.clt("clt")
        isoline = self.x.createisoline()
        isoline.label="y"
        texts=[]
        colors = []
        for i in range(10):
            text = self.x.createtext()
            text.color = 50 + 12 * i
            text.height = 12
            colors.append(100 + 12 * i)
            if i%2 == 0:
              texts.append(text.name)
            else:
              texts.append(text)
        isoline.text = texts

        # First test using isoline.text[...].color
        self.x.plot(data, isoline, bg=self.bg)

        fnm = "test_vcs_isoline_labels.png"
        self.checkImage(fnm)

        # Now set isoline.linecolors and test again.
        self.x.clear()
        isoline.linecolors = colors
        self.x.plot(data, isoline, bg=self.bg)
        fnm = "test_vcs_isoline_labels2.png"
        self.checkImage(fnm)

        # Now set isoline.textcolors and test again.
        self.x.clear()
        isoline.textcolors = colors
        self.x.plot(data, isoline, bg=1)
        fnm = "test_vcs_isoline_labels3.png"
        self.checkImage(fnm)
