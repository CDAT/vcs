import basevcstest
import vcs

class TestVCSObjects(basevcstest.VCSBaseTest):
    def test_vcs_remove_object(self):
        for t in ["boxfill","isofill","meshfill",
            "vector","yxvsx","xyvsy","xvsy","scatter",
            "1d","isoline","line","fillarea","marker",
            "texttable","textorientation","projection",
            "colormap","textcombined"]:
          print "Testing removal of",t,"objects"
          print "\tfrom canvas"
          exec("o = self.x.create%s()" % t)
          nm = o.name
          self.x.removeobject(o)
          self.assertTrue(nm not in self.x.listelements(t))
          print "\tfrom vcs module"
          exec("o = vcs.create%s()" % t)
          nm = o.name
          vcs.removeobject(o)
          self.assertTrue(nm not in vcs.listelements(t))

