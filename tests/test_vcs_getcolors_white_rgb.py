import unittest
import vcs

class VCSGetcolors(unittest.TestCase):
    def testGetColorsRGB(self):
        for white_color in ["white","black","green","blue","pink","salmon","grey"]:
            colors = vcs.getcolors([-0.5,-0.2,0.2,0.5], white=white_color)
            for color in colors:
                if isinstance(color,(list,tuple)):
                    r,g,b = color
                    self.assertTrue(r<=100.)
                    self.assertTrue(g<=100.)
                    self.assertTrue(b<=100.)

