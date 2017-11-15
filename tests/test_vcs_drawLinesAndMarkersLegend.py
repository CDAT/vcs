import basevcstest


class TestVCSDrawMarkerLeg(basevcstest.VCSBaseTest):
    def testDrawMarkerLegend(self):
        t = self.x.createtemplate()
        t.drawLinesAndMarkersLegend(self.x,
                                    ["red", "blue", "green"], [
                                        "solid", "dash", "dot"], [1, 4, 8],
                                    ["blue", "green", "red"], [
                                        "cross", "square", "dot"], [3, 4, 5],
                                    ["sample A", "type B", "thing C"], render=True, bg=self.bg)

        fnm = "test_drawLinesAndMarkersLegend.png"
        self.checkImage(fnm)
