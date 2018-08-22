import vcs
import unittest


class TestVCSCMAP(unittest.TestCase):
    def testGetSetCmapColorcell(self):

        x = vcs.init()

        gm = x.createboxfill()
        cmap = x.createcolormap()

        rgb = cmap.getcolorcell(25)
        self.assertEqual(rgb, [28., 14., 45., 100.])

        rgb = x.getcolorcell(25)
        self.assertEqual(rgb, [28., 14., 45., 100.])

        rgb = x.getcolorcell(25, x)
        self.assertEqual(rgb, [28., 14., 45., 100.])

        rgb = x.getcolorcell(25, gm)
        self.assertEqual(rgb, [28., 14., 45., 100.])

        cmap.setcolorcell(25, 56, 23, 29)
        self.assertEqual(cmap.index[25], [56., 23., 29., 100.])

        cmap.setcolorcell(25, 56, 23, 29, 55.7)
        self.assertEqual(cmap.index[25], [56., 23., 29., 55.7])
