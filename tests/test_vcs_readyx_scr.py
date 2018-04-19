import unittest
import vcs
import os


class TestVCSReadSCR(unittest.TestCase):
    def test_vcs_read_yx_scr(self):

        testfile = os.path.join(
            os.path.dirname(__file__),
            "share",
            "read_yxvsx.scr")
        vcs.scriptrun(testfile)
        self.assertTrue("testyx" in vcs.listelements("yxvsx"))

        y = vcs.getyxvsx("testyx")

        self.assertEqual(y.datawc_x1, -50.)
        self.assertEqual(y.datawc_x2, 20.)
        self.assertEqual(y.datawc_y1, 50.)
        self.assertEqual(y.datawc_timeunits, "days since 2100")
        self.assertEqual(y.datawc_calendar, 135441)
        self.assertEqual(y.xaxisconvert, "log10")
        self.assertEqual(y.yaxisconvert, "area_wt")
        self.assertEqual(y.linetype, "dash")
        self.assertEqual(y.linecolor, [0.0, 0.0, 0.0, 100.0])
        self.assertEqual(y.linewidth, 1)
        self.assertEqual(y.marker, "circle")
        self.assertEqual(y.markercolor, [0.0, 0.0, 0.0, 100.0])
        self.assertEqual(y.markersize, 10)
        self.assertEqual(y.flip, False)
