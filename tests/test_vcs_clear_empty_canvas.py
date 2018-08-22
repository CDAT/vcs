import unittest
import vcs


class TestVCSClear(unittest.TestCase):
    def testClear(self):
        x = vcs.init()
        x.drawlogooff()
        x.clear()
