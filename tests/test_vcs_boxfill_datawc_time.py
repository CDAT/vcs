import basevcstest


class TestVCSBoxfill(basevcstest.VCSBaseTest):
    def testboxfillDatawcTime(self):
        clt = self.clt("clt", latitude=(-90.0, 90.0), longitude=(0.), squeeze=1,
                       time=('1979-1-1 0:0:0.0', '1988-12-1 0:0:0.0'))

        # Create and plot quick boxfill with default settings:
        boxfill = self.x.createboxfill()

        # Change the type
        boxfill.boxfill_type = 'custom'
        boxfill.datawc_y1 = 12

        self.x.plot(clt, boxfill, bg=self.bg)

        # Load the image testing module:
        # Create the test image and compare:
        self.checkImage("test_vcs_boxfill_datawc_time.png")
