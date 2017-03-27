import vcs
import numpy
import unittest

class TestMKSCALE(unittest.TestCase):
    def testMakeScale(self):
        self.assertTrue(numpy.allclose(vcs.mkscale(0,1.e35,16) , [0.0, 9.9999999999999995e+33, 1.9999999999999999e+34, 2.9999999999999997e+34, 3.9999999999999998e+34, 4.9999999999999998e+34, 5.9999999999999994e+34, 7e+34, 7.9999999999999996e+34, 9.0000000000000001e+34, 9.9999999999999997e+34]))
