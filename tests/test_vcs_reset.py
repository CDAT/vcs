import unittest
import vcs

class VCSTestReset(unittest.TestCase):
    def testVCSreset1only(self):
        for gtype in vcs.listelements():
            b0 = vcs.listelements(gtype)
            if gtype == 'colormap':
                b = vcs.createcolormap()
                xtra = vcs.createisofill()
                untouched = vcs.listelements("isofill")
            elif gtype == "template":
                b = vcs.createtemplate()
            elif gtype == "textcombined":
                b = vcs.createtextcombined()
            elif gtype == "textorientation":
                b = vcs.createtextorientation()
            elif gtype == "texttable":
                b = vcs.createtexttable()
            elif gtype == "fillarea":
                b = vcs.createfillarea()
            elif gtype == "projection":
                b = vcs.createprojection()
            elif gtype == "marker":
                b = vcs.createmarker()
            elif gtype == "line":
                b = vcs.createline()
            elif gtype in ["display", "font", "fontNumber", "list"]:
                vcs.manageElements.reset()
                continue
            else:
                b = vcs.creategraphicsmethod(gtype)
            if gtype != "colormap":
                xtra = vcs.createcolormap()
                untouched = vcs.listelements("colormap")
            b1 = vcs.listelements(gtype)
            self.assertNotEqual(b0,b1)
            vcs.manageElements.reset(gtype)
            b2 = vcs.listelements(gtype)
            self.assertEqual(b0,b2)
            if gtype == "colormap":
                self.assertEqual(untouched,vcs.listelements("isofill"))
            else:
                self.assertEqual(untouched,vcs.listelements("colormap"))
            vcs.manageElements.reset()
            if gtype == "colormap":
                self.assertNotEqual(untouched,vcs.listelements("isofill"))
            else:
                self.assertNotEqual(untouched,vcs.listelements("colormap"))

        # case for 1d weirdness
        sc = vcs.createscatter()
        vcs.manageElements.reset()
            

