import unittest
import vcs
import os


class TestVCSReadSCR(unittest.TestCase):
    def test_vcs_read_old_2(self):

        testfile = os.path.join("uvcdat-testdata", "data", "vcs", "old_2.scr")
        Ns = {}
        Es = {}
        for k in list(vcs.elements.keys()):
            Ns[k] = len(list(vcs.elements[k].keys()))
            Es[k] = vcs.listelements(k)
        vcs.scriptrun(testfile)
        Ns2 = {}
        for k in list(vcs.elements.keys()):
            Ns2[k] = len(list(vcs.elements[k].keys()))
        diffs = {
            'projection': 0,
            'colormap': 4,
            'isofill': 102,
            'marker': 15,
            '3d_dual_scalar': 0,
            'texttable': 1,
            '3d_scalar': 0,
            'fillarea': 404,
            'font': 0,
            '3d_vector': 0,
            '1d': 19,
            'template': 128,
            'textcombined': 0,
            'textorientation': 0,
            'xvsy': 0,
            'xyvsy': 15,
            'isoline': 3,
            'boxfill': 3,
            'fontNumber': 0,
            'line': 16,
            'meshfill': 0,
            'yxvsx': 17,
            'taylordiagram': 1,
            'list': 68,
            'display': 0,
            'vector': 5,
            'scatter': 2,
            'format':0,
            "streamline": 0}
        for k in list(vcs.elements.keys()):
            print("Cheking number of new elements for", k)
            self.assertEqual(diffs[k], Ns2[k] - Ns[k])

        gm = vcs.getmarker("navy")
        self.assertEqual(gm.type, ['dot'])
        self.assertEqual(gm.size, [2])
        self.assertEqual(gm.color, [250])
        gm = vcs.getisofill("AMIP2_psl")
        self.assertEqual(
            gm.levels, [
                [
                    -1e+20, 97000.0], [
                    97000.0, 97500.0], [
                    97500.0, 98000.0], [
                        98000.0, 98500.0], [
                            98500.0, 99000.0], [
                                99000.0, 99500.0], [
                                    99500.0, 100000.0], [
                                        100000.0, 100500.0], [
                                            100500.0, 101000.0], [
                                                101000.0, 101500.0], [
                                                    101500.0, 102000.0], [
                                                        102000.0, 102500.0], [
                                                            102500.0, 103000.0], [
                                                                103000.0, 103500.0], [
                                                                    103500.0, 104000.0], [
                                                                        104000.0, 1e+20]])
        self.assertTrue(gm.ext_2)
        self.assertEqual(gm.ymtics1, "lat5")
        self.assertEqual(gm.fillareastyle, "solid")
        self.assertEqual(
            gm.fillareacolors, [
                30, 29, 28, 27, 26, 25, 24, 23, 22, 21, 20, 19, 18, 17, 35, 36])
