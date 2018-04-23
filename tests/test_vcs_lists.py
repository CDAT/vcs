import unittest
import vcs

class TestVCSList(unittest.TestCase):
    def test_list_function(self):
        types = vcs.listelements()
        
        for typ in types:
            if typ in ["display", "font", "fontNumber", "list"]:
                continue
            print("testing: ",typ)
            ldict = locals()
            exec("obj = vcs.create{}()".format(typ), globals(), ldict)
            obj = ldict['obj']
            obj.list()

