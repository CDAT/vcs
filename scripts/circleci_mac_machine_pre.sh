#!/usr/bin/env bash
curl https://repo.continuum.io/miniconda/Miniconda2-latest-MacOSX-x86_64.sh -o miniconda.sh
bash miniconda.sh -b -p $HOME/miniconda
export PATH=${HOME}/miniconda/bin:${PATH}
conda config --set always_yes yes --set changeps1 no
conda update -y -q conda
conda install -c conda-forge -c uvcdat uvcdat pyopenssl nose image-compare
vcs_download_sample_data
conda config --set anaconda_upload no
