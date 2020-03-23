import cdat_info
import unittest
import nbformat
import os
import sys
import vcs
from testsrunner import run_command

class NBTest(unittest.TestCase):
    def checkNB(self, good, test):
        nb_good = nbformat.read(good, nbformat.NO_CONVERT)
        nb_test = nbformat.read(test, nbformat.NO_CONVERT)
        good_cells = nb_good["cells"]
        test_cells = nb_test["cells"]
        self.assertEqual(len(good_cells), len(test_cells))
        for good_cell, test_cell in zip(good_cells, test_cells):
            self.assertEqual(good_cell["cell_type"], test_cell["cell_type"])
            if good_cell["cell_type"] == "code":
                self.assertEqual(good_cell["source"], test_cell["source"])
        return nb_good, nb_test

    def test_generate_notebook_from_png(self):
        run_command("python tests/share/vcs_generate_simple_plot.py")
        metadata = vcs.png_read_metadata("test_vcs_generate_simple_plot.png")
        script = "{p}/bin/generate_cdat_notebook.py".format(p=sys.prefix)
        #cmd = "generate_cdat_notebook.py -i test_vcs_generate_simple_plot.png -o test_vcs_generate_simple_plot"
        cmd = "python {s} -i test_vcs_generate_simple_plot.png -o test_vcs_generate_simple_plot".format(s=script)
        print("COMMAND: {c}".format(c=cmd))
        code, msg = run_command(cmd)
        self.assertEqual(code, 0)
        self.assertTrue(os.path.exists("test_vcs_generate_simple_plot.ipynb"))
        self.checkNB("tests/test_vcs_generate_simple_plot.ipynb", "test_vcs_generate_simple_plot.ipynb")
        os.remove("test_vcs_generate_simple_plot.ipynb")
        os.remove("test_vcs_generate_simple_plot.png")

    def testProvenanceFailIfNotDict(self):
        x = vcs.init(bg=True)
        x.plot([1., 2., 3.])
        with self.assertRaises(RuntimeError):
            x.png("test", provenance="NOT A DICT")

    def testInsertProvenanceAsDict(self):
        prov = {"myprov":4}
        x=vcs.init()
        x.plot([1,2,3])
        x.png("test_insert_prov_from_dict", provenance=prov)
        metadata = vcs.png_read_metadata("test_insert_prov_from_dict.png")
        self.assertTrue("provenance" in metadata)
        self.assertEqual(metadata["provenance"], prov)
        os.remove("test_insert_prov_from_dict.png")


    def testPreserveExistingProvenance(self):
        prov = {"myprov":4}
        metadata = {"provenance":prov}
        x=vcs.init()
        x.plot([1,2,3])
        x.png("test_preserve_prov", metadata=metadata, provenance=True)
        metadata_out = vcs.png_read_metadata("test_preserve_prov.png")
        print(metadata_out["provenance"].keys())
        self.assertTrue("user_provenance" in metadata_out["provenance"])
        self.assertEqual(metadata_out["provenance"]["user_provenance"], prov)
        os.remove("test_preserve_prov.png")
