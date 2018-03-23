#!/usr/bin/env bash
ls
pwd
export PATH=${HOME}/miniconda/bin:${PATH}
conda create -q -n py2 -c nesii/label/dev-esmf  -c conda-forge -c cdat/label/v80 vcs image-compare nose flake8 "python<3"
conda create -q -n py3 -c nesii/label/dev-esmf  -c conda-forge -c cdat/label/v80 vcs image-compare nose flake8 "python>3"
export UVCDAT_ANONYMOUS_LOG=False
git clone git://github.com/uv-cdat/uvcdat-testdata
cd uvcdat-testdata
git checkout v80
cd ..
