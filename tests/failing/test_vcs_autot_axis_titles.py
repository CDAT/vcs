import basevcstest
import vcs
import cdms2

class TestVCSAutot(basevcstest.VCSBaseTest):
    def autotAxisTitle(self,plot,bg,x_over_y):

        testConfig = {'a_boxfill': ('clt.nc', 'clt'),
                      'a_mollweide_boxfill': ('clt.nc', 'clt'),
                      'a_meshfill': ('sampleCurveGrid4.nc', 'sample',),
                      'a_robinson_meshfill': ('sampleCurveGrid4.nc', 'sample'),
                      'a_lambert_isofill': ('clt.nc', 'clt'),
                      'a_robinson_isoline': ('clt.nc', 'clt')}

        # Tests if ratio=autot works correctly for background and foreground plots
        print "XOVERY",x_over_y
        if (x_over_y == 0.5):
            xSize = 250
            ySize = 500
            print "good size"
        else:
            xSize = 800
            ySize = 400
            print "other size"

        f = cdms2.open(vcs.sample_data + "/" + testConfig[plot][0])
        s = f(testConfig[plot][1])
        print "BG GOE:",bg,{"width":xSize, "height":ySize}
        x = vcs.init(bg=bg, geometry={"width":xSize, "height":ySize})
        x.drawlogooff()
        x.setantialiasing(0)

        # graphics method
        if (plot.find('boxfill') != -1):
            gm = x.getboxfill(plot)
        elif (plot.find('meshfill') != -1):
            gm = x.getmeshfill(plot)
        elif (plot.find('isofill') != -1):
            gm = x.getisofill(plot)
        elif (plot.find('isoline') != -1):
            gm = x.getisoline(plot)

        x.plot(s, gm, ratio="autot")
        name = "test_vcs_autot_axis_titles_" + plot[2:] + "_" + str(x_over_y) + "_" + str(bg) + ".png"
        self.x = x
        self.checkImage(name)

    def testAutotAxisTitle(self):
        for x_over_y in [0.5,2]:
            for plot in "a_boxfill a_mollweide_boxfill a_robinson_meshfill a_lambert_isofill a_robinson_isoline".split():
                for mode in [0,1]:
                    self.autotAxisTitle(plot,mode,x_over_y)
