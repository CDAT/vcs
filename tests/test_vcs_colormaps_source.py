import basevcstest
import vcs
import os
import cdms2

class TestVCSColormap(basevcstest.VCSBaseTest):
    def testColormapSource(self):
        for gm in ["boxfill","isofill","meshfill","isoline","vector"]:
            for src in ["vcs","canvas","gm"]:
                self.colormapSource(gm,src)

    def colormapSource(self,gm_type="boxfill",src="vcs"):

        # Makes sure we have regular default values"
        self.x.clear()
        self.x.colormap = None
        vcs._colorMap = "viridis"
        exec("gm = self.x.create%s()" % gm_type)

        if src == "vcs":
          vcs._colorMap = "blue2green"
        elif src == "canvas":
          ## Still setting vcs to make sure it is not used
          vcs._colorMap = "blue2green"
          self.x.setcolormap("blue2grey")
        else:
          ## Still setting vcs and canvas to make sure it is not used
          vcs._colorMap = "blue2green"
          self.x.setcolormap("blue2grey")
          gm.colormap = "blue2orange"

        if gm_type != "meshfill":
          f=self.clt
          if gm_type == "vector":
            u = f("u")[...,::2,::2]
            v = f("v")[...,::2,::2]
            gm.scale = 8.
          else:
            s=f("clt",slice(0,1))
        else:
          f=cdms2.open(os.path.join(vcs.sample_data,'sampleCurveGrid4.nc'))
          s=f("sample")
        if gm_type == "vector":
          self.x.plot(u,v,gm,bg=self.bg)
        else:
          self.x.plot(s,gm,bg=self.bg)

        fnm = "test_vcs_colormaps_source_%s_%s.png" % (gm_type,src)
        self.checkImage(fnm)
