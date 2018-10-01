import basevcstest
import vcs

class VCSTestTemplateFormat(basevcstest.VCSBaseTest):
    def testFormatFromTemplate(self):
        tmpl = self.x.createtemplate()
        tmpl.min.format = "float3dig"
        tmpl.max.format = ":.6E"
        s = self.clt("clt", slice(0,1))
        s.mean = vcs.template.applyFormat(s.mean(), "2f")
        self.x.plot(s, tmpl)
        self.checkImage("test_vcs_template_format.png")

    def testApplyFormat(self):
        fmts = vcs.listelements("format")
        print("Formats:",fmts)
        results = ["02", "002", "0002", "02", "002", "0002", " 2",
                   "0.17", "  2", "0.167", "   2", "1.66667E-06",
                   "0.16666666666666666", "0.16666666666666666",
                   "0.16666666666666666", "0.17", "0.167", "1.66667e-06",
                   "0.16666666666666666", "0.16666666666666666",
                   " 2", "  2", "   2"]
        for fmt, res in zip(fmts,results):
            if "d" in vcs.elements["format"][fmt]:
                value = 2
            elif fmt in ["g", "G"]:
                value = 1./600000.
            else:
                value = 1./6.
            print("Testing formatting {} with format {}, expected: {}".format(value, fmt, res))
            self.assertEqual(vcs.template.applyFormat(value, fmt), res)