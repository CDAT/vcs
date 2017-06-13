import unittest
import vcs

class VCSTestSuggestion(unittest.TestCase):
    def testGoodSuggestionGMs(self):
        for gmtype in ["boxfill","isofill","isoline","meshfill","vector","1d"]:
            gm = eval("vcs.create%s()" % gmtype)
            ## Check suggests list of valid attrributes
            with self.assertRaises(AttributeError) as context:
                setattr(gm,"datawc_x3",.5)
            self.assertTrue("did you mean one of ['datawc_x2', 'datawc_x1']" in str(context.exception))
            ## No close match listing all possible attributes
            with self.assertRaises(AttributeError) as context:
                setattr(gm,"SomeRandomAttribute",.5)
            print str(context.exception)
            self.assertTrue("valid attributes are" in str(context.exception))
            ## Only one close match
            with self.assertRaises(AttributeError) as context:
                setattr(gm,"datawc_Timeunits",.5)
            print str(context.exception)
            self.assertTrue("did you mean '" in str(context.exception))
                
                
