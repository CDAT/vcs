import basevcstest


class TestVCSLambertAzimuthal(basevcstest.VCSBaseTest):
    def main(self, centerlongitude, centerlatitude):
        s = self.clt("clt", time=slice(0, 1),
                longitude=(centerlongitude - 40, centerlongitude + 30),
                latitude=(centerlatitude-20,centerlatitude+30))
        gm = self.x.createboxfill()
        p = self.x.createprojection()
        p.type = "lambert azimuthal"
        p.centerlongitude = centerlongitude
        p.centerlatitude = centerlatitude
        gm.projection = p
        self.x.plot(s, gm, bg=self.bg)
        fileName = "test_vcs_lambert_azimuthal_" + str(centerlongitude) +\
                   ".png"
        self.checkImage(fileName)

    def testVCSLambertAzimuthal(self):
        # north america
        self.main(centerlongitude=-97, centerlatitude=35)
        # africa
        self.main(centerlongitude=21, centerlatitude=-5)
