import basevcstest


class TestVCSMarkerWmoW07(basevcstest.VCSBaseTest):
    def testVCSW07(self):
        m = self.x.createmarker()
        M = 1
        m.worldcoordinate = [0, M, 0, M]
        m.type = "w07"
        m.color = [242, ]
        m.size = [3.0, 5.0, 12.5]
        m.x = [[.25, ], [.5, ], [.75]]
        m.y = [.5, ]
        self.x.plot(m, bg=self.bg)
        fnm = 'test_vcs_wmo_marker.png'
        self.checkImage(fnm)
