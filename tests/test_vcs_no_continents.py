import basevcstest


class TestVCSNoContinents(basevcstest.VCSBaseTest):
    def testNoContinents(self):

        # Load the clt data:
        clt = self.clt("clt")
        clt = clt(latitude=(-90.0, 90.0), longitude=(-180., 175.), squeeze=1,
                  time=('1979-1-1 0:0:0.0', '1988-12-1 0:0:0.0'))

        template_bottom = self.x.createtemplate()
        template_bottom.scale(.5, "y")
        template_bottom.move(-.15, "y")
        template_top = self.x.createtemplate(source=template_bottom.name)
        template_top.move(.5, 'y')

        self.x.plot(clt, template_bottom, continents=0, bg=self.bg)
        self.x.plot(clt, template_top, continents=1, bg=self.bg)

        self.checkImage("test_vcs_no_continents.png")
