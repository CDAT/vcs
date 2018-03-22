import basevcstest
import vcs
import numpy


class TestVCSMeshfillZoom(basevcstest.VCSBaseTest):
    def testVCSMeshfillWrap(self):
        data = numpy.array([1])

        lats = numpy.array([0.])
        lons = numpy.array([0.])

        blats = [-10,-10,10,10]
        blons = [-10,10,10,-10]

        mesh = numpy.zeros((1,2,4))

        mesh[:,0] = blats[:]
        mesh[:,1] = blons[:]

        x = vcs.init()

        gm = vcs.createmeshfill()
        gm.datawc_x1 = -45
        gm.datawc_x2 =  45
        gm.datawc_y1 = -45
        gm.datawc_y2 =  45
        gm.mesh = True
        for wrap in [[22.,0.],[0.,22.],[22.,22.]]:
            gm.wrap = wrap
            self.x.plot(data,mesh,gm)
            fileName = "test_vcs_meshfill_wrap_{:.0f}_{:.0f}.png".format(wrap[0],wrap[1])
            self.checkImage(fileName)
            self.x.clear()
