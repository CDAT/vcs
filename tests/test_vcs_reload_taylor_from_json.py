import unittest
import vcs
import filecmp
import os


class TestVCSReload(unittest.TestCase):
    def test_reload_taylordiagram(self):
        good_json = os.path.join(
            os.path.dirname(__file__),
            "share",
            "vcs_test_save_td_to_json.json")
        vcs.scriptrun(good_json)

        td = vcs.gettaylordiagram("vcs_test_save_taylor_to_json_and_python")
        td.script("vcs_test_save_td_to_json_reload")
        self.assertTrue(
            filecmp.cmp(
                "vcs_test_save_td_to_json_reload.json",
                good_json))

    def tearDown(self):
        os.remove("vcs_test_save_td_to_json_reload.json")
