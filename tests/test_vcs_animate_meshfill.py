import basevcstest
import vcs
import os
import cdms2
import MV2

class TestVCSAnimateMeshfill(basevcstest.VCSBaseTest):
    def testVCSAnimateMeshfill(self):
        f=cdms2.open(os.path.join(vcs.sample_data,"sampleCurveGrid4.nc"))
        s=f("sample")
        s2=MV2.resize(s,(4,32,48))
        t=cdms2.createAxis(range(4))
        t.units="months since 2015"
        t.id="time"
        t.designateTime()
        s2.setAxis(0,t)
        s2.setAxis(1,s.getAxis(0))
        s2.setAxis(2,s.getAxis(1))
        s2.setGrid(s.getGrid())
        for i in range(4):
            s2[i]=s2[i]*(1+float(i)/10.)
        gm=self.x.createmeshfill()
        self.x.plot(s2,gm,bg=self.bg)
        self.x.animate.create()
        prefix= os.path.splitext(os.path.split(__file__)[1])[0]
        self.x.animate.save("%s.mp4"%prefix)
        pngs = self.x.animate.close(preserve_pngs = True) # so we can look at them again
        ret = 0
        for p in pngs:
            ret += self.checkImage(p,os.path.join(self.basedir,'test_vcs_animate_meshfill',os.path.basename(p)),pngReady=True)
        if ret == 0:
            os.removedirs(os.path.split(p)[0])
            os.remove("%s.mp4" % prefix)
