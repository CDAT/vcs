import basevcstest
import os
import vcs
import cdms2
import random
### Moving this to failing
# the random statement seem to indicate that the test should fail once in a while, diff should not be 0
# I think

class TestVCSIsolines(basevcstest.VCSBaseTest):
    def testIsolineLabelBackground(self):

        (latmin, latmax, lonmin, lonmax) = (-90, 90, -180, 180)
        dataset = cdms2.open(os.path.join(vcs.sample_data, "tas_cru_1979.nc"))
        data = dataset("tas", time=slice(0, 1), latitude=(latmin, latmax),
                       longitude=(lonmin, lonmax, 'co'), squeeze=1)
        dataset.close()

        self.x.backgroundcolor = [100, 105, 105]

        isoline = self.x.createisoline()
        isoline.label = "y"
        texts = []
        colors = []
        bcolors = []
        bopacities = []
        for i in range(10):
            text = self.x.createtext()
            random.seed(i*200)
            text.color = random.randint(1, 255)
            text.height = 12
            random.jumpahead(i * 100)
            colors.append(random.randint(1, 255))
            random.jumpahead(i * 20)
            bcolors.append(random.randint(1, 255))
            bopacities.append(random.randint(0, 100))
            if i % 2 == 0:
                texts.append(text.name)
            else:
                texts.append(text)
        isoline.text = texts
        isoline.labelbackgroundcolors = bcolors
        isoline.labelbackgroundopacities = bopacities
        isoline.labelskipdistance = 15.0

        # First test using isoline.text[...].color
        self.x.plot(data, isoline, bg=self.bg)
        fnm = "test_vcs_isoline_labels_background.png"
        self.checkImage(fnm)
