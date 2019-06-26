import basevcstest
import cdms2
import cdat_info
import os
import vcs


class TestPickFrame(basevcstest.VCSBaseTest):
    def testBoxfillPickFrame(self):
        f = cdms2.open(os.path.join(cdat_info.get_sampledata_path(), "ta_ncep_87-6-88-4.nc"))
        ta = f("ta")
        u = self.clt("u")
        v = self.clt("v")

        f = cdms2.open(os.path.join(cdat_info.get_sampledata_path(), "sampleCurveGrid4.nc"))
        mesh = f("sample")
        grd = mesh.getGrid()
        sh = list(mesh.shape)
        print("NESFG SHAPE:",sh)
        sh.insert(0,12)
        axes = mesh.getAxisList()
        mesh = cdms2.MV2.resize(mesh, sh)
        mesh.setGrid(grd)
        ax = mesh.getAxis(0)
        ax.units = "months since 2019"
        ax.id = "time"
        ax.designateTime()
        for i, ax in enumerate(axes):
            mesh.setAxis(1+i, ax)
        mesh[3] = mesh[3]*3.
        gm_types = ["vector", "streamline", "meshfill", "1d", "boxfill", "isofill"]
        for gm_type in gm_types:
            # skip first time and second level on second time
            gm = vcs.getgraphicsmethod(gm_type)
            if gm_type in ["vector", "streamline"]:
                data1 = u
                data2 = v
                frame = 1
            elif gm_type == "meshfill":
                data1 = mesh
                data2 = None
                frame = 3
            else:
                data1 = ta
                data2 = None
                frame = 43
                if gm_type == "1d":
                    frame = 193
                elif gm_type == "isofill":
                    frame = -1
            self.x.clear()
            self.x.plot(data1, data2, gm, frame=frame, bg=self.bg)
            self.checkImage("test_vcs_pick_frame_{}.png".format(gm_type))
