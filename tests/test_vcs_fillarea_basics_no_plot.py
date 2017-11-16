import basevcstest
import vcs


class TestVCSFillarea(basevcstest.VCSBaseTest):
    def testFABasicNoPlot(self):

        f = vcs.createfillarea()
        self.assertTrue(vcs.queries.isfillarea(f))

        self.check_values_setting(f, "style", [
                                  f, 0, 1, 2, 3, "hatch", "pattern", "hallow"], [-1, 4, "foo", [], {}, (), None])
        self.check_values_setting(
            f, "index", [
                None, f, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, ], [
                0, 21, "foo", [], (), {}])
        self.check_values_setting(f, "color", list(range(256)))
        self.check_values_setting(f, "color", [f, "red", [2, 3, 4], [[2, 3, 4], ], [
                                  [1, 2, 3, 5], ], None], [-1, 256, [[2, 3, 4, 6, 5], ]])
        self.check_values_setting(f, ["x", "y"], [None, [1, 2, 3], ], [
                                  1, "sdf", [1, 2, "3"], [[1, 2, 3], 2]])
        b = vcs.createfillarea("self.check_f_ok", f.name)
        self.assertEqual(b.name, "self.check_f_ok")
        self.assertEqual(b.style, ["hallow", ])
        self.assertEqual(b.index, [20, ])
        self.assertEqual(b.color, [[0., 0., 0., 100.]])
        self.assertEqual(f.x, [1, 2, 3])
        self.assertEqual(f.y, [1, 2, 3])
