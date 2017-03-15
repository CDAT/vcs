import unittest
import vcs
class TestVSCreateGet(unittest.TestCase):
    def testCreateGet(self):
        x=vcs.init()

        for obj in ["boxfill","isofill","isoline","meshfill","taylordiagram","vector",
                   "1d","3d_scalar","3d_vector","colormap","fillarea","line","marker",
                   "text","projection","template"]:
          print "Testing create/get for %s" % obj
          exec("Ocr = x.create%s()" % obj)
          exec("Ogt = x.get%s(Ocr.name)" %obj)
          self.assertEqual( Ocr.name, Ogt.name)
          exec("Ocr = vcs.create%s()" % obj)
          exec("Ogt = vcs.get%s(Ocr.name)" %obj)
          self.assertEqual( Ocr.name, Ogt.name)
