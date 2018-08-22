# Check if text chunks are saved correctly in a PNG file
import os
import vcs
import basevcstest


class TestVCSPNG(basevcstest.VCSBaseTest):
    def testPngMetadata(self, *args, **kwargs):
        self.x.plot([1, 2, 3, 4, 5, 4, 3, 2, 1], bg=self.bg)
        fnm = "test_png_metadata.png"
        m = {'one': 'value one', 'two': 'value two'}
        self.x.png(fnm, width=15, metadata=m)
        assert(vcs.png_read_metadata(fnm) == m)
        os.remove(fnm)
