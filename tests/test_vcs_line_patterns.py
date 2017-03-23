import basevcstest

class TestVCSLine(basevcstest.VCSBaseTest):
    def __init__(self, *args, **kwargs):
        kwargs['geometry'] = {"width": 1620, "height": 1080}
        super(TestVCSLine, self).__init__(*args, **kwargs)

    def testVCSLinePatterns(self):
        s = self.clt('clt')
        iso = self.x.createisoline()
        iso.level=[5, 50, 70, 95]
        iso.linetypes = ['dot', 'dash', 'dash-dot', 'long-dash']
        self.x.plot(s,iso,continents=0,bg=self.bg)
        name = "test_vcs_line_patterns.png"
        self.checkImage(name)
