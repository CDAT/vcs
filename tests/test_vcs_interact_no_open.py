import unittest
import vcs
import warnings
#warnings.filterwarnings("error")

class TestVCSInteract(unittest.TestCase):
    def testInteractNoOpen(self):

        x = vcs.init()
        x.drawlogooff()
        # x.interact()
        with warnings.catch_warnings(record=True) as w:
            x.interact()
            self.assertEqual(len(w),1)

        self.assertTrue(
            'Cannot interact if you did not open the canvas yet' in str(w[-1]))
