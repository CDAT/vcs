#!/usr/bin/env bash
ls
pwd
export PATH=${HOME}/miniconda/bin:${PATH}
conda create -q -n py2 -c cdat/label/nightly -c conda-forge -c cdat cdms2 cdat_info udunits2 nose flake8 mesalib nose image-compare flake8 matplotlib image-compare genutil dv3d cdutil cdtime "proj4<5" "python<3" "numpy>1.14" 
conda create -q -n py3 -c cdat/label/nightly -c conda-forge -c cdat cdms2 nose flake8 cdat_info udunits2 mesalib nose image-compare flake8 matplotlib image-compare genutil dv3d cdutil cdtime nbsphinx easydev "proj4<5" "python>3" "numpy>1.14" 
export UVCDAT_ANONYMOUS_LOG=False
source activate py2
python setup.py install --old-and-unmanageable
source activate py3
python setup.py install --old-and-unmanageable
