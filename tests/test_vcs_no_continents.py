import basevcstest

class TestVCSNoContinents(basevcstest.VCSBaseTest):
    def testNoContinents(self):

        # Load the clt data:
        clt = self.clt("clt")
        clt = clt(latitude=(-90.0, 90.0), longitude=(-180., 175.), squeeze=1,
                  time=('1979-1-1 0:0:0.0', '1988-12-1 0:0:0.0'))

        t1 = self.x.createtemplate()
        t1.scale(.5, "y")
        t1.move(-.15, "y")
        t2 = self.x.createtemplate(source=t1.name)
        t2.move(.5, 'y')

        self.x.plot(clt, t1, continents=0, bg=True)
        self.x.plot(clt, t2, continents=1, bg=True)

        self.checkImage("test_vcs_no_continents.png")
