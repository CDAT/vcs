import basevcstest

class TestVCS1DDatawc(basevcstest.VCSBaseTest):
    def test1DDatawc(self):
        o = self.x.createfillarea()
        xs = [-70.0, -66.0, -62.0, -58.0, -54.0, -50.0, -46.0, -46.0, -50.0, -54.0, -58.0, -62.0, -66.0, -70.0, -70.]
        ys = [97.40004179212772, 99.24051369561087, 99.64501380920407, 99.50791666242807, 99.25809764862053, 98.72724999321828, 97.86243057250978, 66.1760279867384, 78.08891693751016, 84.6064443588257, 75.83586128552756, 54.88270839055378, 33.08841943740845, 32.207757042513954, 97.40004179212772]
        o.x = xs
        o.y = ys
        o.color = 242
        o.worldcoordinate = [-70,-35,30,100]
        self.x.plot(o,bg=self.bg)
        self.checkImage("test_vcs_black_in_fillarea.png")

