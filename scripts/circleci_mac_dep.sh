#!/usr/bin/env bash
ls
pwd
export PATH=${HOME}/miniconda/bin:${PATH}
conda install -c conda-forge -c uvcdat uvcdat pyopenssl nose image-compare
pip install dropbox
export UVCDAT_ANONYMOUS_LOG=False
vcs_download_sample_data
python setup.py install --old-and-unmanageable
