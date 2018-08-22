import vcs
import os
import unittest


class TestVCSLoadJSON(unittest.TestCase):
    def testLoadJson(self):
        pth = os.path.dirname(__file__)
        json = os.path.join(pth, "share", "test_vcs_json.json")
        for tp in ["boxfill", "meshfill",
                   "isofill", "isoline", "template", "1d"]:
            b4 = vcs.listelements(tp)
            self.assertFalse("Charles.Doutriaux" in b4)
        vcs.scriptrun(json)
        for tp in ["boxfill", "meshfill",
                   "isofill", "isoline", "template", "1d"]:
            after = vcs.listelements(tp)
            self.assertTrue("Charles.Doutriaux" in after)
            gm = vcs.elements[tp]["Charles.Doutriaux"]
