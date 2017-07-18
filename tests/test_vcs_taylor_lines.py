import basetaylortest

class TestVCSTaylor(basetaylortest.VCSTaylorBaseTest):
    def testVCSTaylor(self):
        for i in range(self.Npoints):
            self.taylor.addMarker(id=self.ids[i],
                             id_size=self.id_sizes[i],
                             id_color=self.id_colors[i],
                             symbol=self.symbols[i],
                             color=self.colors[i],
                             size=self.sizes[i],
                             xoffset=-2.5,
                             yoffset=2.5)
        self.taylor.Marker.line = ["tail","line","line","line","line","line","head"]
        self.taylor.Marker.line_type = ["solid",]*self.Npoints
        self.taylor.Marker.line_color = ["dark grey",]*self.Npoints
        self.taylor.Marker.line_size = [5.,5.,5.,5.,5.,5.,5.]
        self.x.plot(self.data,self.taylor)
        self.checkImage("test_vcs_taylor_line.png")
        self.taylor.Marker.line =  ['tail', 'line', 'head', None, 'tail', 'line', 'head']
        self.taylor.Marker.line_type = ["dash","dash","dash","solid","solid","solid","solid"]
        self.x.clear()
        self.x.plot(self.data,self.taylor)
        self.checkImage("test_vcs_taylor_line_split.png")

    testVCSTaylor.taylordiagrams = 1
    testVCSTaylor.taylordiagramsMarkers = 1
    testVCSTaylor.taylordiagramsLines = 1
    testVCSTaylor.markers = 1
    testVCSTaylor.lines = 1
