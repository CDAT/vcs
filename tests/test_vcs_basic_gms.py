import basevcstest
import vcs
import MV2
import cdms2
import os


class TestVCSBasicGms(basevcstest.VCSBaseTest):
    def basicGm(self, gm_type, projtype="default", lat1=0, lat2=0, lon1=0, lon2=0,
                rg=False, flip=False, zero=False, transparent=False, mask=False, bigvalues=False):

        self.x.clear()
        self.x.setcolormap(None)
        cdms2.tvariable.TransientVariable.variable_count = 1
        loc = locals()
        exec("gm=vcs.create%s()" % gm_type)
        gm = loc["gm"]
        if projtype != "default":
            p = vcs.createprojection()
            try:
                ptype = int(projtype)
            except BaseException:
                ptype = projtype
            p.type = ptype
            gm.projection = p
        nm_xtra = ""
        xtra = {}
        if lat1 != lat2:
            if rg:
                if flip:
                    gm.datawc_y1 = lat2
                    gm.datawc_y2 = lat1
                    nm_xtra += "_gmflip"
                else:
                    gm.datawc_y1 = lat1
                    gm.datawc_y2 = lat2
            xtra["latitude"] = (lat1, lat2)
            if lat1 < 0:
                nm_xtra += "_SH"
            else:
                nm_xtra += "_NH"
        if lon1 != lon2:
            if rg:
                gm.datawc_x1 = lon1
                gm.datawc_x2 = lon2
            xtra["longitude"] = (lon1, lon2)
            nm_xtra += "_%i_%i" % (lon1, lon2)
        if rg:
            nm_xtra += "_via_gm"
        if gm_type == "meshfill":
            f = cdms2.open(
                os.path.join(
                    vcs.sample_data,
                    'sampleCurveGrid4.nc'))
        else:
            f = self.clt
        if gm_type == "vector":
            u = f("u", **xtra)
            v = f("v", **xtra)
            if mask:
                u = MV2.masked_greater(u, 58.)
            if zero:
                u -= u
                v -= v
        elif gm_type == "meshfill":
            s = f("sample", **xtra)
            if mask:
                s = MV2.masked_less(s, 1150.)
            elif bigvalues:
                s[s < 1150] = 1e40
            if zero:
                s -= s
        else:
            s = f("clt", **xtra)
            if mask:
                s = MV2.masked_greater(s, 78.)
            elif bigvalues:
                s[s > 78] = 1e40
            if gm_type in ["1d", "yxvsx", "xyvsy", "xvsy", "scatter"]:
                s = s(
                    latitude=(
                        20, 20, "cob"), longitude=(
                        112, 112, "cob"), squeeze=1)
                s2 = MV2.sin(s)
                if zero:
                    s2 -= s2
            if zero:
                s -= s

        if bigvalues:
            gm.levels = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 1.e36]

        if transparent:
            cmap = self.x.createcolormap()
            for i in range(256):  # tweaks all colors
                cmap.setcolorcell(i, 100., 0, 0, i / 2.55)
            self.x.setcolormap(cmap)
            if gm_type == "vector":
                gm.linecolor = [100, 0, 0, 50.]
            elif gm_type in ["yxvsx", "xyvsy", "yvsx", "scatter", "1d"]:
                gm.linecolor = [100, 0, 0, 50.]
                gm.markercolor = [100, 0, 0, 50.]

        if gm_type == "vector":
            gm.scale = 4.
            self.x.plot(u, v, gm, bg=self.bg)
        elif gm_type in ["scatter", "xvsy"]:
            self.x.plot(s, s2, gm, bg=self.bg)
        else:
            self.x.plot(s, gm, bg=self.bg)
        fnm = "test_vcs_basic_%s" % gm_type.lower()
        if mask:
            fnm += "_masked"
        elif bigvalues:
            fnm += "_bigvalues"
        if projtype != "default":
            fnm += "_%s_proj" % projtype
        if zero:
            fnm += "_zero"
        if transparent:
            fnm += "_transparent"
        fnm += nm_xtra
        self.checkImage(fnm + '.png', threshold=20)

    def testBasicGms(self):
        for gm in "boxfill isofill isoline meshfill".split():
            for proj in [0, -3, "aeqd"]:
                self.basicGm(gm, proj, mask=True)
                self.basicGm(gm, proj, lat1=-90, lat2=0)
                self.basicGm(gm, proj, lat1=-90, lat2=0, rg=True)
                self.basicGm(gm, proj, lat1=-90, lat2=0, lon1=-180, lon2=180)
                self.basicGm(
                    gm,
                    proj,
                    lat1=-90,
                    lat2=0,
                    lon1=-180,
                    lon2=180,
                    rg=True)
                self.basicGm(gm, proj, lat1=-90, lat2=0, lon1=0, lon2=360)
                self.basicGm(
                    gm,
                    proj,
                    lat1=-90,
                    lat2=0,
                    lon1=0,
                    lon2=360,
                    rg=True)
                self.basicGm(gm, proj, lat1=90, lat2=0)
                self.basicGm(gm, proj, lat1=90, lat2=0, rg=True)
                self.basicGm(gm, proj, lat1=90, lat2=0, rg=True, flip=True)
        self.basicGm("isofill", bigvalues=True)
