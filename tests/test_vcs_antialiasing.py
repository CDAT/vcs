import unittest
import vcs


class TestVCSAntialias(unittest.TestCase):

    def testAntiAliasing(self):
        x = vcs.init()
        x.open()
        # test it is on by default
        self.assertEqual(x.getantialiasing(), 8)

        # test we can set it
        x.setantialiasing(3)
        self.assertEqual(x.getantialiasing(), 3)
        # test we can set it off
        x.setantialiasing(0)
        self.assertEqual(x.getantialiasing(), 0)
