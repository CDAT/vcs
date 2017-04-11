import basevcstest


class TestVCSLambertAzimuthal(basevcstest.VCSBaseTest):
    def main(self, centerlongitude):
        s = self.clt("clt", slice(0, 1))
        gm = self.x.createboxfill()
        p = self.x.createprojection()
        p.type = "lambert azimuthal"
        p.centerlongitude = centerlongitude
        gm.projection = p
        self.x.plot(s(longitude=(centerlongitude - 30, centerlongitude + 30)), gm, bg=self.bg)
        fileName = "test_vcs_lambert_azimuthal_" + str(centerlongitude) +\
                   ".png"
        self.checkImage(fileName)

    def testVCSLambertAzimuthal(self):
        # north america
        self.main(centerlongitude=-97)
        # africa
        self.main(centerlongitude=21)
