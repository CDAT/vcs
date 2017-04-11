import basevcstest
import vcs
import os

class TestVCSAnimateIsoline(basevcstest.VCSBaseTest):
    def testVCSAnimateIsolineTextLabelsColored(self):
        s=self.clt("clt",slice(0,12)) # read only 12 times steps to speed up things
        gm=self.x.createisoline()
        gm.label='y'
        levs = range(0,101,10)
        gm.level=levs
        # add dummy values to levs to get the correct number of cols
        cols=vcs.getcolors(levs+[56,])
        gm.textcolors = cols
        gm.linecolors = cols
        self.x.plot(s,gm,bg=self.bg)
        self.x.animate.create()
        prefix= os.path.splitext(os.path.split(__file__)[1])[0]
        self.x.animate.save("%s.mp4"%prefix)
        pngs = self.x.animate.close(preserve_pngs = True) # so we can look at them again
        ret = 0
        for p in pngs:
            ret += self.checkImage(p,os.path.join(self.basedir,'test_vcs_animate_isoline_text_labels_colored',os.path.basename(p)),pngReady=True)
        if ret == 0:
            os.removedirs(os.path.split(p)[0])
            os.remove("%s.mp4" % prefix)
