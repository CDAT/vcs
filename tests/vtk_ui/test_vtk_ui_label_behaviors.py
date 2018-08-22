"""
Test label behavior callbacks
"""
import vcs.vtk_ui
import vtk

from vtk_ui_test import vtk_ui_test


class test_vtk_ui_label_behaviors(vtk_ui_test):
    def setUp(self):
        super(test_vtk_ui_label_behaviors, self).setUp()
        self.click_action_happened = False
        self.drag_moved = False
        self.drag_stopped = False

    def do(self):
        self.win.SetSize(100, 30)
        self.args = ["test_vtk_ui_label_behaviors.png"]

        label = vcs.vtk_ui.Label(self.inter, "Test Text", fgcolor=(0, 0, 0), on_click=self.try_action, movable=True, on_move=self.try_move, on_drag=self.try_drag)
        label.show()
        label.top = 10

        self.inter.SetEventInformation(10, 130)

        #click_release
        label.click_release()

        #drag_move
        label.drag_move(.1, .1)

        #drag_stop
        label.drag_stop()

        if False in (self.click_action_happened, self.drag_stopped, self.drag_moved):
            # Behaviors didn't do what they were supposed to
            if not self.click_action_happened:
                print "click_action_happened false"
            if not self.drag_moved:
                print "drag_moved false"
            if not self.drag_stopped:
                print "drag_stopped false"
            return

        if label.top != 7 or label.left != 10:
            print "Moved a wrong amount", label.left, label.top
            return
        # Make sure the text has been dragged appropriately
        self.test_file = "test_vtk_ui_label_behaviors.png"

    def try_action(self, point):
        self.click_action_happened = True

    def try_move(self):
        self.drag_stopped = True

    def try_drag(self, label, dx, dy):
        if dx == .1 and dy == .1:
            self.drag_moved = True

if __name__ == "__main__":
    test_vtk_ui_label_behaviors().test()
