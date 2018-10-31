import basevcstest


class TestVCSMarker(basevcstest.VCSBaseTest):
    def testStarTriangleMarker(self):
        m = self.x.createmarker()

        m.type = [
            "star",
            "triangle_right",
            "triangle_left",
            "triangle_up",
            "triangle_down"]
        m.x = [[.1], [.3], [.5], [.7], [.9]]
        m.y = [[.1], [.3], [.5], [.7], [.9]]
        m.color = [200, 150, 160, 175, 125]
        m.size = [5, 5, 5, 5, 5]
        self.x.plot(m, bg=self.bg)
        self.checkImage("test_vcs_star_triangle_markers.png")
