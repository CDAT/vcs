import vcs
import vtk
import basevcstest
import os

class TestVCSPicker(basevcstest.VCSBaseTest):
    def testColorPickerAppearance(self):
        picker = vcs.colorpicker.ColorPicker(500, 250, None, 0)
        win = picker.render_window

        win.Render()
        out_filter = vtk.vtkWindowToImageFilter()
        out_filter.SetInput(win)

        png_writer = vtk.vtkPNGWriter()
        fnm = "test_vcs_colorpicker_appearance.png"
        png_writer.SetFileName(os.path.join("tests_png",fnm))
        png_writer.SetInputConnection(out_filter.GetOutputPort())
        png_writer.Write()

        self.checkImage(fnm, pngReady=True)
