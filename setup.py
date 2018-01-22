
#  Usage:
#
#    python setup.py install
#
#
from setuptools import setup, find_packages
import os

import cdat_info

setup(name="vcs",
      version=cdat_info.Version,
      description="Visualization and Control System",
      url="http://uvcdat.llnl.gov",
      packages=find_packages(),
      package_dir={'vcs': 'vcs'},
      scripts= ["scripts/vcs_download_sample_data"],
      data_files=[('share/vcs', ('Share/wmo_symbols.json',
                                 'Share/data_continent_coarse',
                                 'Share/data_continent_political',
                                 'Share/data_continent_river',
                                 'Share/data_continent_states',
                                 'Share/data_continent_other7',
                                 'Share/data_continent_fine',
                                 'Share/initial.attributes',
                                 'Share/cdat.png',
                                 'Share/marker_icon.png',
                                 'Share/text_icon.png',
                                 'Share/fill_icon.png',
                                 'Share/line_icon.png',
                                 'Share/sample_files.txt',
                                 'Share/test_data_files.txt',
                                 'Fonts/Adelon_Regular.ttf',
                                 'Fonts/Arabic.ttf',
                                 'Fonts/Athens_Greek.ttf',
                                 'Fonts/AvantGarde-Book_Bold.ttf',
                                 'Fonts/Chinese_Generic1.ttf',
                                 'Fonts/Clarendon.ttf',
                                 'Fonts/Courier.ttf',
                                 'Fonts/HelvMono.ttf',
                                 'Fonts/Russian.ttf',
                                 'Fonts/Times_CG_ATT.ttf',
                                 'Fonts/blex.ttf',
                                 'Fonts/blsy.ttf',
                                 'Fonts/hebrew.ttf',
                                 'Fonts/jsMath-msam10.ttf',
                                 'Fonts/jsMath-wasy10.ttf',
                                 'Fonts/DejaVu Fonts License.txt',
                                 'Fonts/DejaVuSans-Bold.ttf',
                                 'Fonts/DejaVuSans-BoldOblique.ttf',
                                 'Fonts/DejaVuSans-ExtraLight.ttf',
                                 'Fonts/DejaVuSans-Oblique.ttf',
                                 'Fonts/DejaVuSans.ttf',
                                 'Fonts/DejaVuSansCondensed-Bold.ttf',
                                 'Fonts/DejaVuSansCondensed-BoldOblique.ttf',
                                 'Fonts/DejaVuSansCondensed-Oblique.ttf',
                                 'Fonts/DejaVuSansCondensed.ttf',
                                 'Share/mapper.js',
                                 'Share/cvi_tip_lib.js',
                                 'Share/tooltip.css',
                                 'Share/modal.js'
                                 )), ],
      )
