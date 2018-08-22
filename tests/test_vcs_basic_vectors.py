import basevcstest
import vcs
import MV2
import cdms2
import os
import numpy


class TestVCSBasicVectors(basevcstest.VCSBaseTest):
    def basicVector(self, projtype="default", amplitude=False,
                    scale=1., angle=45., nlat=45, nlon=72):
        self.x.clear()
        cdms2.tvariable.TransientVariable.variable_count = 1

        self.x.setcolormap("rainbow")
        gm = self.x.createvector()
        gm.scale = scale
        nm_xtra = ""
        xtra = {}
        # Creates 4x5 grid
        dlat = 180. / nlat
        lats = cdms2.createAxis(numpy.arange(-90 + dlat / 2., 90, dlat))
        lats.id = "latitude"
        lats.units = "degrees_north"
        lons = cdms2.createAxis(numpy.arange(0, 360, 360. / nlon))
        lons.id = "longitude"
        lons.units = "degrees_east"
        print(len(lats), len(lons))
        if angle in [-45, 0, 45]:
            u = MV2.ones((nlat, nlon))
        elif angle in [-135, -180, 135]:
            u = -MV2.ones((nlat, nlon))
        else:
            u = MV2.zeros((nlat, nlon))
        if angle in [45, 90, 135]:
            v = MV2.ones((nlat, nlon))
        elif angle in [-45, -90, -135]:
            v = -MV2.ones((nlat, nlon))
        else:
            v = MV2.zeros((nlat, nlon))
        if amplitude:
            nm_xtra = "_amplitude"
            U = numpy.cos(lons[:])
            V = numpy.sin(lats[:])
            A = 3 + MV2.array(V[:, numpy.newaxis] * U[numpy.newaxis, :])
            A.setAxis(0, lats)
            A.setAxis(1, lons)
            u *= A
            v *= A
            # Now plots the amplitude underneath the data
            b = self.x.createboxfill()
            b.xticlabels1 = vcs.elements["list"]["Lon30"]
            b.yticlabels1 = vcs.elements["list"]["Lat20"]
            self.x.plot(A, b, bg=self.bg)
        u.setAxis(0, lats)
        u.setAxis(1, lons)
        v.setAxis(0, lats)
        v.setAxis(1, lons)
        self.x.plot(u, v, gm, bg=self.bg)
        fnm = "test_vcs_basic_vectors_%i" % angle
        if scale != 1.:
            fnm += "_%.1g" % scale
        fnm += nm_xtra + ".png"
        self.checkImage(fnm)

    def testBasicVectors(self):
        for angle in [-180, -135, -90, -45, 0, 45, 90, 135]:
            self.basicVector(angle=angle)
        for scale in [.5, 2]:
            self.basicVector(scale=scale, angle=45)
        self.basicVector(scale=2., angle=45, amplitude=True)
