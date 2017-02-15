#!/usr/bin/env bash
PKG_NAME=cdms2
USER=uvcdat
export PATH=${HOME}/miniconda2/bin:${PATH}
echo "Trying to upload conda"
conda update -y -q conda
conda install -c conda-forge -c uvcdat uvcdat-nox pyopenssl nose image-compare
export UVCDAT_ANONYMOUS_LOG=False
vcs_download_sample_data
conda config --set anaconda_upload no
cd /git_repo
ls -l
python setup.py install --old-and-unmanageable
git clone git://github.com/uv-cdat/uvcdat-testdata
df -h
python run_tests.py
