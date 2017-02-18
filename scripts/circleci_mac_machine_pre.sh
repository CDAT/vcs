#!/usr/bin/env bash
export PATH=${HOME}/miniconda2/bin:${PATH}
echo "Trying to upload conda"
conda update -y -q conda
conda install -c conda-forge -c uvcdat uvcdat-nox pyopenssl nose image-compare
vcs_download_sample_data
conda config --set anaconda_upload no
