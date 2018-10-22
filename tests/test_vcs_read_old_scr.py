import unittest
import vcs
import os


class TestVCSReadSCR(unittest.TestCase):
    def test_vcs_read_old_scr(self):

        testfile = os.path.join("uvcdat-testdata", "data", "vcs", "old.scr")

        Ns = {}
        for k in list(vcs.elements.keys()):
            Ns[k] = len(list(vcs.elements[k].keys()))
        vcs.scriptrun(testfile)
        Ns2 = {}
        for k in list(vcs.elements.keys()):
            Ns2[k] = len(list(vcs.elements[k].keys()))

        diffs = {
            'projection': 0,
            'colormap': 53,
            'isofill': 187,
            'marker': 0,
            '3d_dual_scalar': 0,
            'texttable': 4,
            '3d_scalar': 0,
            'fillarea': 234,
            'font': 0,
            '3d_vector': 0,
            '1d': 9,
            'template': 43,
            'textcombined': 0,
            'textorientation': 3,
            'xvsy': 0,
            'xyvsy': 0,
            'isoline': 113,
            'boxfill': 239,
            'fontNumber': 0,
            'line': 21,
            'meshfill': 0,
            'yxvsx': 9,
            'taylordiagram': 0,
            'list': 26,
            'display': 0,
            'vector': 55,
            'scatter': 0,
            'format': 0,
            "streamline": 0}
        for k in list(vcs.elements.keys()):
            print("---Checking number of new elements for", k)
            self.assertEqual(diffs[k], Ns2[k] - Ns[k])

        gm = vcs.getisofill("pr_time_lat_1")
        self.assertEqual(gm.ymtics1, "lat5")
        self.assertTrue(gm.ext_2)
        self.assertEqual(gm.fillareastyle, "solid")
        self.assertEqual(
            gm.fillareacolors, [
                240, 240, 240, 28, 27, 26, 25, 23, 22, 21, 20, 19, 18, 16])
        gm = vcs.getboxfill("lon_lat_mjop05")
        self.assertEqual(gm.xmtics1, "lon5")
        self.assertEqual(gm.yticlabels1, "lat20")
        self.assertEqual(gm.datawc_x1, 30)
        self.assertEqual(gm.datawc_x2, 210.)
        self.assertEqual(gm.datawc_y1, -30)
        self.assertEqual(gm.datawc_y2, 30.)
        self.assertEqual(gm.level_1, -0.05)
        self.assertEqual(gm.level_2, 0.05)
        self.assertEqual(gm.color_1, 18)
        self.assertEqual(gm.color_2, 219)
        gm = vcs.getline("red_solid")
        self.assertEqual(gm.type, ['solid'])
        self.assertEqual(gm.color, [242])
        self.assertEqual(gm.width, [2.0])

        gm = vcs.getyxvsx("pr_lsfit_lat")
        self.assertEqual(gm.xmtics1, "lat5")
        self.assertEqual(gm.linecolor, 242)
        self.assertEqual(gm.linewidth, 2.)
        self.assertEqual(gm.datawc_x1, 30)
        self.assertEqual(gm.datawc_x2, -30.)
        self.assertEqual(gm.datawc_y1, -5.)
        self.assertEqual(gm.datawc_y2, 5.)
        gm = vcs.getisoline("div_anom")
        self.assertEqual(gm.xmtics1, "lon5")
        self.assertEqual(gm.xticlabels1, "lon15")
        self.assertEqual(gm.linetypes,
                         ['dash',
                          'dash',
                          'dash',
                          'dash',
                          'solid',
                          'dash',
                          'dash',
                          'dash',
                          'solid',
                          'solid',
                          'solid',
                          'solid',
                          'solid',
                          'solid',
                          'solid',
                          'solid',
                          'solid'])
        self.assertEqual(
            gm.linecolors, [
                241, 241, 241, 241, 242, 241, 241, 241, 1, 1, 1, 1, 1, 1, 1, 1, 1])
        self.assertEqual(gm.linewidths,
                         [1.0,
                          1.0,
                          1.0,
                          1.0,
                          2.0,
                          1.0,
                          1.0,
                          1.0,
                          1.0,
                          1.0,
                          1.0,
                          1.0,
                          1.0,
                          1.0,
                          1.0,
                          1.0,
                          1.0])
        gm = vcs.getvector("lon_lat_IO_5")
        self.assertEqual(gm.xmtics1, "lon5")
        self.assertEqual(gm.xticlabels1, "lon20")
        self.assertEqual(gm.linecolor, 242)
        self.assertEqual(gm.linewidth, 2.)
        self.assertEqual(gm.scale, 3)
        self.assertEqual(gm.reference, 5)
