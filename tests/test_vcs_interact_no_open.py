import unittest
import vcs
import warnings
warnings.filterwarnings("error")


class TestVCSInteract(unittest.TestCase):
    def testInteractNoOpen(self):

        x = vcs.init()
        x.drawlogooff()
        # x.interact()
        with self.assertRaises(Exception) as context:
            x.interact()

        self.assertTrue(
            'Cannot interact if you did not open the canvas yet' in context.exception)
