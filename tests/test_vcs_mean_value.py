import basevcstest
import cdms2
import MV2
import genutil
import cdutil
import vcs
import os
import requests


class TestVCSMeanValue(basevcstest.VCSBaseTest):
    def test_MeanValue(self):
        # Download data
        filename = 'tas_Amon_IPSL-CM5A-LR_1pctCO2_r1i1p1_185001-198912.nc'
        if not os.path.exists(filename):
            r = requests.get(
                "https://cdat.llnl.gov/cdat/sample_data/notebooks/{}".format(filename), stream=True)
            with open(filename, "wb") as f:
                for chunk in r.iter_content(chunk_size=1024):
                    if chunk:  # filter local_filename keep-alive new chunks
                        f.write(chunk)
        
        # Open data file and extract variable
        f = cdms2.open(filename)
        data = f("tas")

        # Mask the data
        datamskd = MV2.masked_greater(data, data.max()-7)

        # extract the departures of the masked data.
        datamskd_departures = cdutil.times.ANNUALCYCLE.departures(datamskd)

        # create time series of the masked data departures.
        datamskd_departures_ts = genutil.averager(datamskd_departures, axis='xy', weights=[
                                                  'weighted', 'weighted'], combinewts=1)
        datamskd_departures_ts_corrected = cdutil.times.ANNUALCYCLE.departures(
            datamskd_departures_ts)

        # Graphics and plot steps
        template = vcs.createtemplate()
        self.x = vcs.init(bg=True, geometry=(1200, 900))

        # Plot image and check against reference
        self.x.clear()
        self.x.plot(datamskd_departures_ts_corrected, template)
        self.checkImage("test_vcs_mean_value_correct.png")
