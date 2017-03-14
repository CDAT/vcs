import basevcstest
import vcs
import cdms2
import os

class TestVCSHatch(basevcstest.VCSBaseTest):
    def gmPatternHatch(self,gm_type="isofill",fill_style="pattern",
            projtype="default",lat1=-90,lat2=90,lon1=-180,lon2=180,contig=True):


        self.x.setcolormap("classic")

        gm = vcs.creategraphicsmethod(gm_type, "default")
        if projtype != "default":
            p = vcs.createprojection()
            try:
                ptype = int(projtype)
            except:
                ptype = projtype
            p.type = ptype
            gm.projection = p

        if contig:
            gm.levels = [220, 230, 240, 250, 260, 270, 280, 290, 300, 310, 320]
        else:
            gm.levels = [[230,235],[240,245],[250,255],[260,265],[270,275],
                         [280,285],[290,295],[300,305],[310,315],[320,325]]
        gm.fillareastyle = fill_style
        gm.fillareacolors = [242, 244, 237, 248, 250, 252, 44, 243, 139, 247]
        if fill_style == "hatch":
            gm.fillareaindices = [2, 4, 6, 8, 10, 12, 14, 16, 18, 20]
            gm.fillareaopacity = [50, 75, 20, 100, 25, 30, 40, 80, 60, 100]
        else:
            gm.fillareaindices = [1, 3, 5, 7, 9, 11, 18, 15, 17, 19]
            gm.fillareaopacity = [50, 75, 20, 0, 25, 30, 100, 0, 60, 0]

        if gm_type == "boxfill":
            gm.boxfill_type = "custom"

        if gm_type == "meshfill":
            gm.mesh = True

        nm_xtra = ""
        xtra = {}
        if lat1 != lat2:
            gm.datawc_y1 = lat1
            gm.datawc_y2 = lat2
            xtra["latitude"] = (lat1, lat2)
            if lat1 < 0:
                nm_xtra += "_SH"
            else:
                nm_xtra += "_NH"
        if lon1 != lon2:
            xtra["longitude"] = (lon1, lon2)
            nm_xtra += "_%i_%i" % (lon1, lon2)
        if not contig:
            nm_xtra += "_non-contig"

        xtra["time"] = slice(0, 1)
        xtra["squeeze"] = 1
        f = cdms2.open(os.path.join(vcs.sample_data, 'tas_ccsr-95a_1979.01-1979.12.nc'))
        s = f("tas", **xtra)
        f.close()
        self.x.clear()
        self.x.plot(s, gm, bg=self.bg)
        fnm = "test_vcs_%s_%s" % (gm_type.lower(), fill_style.lower())
        if projtype != "default":
            fnm += "_%s_proj" % projtype
        fnm += nm_xtra
        self.checkImage(fnm+".png")

    def testHatchPatterns(self):
        for gm in ["boxfill","isofill","meshfill"]:
            for style in ["solid","pattern","hatch"]:
                self.gmPatternHatch(gm_type=gm,fill_style=style,contig=False)
                self.gmPatternHatch(gm_type=gm,fill_style=style,contig=True)
                self.gmPatternHatch(gm_type=gm,fill_style=style,lon1=0,lon2=360)


