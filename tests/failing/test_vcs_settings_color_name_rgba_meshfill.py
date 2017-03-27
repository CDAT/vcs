import basevcstest
import cdms2
import os
import vcs

class TestVCSColorsMeshfill(basevcstest.VCSBaseTest):
    def test_ColorRGBAMeshfill(self):
        f=cdms2.open(os.path.join(vcs.sample_data,"sampleCurveGrid4.nc"))
        data=f("sample")
        gm = self.x.createmeshfill()
        gm.levels = range(0,1501,150)
        gm.fillareacolors = ["green","red","blue","bisque","yellow","grey",
                [100,0,0,50], [0,100,0],"salmon",[0,0,100,75]]
        self.x.plot(data,gm,bg=self.bg)
        self.checkImage(x, 'test_vcs_settings_color_name_rgba_meshfill.png')
