import basevcstest
import cdms2
import cdat_info
import os
import vcs


class TestVCSUpdateArray(basevcstest.VCSBaseTest):
    def testUpdateArray(self):
        f = cdms2.open(os.path.join(cdat_info.get_sampledata_path(),"ta_ncep_87-6-88-4.nc"))
        data = f("ta")
        levels = vcs.mkscale(*vcs.minmax(data))
        levels.insert(0, 1.e20)
        levels.append(1.e20)
        colors = vcs.getcolors(levels)
        isof = vcs.createisofill()
        isof.levels = levels
        isof.fillareacolors = colors
        isol = vcs.createisoline()
        isol.levels = levels
        tmpl = self.x.gettemplate("top_of2")
        self.x.portrait()
        self.x.plot(data, isof, tmpl)
        tmpl = self.x.gettemplate("bot_of2")
        disp = self.x.plot(data, isof, tmpl)
        kw = {"time": slice(3, 4), "level": slice(6, 7)}
        new = disp.array[0](**kw)
        self.x.backend.update_input(disp.backend, new)
        self.checkImage("test_vcs_update_array_extensions.png")
