import vcs
import unittest

def count():
    elts = {}
    for e in vcs.elements:
        elts[e] = len(vcs.elements[e])
    return elts

class VCSReset(unittest.TestCase):
    def testVCSResetUserObjects(self):
        start = count()
        for typ in vcs.listelements():
            try:
                eval("vcs.create%s()" % typ)
            except:
                pass
        # Making sure we created new methods
        self.assertNotEqual(start["isoline"],len(vcs.listelements("isoline")))
        self.assertNotEqual(start["isofill"],len(vcs.listelements("isofill")))
        self.assertNotEqual(start["meshfill"],len(vcs.listelements("meshfill")))
        self.assertNotEqual(start["boxfill"],len(vcs.listelements("boxfill")))
        # Testing removing 2 types of objects
        vcs.reset(["boxfill","isofill"])
        self.assertEqual(start["boxfill"],len(vcs.listelements("boxfill")))
        self.assertEqual(start["isofill"],len(vcs.listelements("isofill")))
        self.assertNotEqual(start["isoline"],len(vcs.listelements("isoline")))
        self.assertNotEqual(start["meshfill"],len(vcs.listelements("meshfill")))
        # Testing others are still here
        self.assertNotEqual(start["isoline"],len(vcs.listelements("isoline")))
        self.assertNotEqual(start["meshfill"],len(vcs.listelements("meshfill")))
        # Testing removing only one type
        vcs.reset("isoline")
        self.assertEqual(start["isoline"],len(vcs.listelements("isoline")))
        # Testing others are still here
        self.assertNotEqual(start["meshfill"],len(vcs.listelements("meshfill")))
        # Removing everything
        vcs.reset()
        end = count()
        for e in end:
            self.assertEqual(start[e],end[e])
        
        

