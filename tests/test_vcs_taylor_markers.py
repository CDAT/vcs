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
        self.x.plot(self.data, self.taylor)
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
        self.x.plot(self.data, taylor)
        self.checkImage("test_vcs_taylor_markers_offset.png")
        # Other way to set marker attributes
        taylor = self.x.createtaylordiagram()
        taylor.Marker.id = self.ids
        taylor.Marker.id_size = self.id_sizes
        taylor.Marker.id_color = self.id_colors
        taylor.Marker.symbol = self.symbols
        taylor.Marker.color = self.colors
        taylor.Marker.size = self.sizes
        taylor.Marker.xoffset = [-2.5, ] * self.Npoints
        taylor.Marker.yoffset = [2.5] * self.Npoints
        self.x.clear()
        self.x.plot(self.data, taylor)
        self.checkImage("test_vcs_taylor_markers_offset.png")
        # Ids not on legend
        taylor.idsLocation = "plot"
        self.x.clear()
        self.x.plot(self.data, taylor)
        self.checkImage("test_vcs_taylor_markers_offset_plot_only.png")
        # Ids on legend only
        taylor.idsLocation = "legend"
        self.x.clear()
        self.x.plot(self.data, taylor)
        self.checkImage("test_vcs_taylor_markers_offset_legend_only.png")
        # Ids alternative
        taylor.Marker.id_location = [0, 1, 2, 0, 1, 2, None]
        self.x.clear()
        self.x.plot(self.data, taylor)
        self.checkImage("test_vcs_taylor_markers_offset_onoff_legend.png")
        taylor.idsLocation = "plot"
        self.x.clear()
        self.x.plot(self.data, taylor)
        self.checkImage("test_vcs_taylor_markers_offset_onoff_plot.png")
        taylor.idsLocation = "both"
        self.x.clear()
        self.x.plot(self.data, taylor)
        self.checkImage("test_vcs_taylor_markers_offset_onoff_both.png")

    testVCSTaylor.taylordiagrams = 1
    testVCSTaylor.taylordiagramsMarkers = 1
    testVCSTaylor.markers = 1
