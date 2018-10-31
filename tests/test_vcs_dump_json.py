from __future__ import print_function
import basevcstest
import filecmp
import os


class TestVCSJson(basevcstest.VCSBaseTest):
    def testDumpJson(self):
        fnm = "test_vcs_dump_json.json"
        if os.path.exists(fnm):
            os.remove(fnm)

        b = self.x.createboxfill("vcs_instance")
        b.script("test_vcs_dump_json", "a")
        b = self.x.createisofill("vcs_instance")
        b.script("test_vcs_dump_json", "a")
        b = self.x.createisoline("vcs_instance")
        b.script("test_vcs_dump_json", "a")
        b = self.x.createmeshfill("vcs_instance")
        b.script("test_vcs_dump_json", "a")
        b = self.x.create1d("vcs_instance")
        b.script("test_vcs_dump_json", "a")
        b = self.x.createfillarea("vcs_instance")
        b.script("test_vcs_dump_json", "a")
        b = self.x.createvector("vcs_instance")
        b.script("test_vcs_dump_json", "a")
        b = self.x.createtext("vcs_instance")
        b.script("test_vcs_dump_json", "a")
        b = self.x.createline("vcs_instance")
        b.script("test_vcs_dump_json", "a")
        b = self.x.createmarker("vcs_instance")
        b.script("test_vcs_dump_json", "a")
        b = self.x.createtemplate("vcs_instance")
        b.script("test_vcs_dump_json", "a")
        b = self.x.createprojection("vcs_instance")
        b.script(fnm, "a")

        src = os.path.join(self.basedatadir, "vcs", fnm)
        print("Comparing:", os.path.realpath(fnm), src)
        self.assertTrue(filecmp.cmp(fnm, src))
        # os.remove(fnm)
