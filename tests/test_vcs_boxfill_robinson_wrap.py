import basevcstest

class TestVCSBoxfill(basevcstest.VCSBaseTest):
    def testRobinsonBoxfill(self):
        # This tests if extending the longitude to more than 360 decrees is handled correctly by
        # proj4. See https://github.com/UV-CDAT/uvcdat/issues/1728 for more information.
        clt3 = self.clt('clt',latitude=(-90.0, 90.0),squeeze=1,longitude=(-180, 200.0),time=('1979-01', '1988-12'),)
        gmBoxfill = self.x.getboxfill('a_robinson_boxfill')
        kwargs = {}
        kwargs[ 'cdmsfile' ] = self.clt.id
        kwargs['bg'] = self.bg
        self.x.plot(clt3, gmBoxfill, **kwargs)
        self.checkImage("test_vcs_boxfill_robinson_wrap.png")
