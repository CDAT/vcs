import unittest
import vcs


class TestVCSColorCell(unittest.TestCase):
    def testColorcells(self):
        b = vcs.createboxfill()
        x = vcs.init()
        b.colormap = "rainbow"
        x.setcolormap("rainbow")
        self.assertEqual(x.colormap, "rainbow")
        self.assertEqual(x.getcolormapname(), "rainbow")
        self.assertEqual(x.getcolormap().name, "default")
        self.assertEqual(x.getcolorcell(16), [55., 6., 98., 100.])
        self.assertEqual(vcs.getcolorcell(16, x), [55., 6., 98., 100.])
        self.assertEqual(vcs.getcolorcell(16, b), [55, 6., 98., 100.])
        vcs.setcolorcell("rainbow", 16, 100, 100, 100)
        self.assertEqual(x.getcolorcell(16), [100., 100., 100., 100.])
        x.setcolorcell(16, 0, 100, 0)
        self.assertEqual(x.getcolorcell(16), [0., 100., 0., 100.])
        vcs.setcolorcell(b, 16, 100, 100, 100)
        self.assertEqual(x.getcolorcell(16), [100., 100., 100., 100.])
