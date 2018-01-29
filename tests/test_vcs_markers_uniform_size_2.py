import basevcstest


class TestVCSMarkers(basevcstest.VCSBaseTest):
    def testVCSMarkersUniform(self):
        names = ['dot', 'plus', 'star', 'circle', 'cross', 'diamond', 'triangle_up', 'square', 'square_fill', 'hurricane', 'w00', 'w01']

        tmpl = self.x.createtemplate()


        tmpl.legend.x1 = .05
        tmpl.legend.x2 = .95

        tmpl.legend.y1 = .05
        tmpl.legend.y2 = .95
        n = len(names)
        size = 10.
        sizes = [size,]*n
        tmpl.drawLinesAndMarkersLegend(self.x, [[0,0,0,0]]*n, 
                ["solid",]*n,
                [size,]*n,
                ["black",]*n,
                names,
                sizes,
                names
                )

        self.checkImage("test_vcs_markers_uniform_2.png")
