# Test if the marker can be removed (marker=None) from a 1D plot
# Works in 1.5.1, but fails in 2.1
#
# J-Y Peterschmitt - LSCE - 03/2015
import basevcstest
import numpy

class TestVCSRemoveMarker(basevcstest.VCSBaseTest):
    def test_vcs_remove_marker(self):

        dummy_data = numpy.arange(50, dtype=numpy.float32)
        gm = self.x.createyxvsx('test_yxvsx')

        gm.marker = None
        self.x.plot(gm, dummy_data,bg=self.bg)
        self.checkImage("test_vcs_remove_marker_none_1d.png")
