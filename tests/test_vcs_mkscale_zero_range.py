import vcs
import unittest

class TestMKSCALE(unittest.TestCase):
    def testMakeScale(self):
        self.assertEqual(vcs.mkscale(3.5,3.5,16), [3.5,])
