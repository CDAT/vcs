import vcs
import unittest

class TestVCSScaleFonts(unittest.TestCase):
    def testScaleFontsTemplate(self):
        t = vcs.createtemplate()
        sz = vcs.gettextorientation(t.legend.textorientation).height
        t.scalefont(5.)
        sz2 = vcs.gettextorientation(t.legend.textorientation).height

        print sz,sz2
