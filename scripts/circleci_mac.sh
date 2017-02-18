#!/usr/bin/env bash
PKG_NAME=cdms2
USER=uvcdat
wget https://repo.continuum.io/miniconda/Miniconda-latest-MacOSX-x86_64.sh -O miniconda.sh
export PATH="$HOME/miniconda/bin:$PATH"
bash miniconda.sh -b -p $HOME/miniconda
conda config --set always_yes yes --set changeps1 no
conda update -y -q conda
conda install -c conda-forge -c uvcdat uvcdat pyopenssl nose image-compare gcc
export UVCDAT_ANONYMOUS_LOG=False
vcs_download_sample_data
conda config --set anaconda_upload no
cd /git_repo
ls -l
python setup.py install --old-and-unmanageable
git clone git://github.com/uv-cdat/uvcdat-testdata
python run_tests.py -v2 -g

