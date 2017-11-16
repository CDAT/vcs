import basevcstest
import filecmp
import os
import vcs


class TestVCSContinents(basevcstest.VCSBaseTest):
    def testContinents(self):

        # Load the clt data:
        clt = self.clt("clt", time="1979-1-1", squeeze=1)

        # Zero out the array so we can see the continents clearly
        clt[:] = 0

        # Create and plot quick boxfill with default settings:
        boxfill = self.x.createboxfill()
        # Change the type
        boxfill.boxfill_type = 'custom'
        # Set levels to ignore 0
        boxfill.levels = [1, 100]
        # Pick a color, any color
        boxfill.fillareacolors = [242]

        dataonly = self.x.createtemplate()
        dataonly.blank()
        dataonly.data.priority = 1

        line_styles = ['long-dash', 'dot', 'dash', 'dash-dot', 'solid']

        self.x.scriptrun(
            os.path.join(
                os.path.dirname(__file__),
                "share",
                "test_vcs_continents.json"))

        for i in range(12):
            cont_index = i % 6 + 1
            cont_line = self.x.createline()
            cont_line.width = i % 3 + 1
            cont_line.type = line_styles[i % 5]
            cont_line.color = i + 200
            col = i % 3
            row = i / 3
            template = self.x.gettemplate("%i_x_%i_1" % (col, row))
            if cont_index != 3 and i != 4 and i != 11:
                self.x.plot(
                    clt,
                    template,
                    boxfill,
                    continents=cont_index,
                    continents_line=cont_line,
                    bg=self.bg)
            elif cont_index == 3:
                self.x.setcontinentsline(cont_line)
                self.x.setcontinentstype(3)
                self.x.plot(clt, template, boxfill, bg=self.bg)
            elif i == 4:
                self.x.setcontinentstype(0)
                # Make sure absolute path works
                path = os.path.join(
                    vcs.prefix, "share", "vcs", "data_continent_political")
                self.x.plot(
                    clt,
                    template,
                    boxfill,
                    continents=path,
                    continents_line=cont_line,
                    bg=self.bg)
            elif i == 11:
                # Make sure the dotdirectory other* works
                dotdir = vcs.getdotdirectory()
                current_dotdir = os.environ.get(dotdir[1], dotdir[0])
                os.environ["UVCDAT_DIR"] = os.path.join(
                    vcs.prefix, "share", "vcs")
                # Should pick up the other7 continents
                self.x.plot(
                    clt,
                    template,
                    boxfill,
                    continents=7,
                    continents_line=cont_line,
                    bg=self.bg)
                os.environ["UVCDAT_DIR"] = current_dotdir

        self.checkImage("test_vcs_continents.png", threshold=12)
