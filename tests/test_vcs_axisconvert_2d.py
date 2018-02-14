import basevcstest
import vcs
import cdms2
import numpy


class TestVCSAxisConvert(basevcstest.VCSBaseTest):
    def axisConvertGmLog10Areawt(self, method):
        f = cdms2.open(vcs.sample_data+"/ta_ncep_87-6-88-4.nc")
        data = f("ta", time=slice(0,1), longitude=(12,12,'cob'), squeeze=1)
        self.axisConvertGm(data, method, 'area_wt', 'log10')

    def axisConvertGmLog10(self, method):
        f = cdms2.open(vcs.sample_data+"/ta_ncep_87-6-88-4.nc")
        data = f("ta", longitude=(12,12,'cob'), latitude=(12, 12, 'cob'), squeeze=1)
        self.axisConvertGm(data, method, 'log10', 'linear')

    def axisConvertGmAreaWt(self, method):
        data = self.clt("clt")
        self.axisConvertGm(data, method, 'linear', 'area_wt')

    def axisConvertGm(self, data, method, xconvert, yconvert):
        gm = method()
        gm.xaxisconvert = xconvert
        gm.yaxisconvert = yconvert
        self.x.clear()
        self.x.plot(data,gm)
        self.checkImage("test_vcs_axisconvert_{}_{}_{}.png".format(gm.g_name, xconvert, yconvert))

    def test_areawt(self):
        for method in [
                vcs.createboxfill,
                vcs.createisofill,
                       ]:
            self.axisConvertGmAreaWt(method)
            self.axisConvertGmLog10(method)
            self.axisConvertGmLog10Areawt(method)
