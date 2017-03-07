import basevcstest

class TestVCSMissingCMap(basevcstest.VCSBaseTest):
    def testVCSMissingColormap(self):

        # Load the clt data:
        clt = self.clt("clt",slice(0,1),squeeze=1)
        height, width = clt.shape
        clt.mask = [[True if i % 2 else False for i in range(width)] for _ in range(height)]

        # Create and plot quick boxfill with default settings:
        # Only have to test boxfill because all 2D methods use the same code
        # for missing values
        boxfill = self.x.createboxfill()

        # Change the missing color to a colorname
        boxfill.missing = "lightgrey"

        self.x.plot(clt, boxfill, bg=self.bg)
        self.checkImage("test_vcs_missing_colorname.png")
