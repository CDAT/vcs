import vcs
import unittest


class TestVCSPicker(unittest.TestCase):
    def save_clicked(self, colormap, color):
        self.assertEqual(color, 135)
        self.clicked = True

    def testColorPickerSelection(self):

        self.clicked = False
        picker = vcs.colorpicker.ColorPicker(
            500, 500, None, None, on_save=self.save_clicked)

        interactor = picker.render_window.GetInteractor()
        interactor.SetEventInformation(250, 260)
        picker.clickEvent(None, None)
        picker.save(0)
        self.assertTrue(self.clicked)
