import unittest
import vcs


class TestVCSLineAttributes(unittest.TestCase):
    def test_setlineattributes(self):
        l = vcs.createline("vcs_test_set_line")
        l.color = 242
        l.width = 5.6
        l.type = "dash"

        self.assertEqual(l.color, [242])
        self.assertEqual(l.width, [5.6])
        self.assertEqual(l.type, ["dash"])

        v = vcs.createvector()
        v.setLineAttributes("vcs_test_set_line")

        self.assertEqual(v.linecolor, 242)
        self.assertEqual(v.linewidth, 5.6)
        self.assertEqual(v.linetype, "dash")

        yx = vcs.create1d()
        yx.setLineAttributes(l)

        self.assertEqual(yx.linecolor, 242)
        self.assertEqual(yx.linewidth, 5.6)
        self.assertEqual(yx.linetype, "dash")

        iso = vcs.createisoline()
        # Note "solid" is a line name.
        iso.setLineAttributes([l, "solid", l])

        self.assertEqual(iso.linecolors, [242, 1, 242])
        self.assertEqual(iso.linewidths, [5.6, 1, 5.6])
        self.assertEqual(iso.linetypes, ['dash', 'solid', 'dash'])
