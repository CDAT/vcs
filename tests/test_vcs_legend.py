import basevcstest
import cdms2
import vcs
import os

class TestVCSLegend(basevcstest.VCSBaseTest):
    def legend(self,gm_type,orientation,ext1,ext2):

        self.x.setcolormap("rainbow")
        exec("gm=self.x.create%s()" % gm_type)
        nm_xtra=""
        xtra = {'time':slice(0,1),'squeeze':1}
        if gm_type=="meshfill":
            f=cdms2.open(os.path.join(vcs.sample_data,'sampleCurveGrid4.nc'))
        else:
            f=self.clt
        if gm_type=="meshfill":
            s=f("sample")
        else:
            s=f("clt",**xtra)


        if gm_type=="boxfill":
            gm.level_1=20
            gm.level_2=80
            if ext1=="y":
                gm.ext_1="y"
            if ext2=="y":
                gm.ext_2="y"
        else:
            if gm_type=="isofill":
                levels = [20, 30, 40, 50, 60, 70, 80]
            else:
                levels = [300,500,800,1000,1200]
            gm.levels=levels
            if ext1=="y":
                gm.ext_1="y"
            if ext2=="y":
                gm.ext_2="y"
            gm.fillareacolors = vcs.getcolors(gm.levels)
        tmpl = self.x.createtemplate()
        if orientation=="vertical":
            tmpl.data.x2=.8
            tmpl.box1.x2=.8
            tmpl.ytic2.x1=.8
            tmpl.ytic2.x2=.815
            tmpl.legend.x1=.86
            tmpl.legend.x2=.9
            tmpl.legend.y1=.3
            tmpl.legend.y2=.8

        self.x.clear()
        self.x.plot(s,gm,tmpl,bg=self.bg)

        fnm = "test_vcs_legend_%s_%s_ext1_%s_ext2_%s.png" % (gm_type,orientation,ext1,ext2)
        self.checkImage(fnm)

    def testLegend(self):
        for gm in ["boxfill", "isofill", "meshfill"]:
            for ori in ["horizontal", "vertical"]:
                for ext1 in ["y","n"]:
                    for ext2 in ["y","n"]:
                        self.legend(gm,ori,ext1,ext2)

