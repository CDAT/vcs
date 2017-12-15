import basevcstest
import cdms2
import os
import vcs
import MV2


class TestVCSAnimate(basevcstest.VCSBaseTest):
    def projected(self, gm_type, projtype="default"):
        s = None

        if gm_type == "meshfill":
            f = cdms2.open(
                os.path.join(
                    vcs.sample_data,
                    "sampleCurveGrid4.nc"))
            s2 = f("sample")

            s = MV2.resize(s2, (4, 32, 48))
            s.id = 'sample'
            t = cdms2.createAxis(list(range(4)))
            t.units = "months since 2015"
            t.id = "time"
            t.designateTime()
            s.setAxis(0, t)
            s.setAxis(1, s2.getAxis(0))
            s.setAxis(2, s2.getAxis(1))
            s.setGrid(s2.getGrid())
            for i in range(4):
                s[i] = s[i] * (1 + float(i) / 10.)
        else:
            # read only 12 times steps to speed up things
            s = self.clt("clt", slice(0, 12))

        gm = vcs.creategraphicsmethod(gm_type, "default")
        if projtype != "default":
            p = vcs.createprojection()
            try:
                ptype = int(projtype)
            except BaseException:
                ptype = projtype
            p.type = ptype
            gm.projection = p

        self.x.clear()
        self.x.plot(s, gm, bg=self.bg)
        self.x.animate.create()

        prefix = "test_vcs_animate_%s_%s" % (gm_type.lower(), projtype.lower())
        self.x.animate.save("%s.mp4" % prefix)
        # so we can look at them again
        pngs = self.x.animate.close(preserve_pngs=True)

        pdir = os.path.split(pngs[0])[0]
        p = os.path.join(pdir, "anim_0.png")
        src = os.path.join(
            self.basedir, "test_vcs_animate_projected_%s_%s.png" %
            (gm_type.lower(), projtype.lower()))
        self.checkImage(p, pngReady=True, src=src)
        for f in pngs:
            if os.path.isfile(f):
                os.remove(f)
        os.removedirs(pdir)
        os.remove("%s.mp4" % prefix)

    def testProjected(self):
        for gm_type in ["isofill", "meshfill", "boxfill"]:
            self.projected(gm_type=gm_type, projtype="robinson")
