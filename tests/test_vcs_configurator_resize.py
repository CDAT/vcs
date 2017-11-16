import basevcstest
import vtk
import os


class TestVSConfigurator(basevcstest.VCSBaseTest):
    def __init__(self, *a, **k):
        k["bg"] = False
        super(TestVSConfigurator, self).__init__(*a, **k)

    def testConfiguratorResize(self):
        self.x.open()
        self.x.configure()

        fnm = "test_vcs_configurator_resize.png"

        win = self.x.backend.renWin
        win.SetSize(814, 303)

        out_filter = vtk.vtkWindowToImageFilter()
        out_filter.SetInput(win)

        win.Render()

        png_writer = vtk.vtkPNGWriter()
        png_writer.SetFileName(os.path.join("tests_png", fnm))
        png_writer.SetInputConnection(out_filter.GetOutputPort())
        png_writer.Write()

        self.checkImage(fnm, pngReady=True)
