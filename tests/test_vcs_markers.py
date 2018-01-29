import basevcstest


class TestVCSMarkers(basevcstest.VCSBaseTest):
    def testVCSMarkers(self):
        self.x.setcolormap("classic")
        m = self.x.createmarker()
        m.x = [[0., ], [5, ], [10., ], [15.]]
        m.y = [[0., ], [5, ], [10., ], [15.]]
        m.worldcoordinate = [-5, 20, -5, 20]

        # m.worldcoordinate=[-10,10,0,10]
        m.type = ['plus', 'diamond', 'square_fill', "hurricane"]
        m.color = [242, 243, 244, 242]
        m.size = [2, 2, 2, 150]
        self.x.plot(m, bg=self.bg)
        self.checkImage("test_vcs_markers.png")
