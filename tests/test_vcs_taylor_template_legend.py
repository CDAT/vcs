import basetaylortest
import MV2

class TestVCSTaylor(basetaylortest.VCSTaylorBaseTest):
    def testVCSTaylor(self):
        for i in range(self.Npoints):
            self.taylor.addMarker(id=self.ids[i],
                             id_size=self.id_sizes[i],
                             id_color=self.id_colors[i],
                             symbol=self.symbols[i],
                             color=self.colors[i],
                             size=self.sizes[i],
                             xoffset=-2.5,
                             yoffset=2.5)
        template = self.x.createtemplate(source="deftaylor")
        template.legend.x1 = .56
        template.legend.x2 = .98
        template.legend.y1 = .2
        template.legend.y2 = .65
        template.legend.line = "black"
        self.x.plot(self.data,self.taylor,template)
        self.checkImage("test_vcs_taylor_template_legend.png")

    testVCSTaylor.taylordiagrams = 1
    testVCSTaylor.templates = 1
