# -*- coding: utf-8 -*-
import unittest
import vcs
import sys


class VCSTestApplyFormat(unittest.TestCase):
    def testApplyFormat(self):
        class Data(object):
            def __repr__(self):
                return 'räpr'
        fmts = vcs.listelements("format")
        print("Formats:",fmts)
        results = ["02", "002", "0002", "02", "002", "0002", " 2",
                   "0.17", "  2", "0.167", "   2", "1.66667E-06",
                   "r\\xe4pr", "0.16666666666666666",
                   "0.16666666666666666", "0.17", "0.167", "1.66667e-06",
                   "räpr", "0.16666666666666666",
                   " 2", "  2", "   2"]
        if sys.version_info.major == 2:
                # different on py2 precision....
                results = ["02", "002", "0002", "02", "002", "0002", " 2",
                   "0.17", "  2", "0.167", "   2", "1.66667E-06", "r\\xe4pr",
                   "0.166666666667",
                   "0.166666666667", "0.17", "0.167", "1.66667e-06",
                   "räpr", "0.166666666667",
                   " 2", "  2", "   2"]
        for fmt, res in zip(fmts,results):
            if "d" in vcs.elements["format"][fmt]:
                value = 2
            elif fmt in ["g", "G"]:
                value = 1./600000.
            elif fmt in ["a", "r"]:
                if sys.version_info.major == 2:
                    #  different on py2 precision....
                    continue
                else:
                    value = Data()
            else:
                value = 1./6.
            print("Testing formatting {} with format {}, expected: {}".format(value, fmt, res))
            self.assertEqual(vcs.template.applyFormat(value, fmt), res)