import basevcstest
import os
import vcs
import cdms2
import numpy


class TestVCSAxisConvert(basevcstest.VCSBaseTest):
    def axisConvertGmLinear(self, method):
        method = method()
        f = cdms2.open(vcs.sample_data+"/ta_ncep_87-6-88-4.nc")
        data = f("ta", longitude=(12,12,'cob'), latitude=(12, 12, 'cob'), squeeze=1)
        if isinstance(method, vcs.vector.Gv) or \
           isinstance(method, vcs.streamline.Gs):
            data = self.clt("u")
            data2 = self.clt("v")
        else:
            data2 = None
        self.axisConvertGm(data, data2, method, 'linear', 'linear')

    def axisConvertGmLog10Areawt(self, method):
        method = method()
        f = cdms2.open(vcs.sample_data+"/ta_ncep_87-6-88-4.nc")
        data = f("ta", time=slice(0,1), longitude=(12,12,'cob'), squeeze=1)
        if isinstance(method, vcs.vector.Gv) or \
           isinstance(method, vcs.streamline.Gs):
            data2 = data
        else:
            data2 = None
        self.axisConvertGm(data, data2, method, 'area_wt', 'log10')

    def axisConvertGmLog10(self, method):
        method = method()
        f = cdms2.open(vcs.sample_data+"/ta_ncep_87-6-88-4.nc")
        data = f("ta", longitude=(12,12,'cob'), latitude=(12, 12, 'cob'), squeeze=1)
        if isinstance(method, vcs.vector.Gv) or \
           isinstance(method, vcs.streamline.Gs):
            data2 = data
        else:
            data2 = None
        self.axisConvertGm(data, data2, method, 'log10', 'linear')

    def axisConvertGmAreaWt(self, method):
        method = method()
        if isinstance(method, vcs.vector.Gv) or \
           isinstance(method, vcs.streamline.Gs):
            data = self.clt("u")
            data2 = self.clt("v")
        elif isinstance(method, vcs.meshfill.Gfm):
            data = cdms2.open(os.path.join(vcs.sample_data,"sampleCurveGrid4.nc"))("sample")
            data2 = None
        else:
            data = self.clt("clt")
            data2 = None
        self.axisConvertGm(data, data2, method, 'linear', 'area_wt')

    def axisConvertGm(self, data, data2, gm, xconvert, yconvert):
        gm.xaxisconvert = xconvert
        gm.yaxisconvert = yconvert
        self.x.clear()
        if data2 is None:
            self.x.plot(data, gm)
        else:
            self.x.plot(data, data2, gm)
        self.checkImage("test_vcs_axisconvert_{}_{}_{}.png".format(gm.g_name, xconvert, yconvert))

    def test_areawt(self):
        for method in [
                vcs.createboxfill,
                vcs.createisofill,
                vcs.createisoline,
                vcs.createmeshfill,
                vcs.createvector,
                vcs.createstreamline,
                       ]:
            self.axisConvertGmAreaWt(method)
            if not method in [vcs.createmeshfill,]:
                self.axisConvertGmLinear(method)
                self.axisConvertGmLog10(method)
                self.axisConvertGmLog10Areawt(method)
