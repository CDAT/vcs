import unittest
import vcs

class TestVCSFonts(unittest.TestCase):
    def testSwitchFonts(self):

        a=vcs.init()
        font1 = a.getfont(1)
        font2 = a.getfont(2)

        # switchfont() by number
        a.switchfonts(1,2)
        new_font1 = a.getfont(1)
        new_font2 = a.getfont(2)
        self.assertEqual(font1, new_font2)
        self.assertEqual(font2, new_font1)

        # switchfont() by name
        a.switchfonts(font1,font2)
        new_font1 = a.getfont(1)
        new_font2 = a.getfont(2)
        self.assertEqual(font1, new_font1)
        self.assertEqual(font2, new_font2)
