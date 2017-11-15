import basevcstest
import numpy
import MV2
import vcs


class TestVCSEditor(basevcstest.VCSBaseTest):
    def __init__(self, *a, **k):
        k["geometry"] = {"width": 800, "height": 600}
        k["bg"] = False
        super(TestVCSEditor, self).__init__(*a, **k)

    def testMarkerDelete(self):

        m = self.x.createmarker()
        m.x = .1,
        m.y = .1,

        # enable the configurator
        self.x.configure()

        # plot
        dp = self.x.plot(m)

        # Grab the initialized configurator
        c = self.x.configurator

        # Make sure the displays are current
        c.update()

        w, h = 800, 606

        # Retrieve the actor at the specified point
        c.interactor.SetEventInformation(int(.1 * w), int(.1 * h))
        c.click(None, None)
        c.release(None, None)

        # Make sure we've got the correct editor
        editor = c.target
        self.assertIsNotNone(editor, "Could not find an editable object at %i, %i" % (
            int(.1 * w), int(.1 * h)))
        print("Found an editable object")
        self.assertFalse(
            not isinstance(
                editor,
                vcs.editors.marker.MarkerEditor),
            "Object found is not a marker")
        print("Found a marker object")
        self.assertEqual(
            editor.marker, m, "Did not find the correct marker, expected %s %s %s" %
            (m.name, "received", editor.marker.name))
        print("Found the correct marker")

        # Simulate a right click on the marker
        editor.right_release()

        # Make sure the editor has been deactivated
        self.assertNotEqual(c.target == editor, "Did not end edit of object")
        print("Marker no longer being edited")
        # Make sure the marker was deleted
        self.assertFalse(len(m.x) != len(m.y) != len(m.type) != len(
            m.color), "Did not delete all attributes on marker")
        print("Deleted all attributes on marker")
