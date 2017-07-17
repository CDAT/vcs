import basetaylortest

class TestVCSTaylor(basetaylortest.VCSTaylorBaseTest):
    def testVCSTaylor(self):
        for i in range(self.Npoints):
            self.taylor.addMarker(id=self.ids[i],
                             id_size=self.id_sizes[i],
                             id_color=self.id_colors[i],
                             symbol=self.symbols[i],
                             color=self.colors[i],
                             size=self.sizes[i])
        self.x.plot(self.data,self.taylor)
        self.checkImage("test_vcs_taylor_marker.png")
        taylor = self.x.createtaylordiagram()
        for i in range(self.Npoints):
            taylor.addMarker(id=self.ids[i],
                             id_size=self.id_sizes[i],
                             id_color=self.id_colors[i],
                             symbol=self.symbols[i],
                             color=self.colors[i],
                             size=self.sizes[i],
                             xoffset=-2.5,
                             yoffset=2.5)
        self.x.clear()
        self.x.plot(self.data,taylor)
        self.checkImage("test_vcs_taylor_markers_offset.png")
        # Other way to set marker attributes
        taylor = self.x.createtaylordiagram()
        taylor.Marker.id = self.ids
        taylor.Marker.id_size = self.id_sizes
        taylor.Marker.id_color = self.id_colors
        taylor.Marker.symbol = self.symbols
        taylor.Marker.color = self.colors
        taylor.Marker.size = self.sizes
        taylor.Marker.xoffset = [-2.5,]*self.Npoints
        taylor.Marker.yoffset = [2.5]*self.Npoints
        self.x.clear()
        self.x.plot(self.data,taylor)
        self.checkImage("test_vcs_taylor_markers_offset.png")

    testVCSTaylor.taylordiagrams = 1
    testVCSTaylor.taylordiagramsMarkers = 1
    testVCSTaylor.markers = 1
