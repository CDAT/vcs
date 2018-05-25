
import basevcstest
import numpy
import MV2


class TestVCSFonts(basevcstest.VCSBaseTest):
    def test_project_font(self):
        bot = self.x.gettemplate("bot_of2")
        top = self.x.gettemplate("top_of2")
        gm = self.x.createisoline()
        gm.datawc_x1 = -180
        gm.datawc_x2 = 180
        gm.datawc_y1 = -90
        gm.datawc_y2 = 90
        self.x.plot(self.clt("clt", slice(0,1)),gm,top)
        proj = "polar"
        gm.projection = proj
        self.x.plot(self.clt("clt",slice(0,1),longitude=(-180,181)),gm,bot)
        txt = self.x.createtext()
        txt.string = "Non proj"
        txt.worldcoordinate = [-180,180,-90,90]
        txt.x = -30
        txt.y = 80
        txt.color="blue"
        txt.height = 15
        txt.halign = "center"
        txt.viewport = top.data.x1, top.data.x2, top.data.y1, top.data.y2
        self.x.plot(txt)
        txt.projection = proj
        txt.color = "red"
        txt.string = "PROJECTED"
        txt.viewport = bot.data.x1, bot.data.x2, bot.data.y1, bot.data.y2
        self.x.plot(txt)
        fnm = "test_vcs_font_projection.png"
        self.checkImage(fnm)


