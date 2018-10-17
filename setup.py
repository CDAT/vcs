
#  Usage:
#
#    python setup.py install
#
#
from setuptools import setup, find_packages
import os
from subprocess import Popen, PIPE
import cdat_info

Version = "8.0"
p = Popen(
    ("git",
     "describe",
     "--tags"),
    stdin=PIPE,
    stdout=PIPE,
    stderr=PIPE)
try:
    descr = p.stdout.readlines()[0].strip().decode("utf-8")
    Version = "-".join(descr.split("-")[:-2])
    if Version == "":
        Version = descr
except:
    descr = Version


setup(name="vcs",
      version=descr,
      description="Visualization and Control System",
      url="http://github.com/cdat/vcs",
      packages=find_packages(),
      #package_dir={'vcs': 'vcs'},
      scripts= ["scripts/vcs_download_sample_data"],
      zip_safe=True,
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
                                 'Share/mapper.js',
                                 'Share/cvi_tip_lib.js',
                                 'Share/tooltip.css',
                                 'Share/modal.js',
                                 'Share/test_data_files.txt')),
                  ('share/vcs/fonts', ('Fonts/Adelon_Regular.ttf',
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
                                       'Fonts/DejaVuSansCondensed.ttf'))
                  ]
)
