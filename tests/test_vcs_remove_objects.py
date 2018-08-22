import basevcstest
import vcs


class TestVCSObjects(basevcstest.VCSBaseTest):
    def test_vcs_remove_object(self):
        for t in ["boxfill", "isofill", "meshfill",
                  "vector", "yxvsx", "xyvsy", "xvsy", "scatter",
                  "1d", "isoline", "line", "fillarea", "marker",
                  "texttable", "textorientation", "projection",
                  "colormap", "textcombined"]:
            print("Testing removal of", t, "objects")
            print("\tfrom canvas")
            loc = locals()
            exec("o = self.x.create%s()" % t)
            o = loc["o"]
            nm = o.name
            self.x.removeobject(o)
            self.assertTrue(nm not in self.x.listelements(t))
            print("\tfrom vcs module")
            loc = locals()
            exec("o = vcs.create%s()" % t)
            o = loc["o"]
            nm = o.name
            vcs.removeobject(o)
            self.assertTrue(nm not in vcs.listelements(t))
