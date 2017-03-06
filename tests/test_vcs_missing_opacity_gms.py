import basevcstest
import cdms2
import vcs

class TestVCSPatterns(basevcstest.VCSBaseTest):
    def testOpacity(self):
        clt = self.clt("clt")
        for gm_type in ["boxfill","isofill","meshfill"]:

            # Plot the dataset
            self.x.clear()
            self.x.plot(clt, bg=self.bg)

            # Mask values
            masked = cdms2.MV2.masked_greater(clt, 50.)
            gm = vcs.creategraphicsmethod(gm_type, "default")

            # Set the missing color and opacity
            gm.missing = [50., 50., 50., 50.]

            # Plot the masked values
            self.x.plot(masked, gm, bg=self.bg)

            # Write to png file
            fnm = "test_vcs_missing_opacity_%s.png" % gm_type.lower()
            self.checkImage(fnm)


