import basevcstest


class TestVCS(basevcstest.VCSBaseTest):
    def testShowElements(self):
        self.x.show("taylordiagram")
        assert(self.x.listelements("taylordiagram") == ["default"])
        assert(
            self.x.listelements() == [
                '1d',
                '3d_dual_scalar',
                '3d_scalar',
                '3d_vector',
                'boxfill',
                'colormap',
                'display',
                'fillarea',
                'font',
                'fontNumber',
                'isofill',
                'isoline',
                'line',
                'list',
                'marker',
                'meshfill',
                'projection',
                'scatter',
                'streamline',
                'taylordiagram',
                'template',
                'textcombined',
                'textorientation',
                'texttable',
                'vector',
                'xvsy',
                'xyvsy',
                'yxvsx'])
        assert(
            self.x.listelements("fontNumber") == [
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15,
                16,
                17, 18, 19, 20, 21, 22, 23, 24, 25])
        self.x.show("textcombined")
        before = self.x.listelements("textcombined")
        t = self.x.createtext()
        after = self.x.listelements("textcombined")
        assert(before != after)
        assert(t.name in after)
