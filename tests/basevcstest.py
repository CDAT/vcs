from __future__ import print_function
import unittest
# import shutil
import os
import vcs
import cdms2
import sys
pth = os.path.dirname(__file__)
sys.path.append(pth)
import checkimage
# import glob


class VCSBaseTest(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        self.geometry = {"width": 1200, "height": 1090}
        if 'geometry' in kwargs:
            self.geometry = kwargs['geometry']
            del kwargs['geometry']
        self.bg = int(os.environ.get("VCS_BACKGROUND", 1))
        if 'bg' in kwargs:
            self.bg = kwargs['bg']
            del kwargs['bg']
        super(VCSBaseTest, self).__init__(*args, **kwargs)

    def setUp(self):
        # This is for circleci that crashes for any mac bg=True
        self.x = vcs.init(geometry=self.geometry, bg=self.bg)
        self.x.setantialiasing(0)
        self.x.drawlogooff()
        if self.geometry is not None:
            self.x.setbgoutputdimensions(self.geometry['width'],
                                         self.geometry['height'],
                                         units="pixels")
        # if not self.bg:
        #    self.x.open()
        self.orig_cwd = os.getcwd()
        self.pngsdir = "tests_png"
        if not os.path.exists(self.pngsdir):
            try:
                os.makedirs(self.pngsdir)
            except:
                pass
        self.basedir = os.path.join("uvcdat-testdata", "baselines", "vcs")
        self.basedatadir = os.path.join("uvcdat-testdata", "data")
        self.clt = cdms2.open(os.path.join(vcs.sample_data, "clt.nc"))

    def tearDown(self):
        os.chdir(self.orig_cwd)
        self.x.clear()
        del(self.x)
        # if png dir is empty (no failures) remove it
        # if glob.glob(os.path.join(self.pngsdir,"*")) == []:
        #    shutil.rmtree(self.pngsdir)

    def checkImage(self, fnm, src=None, threshold=checkimage.defaultThreshold,
                   pngReady=False, pngPathSet=False):
        if src is None:
            src = os.path.join(self.basedir, os.path.basename(fnm))
        if not pngPathSet:
            fnm = os.path.join(self.pngsdir, fnm)
        print("Test file  :", fnm)
        print("Source file:", src)
        if not pngReady:
            self.x.png(
                fnm,
                width=self.x.width,
                height=self.x.height,
                units="pixels")
        ret = checkimage.check_result_image(fnm, src, threshold)
        self.assertEqual(ret, 0)
        return ret

    def check_values_setting(self, gm, attributes,
                             good_values=[], bad_values=[]):
        if isinstance(attributes, str):
            attributes = [attributes, ]
        for att in attributes:
            for val in good_values:
                setattr(gm, att, val)
            for val in bad_values:
                try:
                    setattr(gm, att, val)
                    success = True
                except BaseException:
                    success = False
                else:
                    if success:
                        if hasattr(gm, "g_name"):
                            nm = gm.g_name
                        elif hasattr(gm, "s_name"):
                            nm = gm.s_name
                        else:
                            nm = gm.p_name
                        raise Exception(
                            "Should not be able to set %s attribute '%s' to %s" %
                            (nm, att, repr(val)))


def run():
    unittest.main()
