#!/usr/bin/env bash
ls
pwd
export PATH=${HOME}/miniconda/bin:${PATH}
conda install -c uvcdat/label/testmesa -c uvcdat/label/nightly -c conda-forge -c uvcdat cdutil genutil dv3d-nox "mesalib>17" nose image-compare flake8
pip install dropbox
#conda install --force -c uvcdat/label/testmesa -c conda-forge -c uvcdat vtk-cdat-nox mesalib>17
export UVCDAT_ANONYMOUS_LOG=False
python setup.py install --old-and-unmanageable
