import cdat_info
import unittest
import nbformat
import os
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
        cmd = "generate_cdat_notebook.py -i test_vcs_generate_simple_plot.png -o test_vcs_generate_simple_plot"
        code, msg = run_command(cmd)
        self.assertEqual(code, 0)
        self.assertTrue(os.path.exists("test_vcs_generate_simple_plot.ipynb"))
        self.checkNB("tests/test_vcs_generate_simple_plot.ipynb", "test_vcs_generate_simple_plot.ipynb")
        os.remove("test_vcs_generate_simple_plot.ipynb")
        os.remove("test_vcs_generate_simple_plot.png")