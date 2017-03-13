import basevcstest

class TestVCSIsolines(basevcstest.VCSBaseTest):
    def testIsolineLabelMultiInput(self):
        s = self.clt("clt")
        iso = self.x.createisoline()
        t = self.x.createtext()
        t.color = 243
        t.height = 25
        to = self.x.createtextorientation()
        to.height = 55
        tt = self.x.createtexttable()
        tt.color = 245
        iso.textcolors = [None,None,None,242,244]
        iso.text = [t,tt,to]
        iso.label = "y"
        self.x.plot(s, iso, bg=self.bg)
        self.checkImage("test_vcs_isoline_labels_multi_label_input_types.png")
