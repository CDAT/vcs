import basevcstest

class TestVCSColors(basevcstest.VCSBaseTest):
    def testFewerColorsThanLevels(self):
        data = self.clt("clt")

        boxfill = self.x.createboxfill()

        boxfill.color_1 = 242
        boxfill.color_2 = 250
        boxfill.colormap = "classic"

        self.x.plot(data, boxfill, bg=self.bg)

        self.checkImage("test_fewer_colors_than_levels.png")
