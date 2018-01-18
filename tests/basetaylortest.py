import basevcstest
import MV2


class VCSTaylorBaseTest(basevcstest.VCSBaseTest):
    def setUp(self):
        super(VCSTaylorBaseTest, self).setUp()
        # Create dummy 7 data
        corr = [.2, .5, .7, .85, .9, .95, .99]
        std = [1.6, 1.7, 1.5, 1.2, .8, .9, .98]
        self.Npoints = len(std)
        self.data = MV2.array(list(zip(std, corr)))
        self.data.id = "My Taylor Diagram Data"
        # Markers attributes for later
        self.ids = ["A1", "A2", "A3", "B", "C1", "C2", "C3"]
        self.sizes = [2.5, 5, 2., 2., 2., 2., 2., ]
        self.symbols = [
            "square",
            "dot",
            "circle",
            "triangle_right",
            "triangle_left",
            "triangle_up",
            "triangle_down"]
        self.colors = [
            "red",
            "black",
            "black",
            "black",
            "black",
            "black",
            "blue"]
        self.id_sizes = [20., 15., 15., 15., 15., 15., 15., ]
        self.id_colors = [
            "orange",
            "grey",
            "grey",
            "grey",
            "grey",
            "grey",
            "cyan"]

        self.taylor = self.x.createtaylordiagram()
