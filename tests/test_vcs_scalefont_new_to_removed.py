import vcs
import unittest


class VCSScaleFOntToRemoved(unittest.TestCase):
    def testRemoveTo(self):
        #canvas = vcs.init()
        nto = vcs.listelements("textorientation")
        nt = vcs.listelements("template")
        t = vcs.createtemplate()
        t.scalefont(.6)
        # canvas.removeobect(t)
        vcs.removeobject(t)
        nto2 = vcs.listelements("textorientation")
        nt2 = vcs.listelements("template")
        self.assertEqual(len(nto2), len(nto))
        self.assertEqual(len(nt2), len(nt))
