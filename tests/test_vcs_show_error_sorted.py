import unittest
import vcs

class TestVCSShow(unittest.TestCase):
    def testSortedErrorAlpha(self):
        elts = str(vcs.listelements())
        with self.assertRaisesRegexp(Exception,elts):
            vcs.show("bad")
