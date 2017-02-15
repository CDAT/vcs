import unittest
import shutil
import os
import vcs
import cdms2
import MV2
import tempfile
import sys
pth = os.path.dirname(__file__)
sys.path.append(pth)
import checkimage
import subprocess
import glob
import MV2

class VCSBaseTest(unittest.TestCase):

    def getTempFile(self, path, mode="r"):
        return self.getFile(os.path.join(self.tempdir, path), mode)

    def setUp(self):
        #global vcs
        #global cdms2
        #global MV2
        #vcs = reload(vcs)
        #cdms2 = reload(cdms2)
        #MV2 = reload(MV2)
        self.x=vcs.init()
        self.x.setantialiasing(0)
        self.x.drawlogooff()
        self.x.setbgoutputdimensions(1200,1091,units="pixels")
        self.orig_cwd = os.getcwd()
        self.tempdir = tempfile.mkdtemp()
        self.pngsdir = "tests_png"
        if not os.path.exists(self.pngsdir):
            os.makedirs(self.pngsdir)
        self.basedir = os.path.join("uvcdat-testdata","baselines","vcs")
        print("WORKNIG DIRECTORY IS:",os.getcwd())



    def tearDown(self):
        os.chdir(self.orig_cwd)
        shutil.rmtree(self.tempdir)
        self.x.clear()
        del(self.x)
        # if png dir is empty (no failures) remove it
        #if glob.glob(os.path.join(self.pngsdir,"*")) == []:
        #    shutil.rmtree(self.pngsdir)

    def checkImage(self,fnm,src=None,threshold=checkimage.defaultThreshold):
        if src is None:
            src = os.path.join(self.basedir,fnm)
        fnm = os.path.join(self.pngsdir,fnm)
        print "Test file  :",fnm
        print "Source file:",src
        self.x.png(fnm)
        ret = checkimage.check_result_image(fnm,src,threshold)
        self.assertEqual(ret,0)
        return ret

def run():
    unittest.main()
