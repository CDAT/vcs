
import basevcstest
import vcs

class TestVCSAspectRatio(basevcstest.VCSBaseTest):

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
        self.x.geometry(400, 800)
        self.x.update()
        y = vcs.init()
        y.open()
        y.geometry(800, 400)
        for X in [self.x, y]:
            X.plot(s,gm,ratio=ratio)
            if X.islandscape():
                orient = "ldscp"
            else:
                orient = "port"
            fnm = "aspect_ratio_%s_%s.png" % (orient, ratio)
            X.png(fnm)
            print "fnm:",fnm
            ret +=  self.checkImage(fnm)
        return ret




