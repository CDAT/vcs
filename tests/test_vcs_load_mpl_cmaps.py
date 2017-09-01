import unittest
import vcs
class VCSMPLCmaps(unittest.TestCase):
    def testLoadMPLCmaps(self):
        import vcs
        original = vcs.listelements("colormap")
        vcs.utils.loadmatplotlibcolormaps()
        mpl = vcs.listelements("colormap")
        self.assertGreater(len(mpl),len(original))
