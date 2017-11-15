import unittest
import vcs


class TestVCSShow(unittest.TestCase):
    def testSortedErrorAlpha(self):
        elts = str(vcs.listelements())
        with self.assertRaisesRegex(Exception, elts):
            vcs.show("bad")
