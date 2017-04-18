#!/usr/bin/env bash
ls
pwd
export PATH=${HOME}/miniconda/bin:${PATH}
conda install -c uvcdat/label/nightly -c conda-forge -c uvcdat uvcdat pyopenssl nose image-compare flake8 "mesalib<8"
pip install dropbox
conda install --force -c uvcdat/label/testmesa -c conda-forge -c uvcdat vtk-cdat-nox
export UVCDAT_ANONYMOUS_LOG=False
python setup.py install --old-and-unmanageable
