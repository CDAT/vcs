import basevcstest
import cdms2
import vcs

class TestVCSUnstructuredBoxfill(basevcstest.VCSBaseTest):
    def testVCSUnstructuredBoxfill(self):
        f = cdms2.open(os.path.join(vcs.sample_data,"sampleCurveGrid4.nc"))
        s = f("sample")
        self.x.plot(s,bg=self.bg)
        fnm = "test_vcs_plot_unstructured_via_boxfill.png"
        self.checkImage(fnm)
