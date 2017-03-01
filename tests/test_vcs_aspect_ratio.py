
import basevcstest
import vcs

class TestVCSAspectRatio(basevcstest.VCSBaseTest):

    def __init__(self, *args, **kwargs):
        kwargs['geometry'] = {"width": 400, "height": 800}
        super(TestVCSAspectRatio, self).__init__(*args, **kwargs)

    def testAspectRatio(self):
        ret = 0 
        gm = vcs.createisofill()
        s = self.clt("clt", time=slice(0,1), squeeze=1)
        for ratio in ["1t", "2t", ".5t", "autot"]:
            ret += self.plotRatio(s, gm, ratio)
        self.assertEqual(ret, 0)
        return ret

    def plotRatio(self, s, gm, ratio):
        ret = 0
        # y = vcs.init(geometry={"width":800, "height":400})
        # y.setbgoutputdimensions(800, 400, units="pixels")
        # if not self.bg:
        #     y.open()
        for X in [self.x]:
            X.clear()
            X.plot(s, gm, ratio=ratio)
            if X.islandscape():
                orient = "ldscp"
            else:
                orient = "port"
            fnm = "aspect_ratio_%s_%s.png" % (orient, ratio)
            X.png(fnm)
            print "fnm:",fnm
            ret +=  self.checkImage(fnm)
        return ret




