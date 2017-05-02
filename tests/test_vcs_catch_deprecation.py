import unittest
import vcs
import warnings
#warnings.simplefilter("default")
warnings.resetwarnings()

class VCSDeprecationTest(unittest.TestCase):
    def testCatchDeprecationWarning(self):
        with warnings.catch_warnings(record=True) as w:
            warnings.warn("Can you catch me?",vcs.VCSDeprecationWarning)
            #warnings.warn("Can you catch me?",DeprecationWarning)
            self.assertEqual(w[0].category, vcs.VCSDeprecationWarning)
            print w
            print w[0].category
