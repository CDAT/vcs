#!/usr/bin/env bash
ls
pwd
export PATH=${HOME}/miniconda/bin:${PATH}
conda install -c uvcdat/label/testmesa -c uvcdat/label/nightly -c conda-forge -c uvcdat vtk-cdat cdutil genutil dv3d mesalib nose image-compare flake8 matplotlib
pip install dropbox
export UVCDAT_ANONYMOUS_LOG=False
python setup.py install --old-and-unmanageable
