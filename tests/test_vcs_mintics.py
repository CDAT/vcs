import basevcstest

class TestVCSMinTics(basevcstest.VCSBaseTest):
    def testVCSMinTics(self):
        s = self.clt("clt")
        box = self.x.createboxfill()

        # Should ignore the string here
        box.xmtics1 = {i:"Test" for i in range(-180, 180, 15) if i % 30 != 0}
        box.ymtics1 = {i:"Test" for i in range(-90, 90, 5) if i % 10 != 0}
        box.xmtics2 = "lon15"
        box.ymtics2 = "lat5"
        template = self.x.createtemplate()
        template.xmintic1.priority = 1
        template.ymintic1.priority = 1
        template.xmintic2.priority = 1
        template.xmintic2.y2 += template.xmintic1.y1 - template.xmintic1.y2
        template.ymintic2.priority = 1
        self.x.plot(s, template, box, bg=1)
        self.checkImage("test_vcs_mintics.png")
