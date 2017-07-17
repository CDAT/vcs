import basetaylortest
import numpy

def mySkill(s,r):
    return (4*numpy.ma.power(1+r,4))/(numpy.power(s+1./s,2)*numpy.power(1+r*2.,4))

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
        self.x.plot(self.data,self.taylor,skill=self.taylor.defaultSkillFunction)
        self.checkImage("test_vcs_taylor_skills.png")
        self.x.clear()
        self.x.plot(self.data,self.taylor,skill=mySkill)
        self.checkImage("test_vcs_taylor_skills_custom.png")

    testVCSTaylor.taylordiagrams = 1
    testVCSTaylor.taylordiagramsSkills = 1
    testVCSTaylor.taylordiagramsMarkers = 1
    testVCSTaylor.markers = 1
    testVCSTaylor.isolines = 1
