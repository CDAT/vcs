import basevcstest


class TestVCSIsofill(basevcstest.VCSBaseTest):
    def testIsofillNorthToSouth(self):

        clt = self.clt("clt", latitude=(80.0, 38.0), squeeze=1,
                       longitude=(-180.0, 180.0), time=slice(0, 1))
        gm = self.x.createisofill()
        gm.projection = "polar"
        self.x.plot(clt, gm, bg=self.bg)
        self.checkImage("test_vcs_isofill_data_read_north_to_south.png")
