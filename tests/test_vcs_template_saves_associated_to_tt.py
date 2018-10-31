from __future__ import print_function
import basevcstest
import os
import filecmp


class TestVCSTemplate(basevcstest.VCSBaseTest):
    def testTemplateSaveAssociated(self):

        tt = self.x.createtexttable("this_is_my_test_tt")
        t = self.x.createtemplate("this_is_our_test_template")

        t.xname.texttable = tt

        fnm = "template_test_associated_dump.json"
        if os.path.exists(fnm):
            os.remove(fnm)

        t.script(fnm)
        good = os.path.join(os.path.dirname(__file__), "share", fnm)
        print("Comparing:", os.path.realpath(fnm), good)
        assert filecmp.cmp(fnm, good)
        os.remove(fnm)
