import basevcstest
import numpy
import MV2
import cdms2

class TestVCSUpdateArray(basevcstest.VCSBaseTest):
    def testUpdateArray(self):
        L=cdms2.createAxis(range(0,360,36))
        L.designateLongitude()
        lat = cdms2.createAxis(range(-90,90,18))
        a=numpy.arange(400)
        a.shape=(2,2,10,10)
        b=MV2.cos(a)/2.
        a=MV2.sin(a)
        t=cdms2.createAxis(range(2))
        t.designateTime()
        t.units="months since 2014"
        t.id="time"
        l=cdms2.createAxis(numpy.arange(1,3)*1000.)
        l.designateLevel()
        l.units="hPa"
        l.id="plev"
        a.setAxis(0,t)
        a.setAxis(1,l)
        a.setAxis(2,lat)
        a.setAxis(3,L)
        b.setAxisList(a.getAxisList())
        gm=self.x.createboxfill()
        gm.level_1=-.8
        gm.level_2=.8
        d = self.x.plot(a,gm,bg=1)
        fnm = "test_vcs_update_array_step_1.png"
        self.checkImage(fnm)
        self.x.backend.update_input(d.backend,b(slice(1,2),slice(1,2)))
        fnm = "test_vcs_update_array_step_2.png"
        self.checkImage(fnm)

