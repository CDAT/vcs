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