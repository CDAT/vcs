#!/usr/bin/env bash
ls
pwd
export PATH=${HOME}/miniconda/bin:${PATH}
conda create -n py3 -c uvcdat/label/nightly -c nadeau1  -c conda-forge -c uvcdat cdms2 nose flake8 "python>3" cdat_info udunits2 dv3d mesalib nose image-compare flake8 "matplotlib<2.1" numpy=1.13
conda create -n py2 -c uvcdat/label/nightly -c conda-forge -c uvcdat cdms2 cdat_info udunits2 nose flake8 dv3d mesalib nose image-compare flake8 "matplotlib<2.1" numpy=1.13
export UVCDAT_ANONYMOUS_LOG=False
source activate py2
mkdir gits
cd gits ; git clone git://github.com/uv-cdat/cdms ; cd cdms ; git checkout remove_string_module ; python setup.py install; cd ../..
cd gits ; git clone git://github.com/uv-cdat/cdutil ; cd cdutil ; git checkout py3 ; python setup.py install; cd ../..
cd gits ; git clone git://github.com/uv-cdat/dv3d ; cd dv3d ; git checkout py3 ; python setup.py install; cd ../..
source activate py3
cd gits ; cd cdms ; rm -rf build ; python setup.py install; cd ../..
cd gits ; cd cdutil ; rm -rf build ; python setup.py install; cd ../..
cd gits ; cd dv3d ; rm -rf build ; python setup.py install; cd ../..
source activate py2
python setup.py install --old-and-unmanageable
source activate py3
python setup.py install --old-and-unmanageable
