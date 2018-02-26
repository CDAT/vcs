import basevcstest
import vcs

import numpy


class TestVCSAxisConvert(basevcstest.VCSBaseTest):
    def testAxisConvert(self):
        gm = vcs.create1d()
        gm.yaxisconvert = "log10"
        data = numpy.arange(10)
        self.x.plot(numpy.power(10,data), gm, bg=self.bg)
        self.checkImage("test_vcs_yaxisconvert_log10.png")

        self.x.clear()
        gm.flip = True
        gm.yaxisconvert = "linear"
        gm.xaxisconvert="log10"
        self.x.plot(numpy.power(10,data), gm, bg=self.bg)
        self.checkImage("test_vcs_xaxisconvert_log10_flip.png")

        self.x.clear()
        gm.flip = False
        gm.xaxisconvert = "linear"
        gm.yaxisconvert="ln"
        self.x.plot(numpy.exp(data), gm, bg=self.bg)
        self.checkImage("test_vcs_yaxisconvert_ln.png")

        self.x.clear()
        gm.flip = False
        gm.xaxisconvert="area_wt"
        gm.yaxisconvert = "linear"
        data2 = self.clt("clt",time=slice(0,1), longitude=slice(23,24), squeeze=1)
        self.x.plot(data2, gm, bg=self.bg)
        self.checkImage("test_vcs_xaxisconvert_areawt.png")

        self.x.clear()
        gm.flip = True
        gm.yaxisconvert="area_wt"
        gm.xaxisconvert = "linear"
        self.x.plot(data2, gm, bg=self.bg)
        self.checkImage("test_vcs_yaxisconvert_areawt_flip.png")

        
        self.x.clear()
        gm.flip = False
        gm.xaxisconvert="log10"
        gm.yaxisconvert = "ln"
        self.x.plot(numpy.power(10,data), numpy.exp(data), gm, bg=self.bg)
        self.checkImage("test_vcs_axisconvert_log10_ln.png")
        
        self.x.clear()
        #gm.flip = True
        data2[:] = numpy.power(10,numpy.arange(1, data2.shape[0]+1))
        data2 = data2[:10]
        gm.xaxisconvert = "area_wt"
        gm.yaxisconvert="log10"
        self.x.plot(data2 , gm, bg=self.bg)
        self.checkImage("test_vcs_axisconvert_area_log10.png")
        
        self.x.clear()
        gm.flip = True
        gm.yaxisconvert = "area_wt"
        gm.xaxisconvert="log10"
        self.x.plot(data2 , gm, bg=self.bg)
        self.checkImage("test_vcs_axisconvert_area_log10_flip.png")
        
        self.x.clear()
        gm.flip = False
        gm.xaxisconvert = "area_wt"
        gm.yaxisconvert="log10"
        self.x.plot(data2.getAxis(0)[:], data2 , gm, bg=self.bg)
        self.checkImage("test_vcs_axisconvert_area_log10_2arrays.png")
        
        with self.assertRaises(RuntimeError):
            self.x.clear()
            gm.flip = True
            self.x.plot(data2.getAxis(0)[:], data2 , gm, bg=self.bg)
        
        self.x.clear()
        gm.flip = False
        gm.xaxisconvert = "area_wt"
        gm.yaxisconvert="log10"
        gm.xticlabels1 = { -90:"90S", -80:"80S", -70:"70S", -60:"60S"}
        gm.xticlabels2 = { -85:"85S", -75:"75S", -65:"65S", -55:"55S"}
        mtics = {}
        def func(x):
            mtics[x]=""

        map(func, range(-90,-40,10))
        gm.xmtics2 = mtics
        mtics = {}
        map(func, range(-85,-40,10))
        gm.xmtics1 = mtics

        gm.yticlabels1 = {100:"hun"}
        gm.yticlabels2 = {1000:"thou"}
        gm.ymtics1 = {10:"",1000:""}
        gm.ymtics2 = {10000:"",1000:""}
        gm.list()
        tmpl = vcs.createtemplate()
        for num in ["1", "2"]:
            for loc in ["x", "y"]:
                for attr in ["mintic", "tic"]:
                    filled_attr = "{}{}{}".format(loc,attr,num)
                    print("PRIO FOR ATT:",filled_attr)
                    obj = getattr(tmpl,filled_attr)
                    obj.priority=1
                    obj.list()
        tmpl.xlabel1.priority=1
        tmpl.xlabel2.priority=1
        tmpl.ylabel1.priority=1
        tmpl.ylabel2.priority=1
        self.x.plot(data2.getAxis(0)[:], data2 , gm, tmpl, bg=self.bg)
        self.checkImage("test_vcs_axisconvert_area_log10_user_labels.png")
