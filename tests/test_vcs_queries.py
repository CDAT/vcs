import unittest
import vcs


class TestVCSQueries(unittest.TestCase):
    def testVCSQueries(self):
        gms = [
            "boxfill",
            "isofill",
            "isoline",
            "meshfill",
            "scatter",
            "yxvsx",
            "xvsy",
            "xyvsy",
            "vector",
            "streamline"]
        for gm in gms:
            print("testing query work for:", gm)
            loc = locals()
            exec("g=vcs.create%s()" % gm)
            g = loc["g"]
            loc = locals()
            exec("res = vcs.is%s(g)" % gm)
            res = loc["res"]
            self.assertTrue(res)
            for gm2 in gms:
                if gm2 == gm or (gm in ("yxvsx", "xvsy")
                                 and gm2 in ("yxvsx", "xvsy")):
                    continue
                print("\tAsserting %s is not %s" % (gm, gm2))
                loc = locals()
                exec("res = vcs.is%s(g)" % gm2)
                res=loc["res"]
                self.assertFalse(res)
