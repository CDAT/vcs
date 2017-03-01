import os
import basevcstest
import struct

def get_image_info(fnm):
    data = open(fnm,"rb").read()
    w, h = struct.unpack('>LL', data[16:24])
    width = int(w)
    height = int(h)
    print "File:",fnm,"size",width, height
    return width, height

class TestVCSPNG(basevcstest.VCSBaseTest):
    def testPngSize(self):
        self.x.plot([1,2,3,4,5,4,3,2,1],bg=1)
        fnm = "test_png_set_size.png"
        self.x.png(fnm,width=15)
        self.assertEqual(get_image_info(fnm), (15,11))
        self.x.png(fnm,height=16)
        self.assertEqual(get_image_info(fnm), (20,16))
        self.x.png(fnm,width=15,height=12)
        self.assertEqual(get_image_info(fnm), (15,12))
        os.remove(fnm)
