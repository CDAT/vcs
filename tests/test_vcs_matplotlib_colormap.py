import basevcstest
import matplotlib
import vcs

class TestVCSMatplotlibCMap(basevcstest.VCSBaseTest):
    def testVCSMatplotlibColorMap(self):
        sp = matplotlib.__version__.split(".")
        if int(sp[0])*10+int(sp[1])<15:
            # This only works with matplotlib 1.5 and greater
            sys.exit()

        # Load the clt data:
        clt = self.clt("clt",latitude=(-90.0, 90.0))

        # Initialize self.x:
        self.x.setcolormap(vcs.matplotlib2vcs("viridis"))
        self.x.plot(clt, bg=self.bg)
        fnm = "test_vcs_matplotlib_colormap.png"
        self.checkImage(fnm)
