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
        # This is for circleci that crashes for any mac bg=True
        self.bg = int(os.environ.get("VCS_BACKGROUND",1))
        self.x=vcs.init(geometry={"width": 1200, "height": 1091})
        self.x.setantialiasing(0)
        self.x.drawlogooff()
        self.x.setbgoutputdimensions(1200,1091,units="pixels")
        if not self.bg:
            self.x.open()
        self.orig_cwd = os.getcwd()
        self.tempdir = tempfile.mkdtemp()
        self.pngsdir = "tests_png"
        if not os.path.exists(self.pngsdir):
            os.makedirs(self.pngsdir)
        self.basedir = os.path.join("uvcdat-testdata","baselines","vcs")
        self.clt = cdms2.open(os.path.join(vcs.sample_data, "clt.nc"))


    def tearDown(self):
        os.chdir(self.orig_cwd)
        shutil.rmtree(self.tempdir)
        self.x.clear()
        del(self.x)
        # if png dir is empty (no failures) remove it
        #if glob.glob(os.path.join(self.pngsdir,"*")) == []:
        #    shutil.rmtree(self.pngsdir)

    def checkImage(self,fnm,src=None,threshold=checkimage.defaultThreshold,pngReady=False):
        if src is None:
            src = os.path.join(self.basedir,os.path.basename(fnm))
        fnm = os.path.join(self.pngsdir,fnm)
        print "Test file  :",fnm
        print "Source file:",src
        if not pngReady:
            self.x.png(fnm,width=self.x.bgX,height=self.x.bgY,units="pixels")
        ret = checkimage.check_result_image(fnm,src,threshold)
        self.assertEqual(ret,0)
        return ret

    def check_values_setting(self,gm,attributes,good_values=[],bad_values=[]):
      if isinstance(attributes,str):
	attributes=[attributes,]
      for att in attributes:
	for val in good_values:
	  setattr(gm,att,val)
	for val in bad_values:
	  try:
	    setattr(gm,att,val)
	    success = True
	  except:
	    success = False
	  else:
	    if success:
	      if hasattr(gm,"g_name"):
		nm = gm.g_name
	      elif hasattr(gm,"s_name"):
		nm = gm.s_name
	      else:
		nm=gm.p_name
	      raise Exception,"Should not be able to set %s attribute '%s' to %s" % (nm,att,repr(val))


def run():
    unittest.main()
