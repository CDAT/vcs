import basevcstest
import os
import cdms2

class TestVCSIsofill(basevcstest.VCSBaseTest):
    def isofillLevels(self,data,level):
        levels = {0: range(-5,36,5),
                  1: [-1000, -15, 35],
                  2: [-300, -15, 0, 15, 25],
                  3: range(190, 320, 10)}


        iso=self.x.createisofill()
        iso.levels=levels[level]
        self.x.clear()
        self.x.plot(data,iso)
        self.checkImage("test_vcs_isofill_level%s.png"%level)

    def testIsofillLevels(self):
        fnm = os.path.join(self.basedatadir,"HadSST1870to99.nc")
        f=cdms2.open(fnm)
        data = f("sst")
        for level in [0,1,2]:
            self.isofillLevels(data,level)
        fnm = os.path.join(self.basedatadir,"masked-file.nc")
        f=cdms2.open(fnm)
        data = f("test")
        self.isofillLevels(data,3)

