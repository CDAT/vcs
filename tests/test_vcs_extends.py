import vcs
import numpy
import unittest


class TestVcsExtend(unittest.TestCase):
    def testExtend(self):

        box = vcs.createboxfill()

        box.ext_1 = True
        self.assertTrue(numpy.allclose(box.levels, [1e20] * 2))

        box.ext_2 = True
        self.assertTrue(numpy.allclose(box.levels, [1e20] * 2))

        box.levels = [1, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
        self.assertFalse(box.ext_1)
        self.assertFalse(box.ext_1)

        box.ext_1 = True
        self.assertTrue(box.levels[0] < -9e19)

        box.ext_2 = True
        self.assertTrue(box.levels[-1] > 9e19)

        box.ext_1 = False
        self.assertTrue(box.levels[0] > -9e19)

        box.ext_2 = False
        self.assertTrue(box.levels[-1] < 9e19)
