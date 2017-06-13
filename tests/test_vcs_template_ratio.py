import unittest
import vcs
import numpy

class VCSTestRatio(unittest.TestCase):
    def assertClose(self, my, good):
        self.assertEqual(numpy.ma.allclose(my,good),1)

    def testRatioOne(self):
        t = vcs.createtemplate()
        t.ratio(1)
        self.assertClose(t.data.x1, 0.276658462196)
        self.assertClose(t.data.y1, 0.259999990463)
        self.assertClose(t.data.x2, 0.723341526628)
        self.assertClose(t.data.y2, 0.860000014305)


    def testScaleX(self):
        t = vcs.createtemplate()
        t.scale(.5,axis='x')
        self.assertClose(t.data.x2, 0.499999994412)

    def testScaleY(self):
        t = vcs.createtemplate()
        t.scale(.5,axis='y')
        self.assertClose(t.data.y2, 0.560000002384)

    def testScaleXY(self):
        t = vcs.createtemplate()
        t.scale(.5,axis='xy')
        self.assertClose(t.data.x2, 0.499999994412)
        self.assertClose(t.data.y2, 0.560000002384)

    def testResetX(self):
        t = vcs.createtemplate()
        t.reset('x',.2,.8,t.data.x1,t.data.x2)
        self.assertClose(t.data.x1, 0.2)
        self.assertClose(t.data.x2, 0.8)
