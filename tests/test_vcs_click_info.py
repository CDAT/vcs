import basevcstest
import vcs
import cdms2
import os


class TestVCSClickInfo(basevcstest.VCSBaseTest):
    def __init__(self, *a, **k):
        k["bg"] = False
        k["geometry"] = {"width": 800, "height": 600}
        super(TestVCSClickInfo, self).__init__(*a, **k)

    def clickInfo(self, plot):

        self.x.clear()
        # graphics method
        typ = "_".join(plot.split("_")[1:])
        if (plot.find('autot') != -1):
            gm = self.x.getboxfill("a_boxfill")
        elif (plot.find('boxfill') != -1):
            gm = self.x.getboxfill(plot)
        elif (plot.find('meshfill') != -1):
            gm = self.x.getmeshfill(plot)
            gm.ext_2 = False
            gm.list()
        elif (plot.find('isofill') != -1):
            gm = self.x.getisofill(plot)
        elif (plot.find('isoline') != -1):
            gm = self.x.getisoline(plot)
        elif (plot.find('vector') != -1):
            gm = self.x.getvector(plot[plot.index('_') + 1:])
            typ = "vector"
        else:
            print("Invalid plot")
            sys.exit(13)

        # data
        f = cdms2.open(os.path.join(vcs.sample_data, self.testConfig[plot][0]))
        if typ == "vector":
            u = f(self.testConfig[plot][1][0])
            v = f(self.testConfig[plot][1][1])
            self.x.plot(u, v, gm, bg=False)
        elif plot.find("autot")>-1:
            s = f(self.testConfig[plot][1])
            self.x.plot(s, gm, bg=False, ratio="autot")
        else:
            s = f(self.testConfig[plot][1])
            self.x.plot(s, gm, bg=False)

        # Simulate a click -- VTK Specific
        location = self.testConfig[plot][2]
        i = self.x.backend.renWin.GetInteractor()
        i.SetEventInformation(location[0], location[1])
        i.LeftButtonPressEvent()

        fileName = "test_vcs_click_info_%s.png" % (typ)
        self.checkImage(fileName)

    def testClickInfo(self):
        self.testConfig = {
                'a_boxfill': ('clt.nc', 'clt', (200, 200)),
                'a_boxfill_autot': ('clt.nc', 'clt', (200, 200)),
                'a_mollweide_boxfill': ('clt.nc', 'clt', (222, 322)),
                'a_isofill': ('clt.nc', 'clt', (200, 200)),
                'a_isoline': ('clt.nc', 'clt', (200, 200)),
                'vector_default': ('clt.nc', ('u', 'v'), (200, 200)),
                'a_meshfill': ('sampleCurveGrid4.nc', 'sample', (222, 322)),
                'a_robinson_meshfill': ('sampleCurveGrid4.nc', 'sample', (222, 322)),
                }
        for src in self.testConfig.keys():
            self.clickInfo(src)
