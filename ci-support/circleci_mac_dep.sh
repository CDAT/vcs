#!/usr/bin/env bash
ls
pwd
export PATH=${HOME}/miniconda/bin:${PATH}
conda create -q -n py3 -c uvcdat/label/nightly -c nesii/channel/dev-esmf  -c conda-forge -c uvcdat "cdms2>2.12.2018.02.06" nose flake8 "python>3" cdat_info udunits2 mesalib nose image-compare flake8 "matplotlib<2.1" numpy=1.13 image-compare genutil vtk-cdat "dv3d>2.12.2017" "cdutil>2.12.2017" "cdtime<2018" nbsphinx easydev
conda create -q -n py2 -c uvcdat/label/nightly -c conda-forge -c uvcdat "cdms2>2.12.2018.02.06" cdat_info udunits2 nose flake8 mesalib nose image-compare flake8 "matplotlib<2.1" numpy=1.13 image-compare genutil vtk-cdat "dv3d>2.12.2017" "cdutil>2.12.2017" "cdtime<2018" nbsphinx easydev
export UVCDAT_ANONYMOUS_LOG=False
source activate py2
python setup.py install --old-and-unmanageable
source activate py3
python setup.py install --old-and-unmanageable
