import basevcstest

class TestVCSLine(basevcstest.VCSBaseTest):
    def testVCSLinePintExtensions(self):
        line = self.x.createline()
        line.x = [[0, .1], [.2, .3], [.4, .5], [.6, .7]]
        line.y = [[0, .1], [.2, .3, .4], [.5], [.6, .7]]

        self.x.plot(line, bg=self.bg)
        self.checkImage("test_vcs_line_point_extension.png")

        self.assertEqual(line.x[0], [0, .1])

        self.assertEqual(line.x[1], [.2, .3, .3])

        self.assertEqual(line.y[2], [.5, .5])
