#!/usr/bin/env bash
PKG_NAME=cdms2
USER=uvcdat
echo "Trying to upload conda"
if [ `uname` == "Linux" ]; then
    OS=linux-64
    echo "Linux OS"
    export PATH="$HOME/miniconda2/bin:$PATH"
    conda update -y -q conda
else
    echo "Mac OS"
    OS=osx-64
fi

mkdir ~/conda-bld
conda config --set anaconda_upload no
export CONDA_BLD_PATH=${HOME}/conda-bld
export VERSION=`date +%Y.%m.%d`
echo "Cloning recipes"
git clone git://github.com/UV-CDAT/conda-recipes
cd conda-recipes
# uvcdat creates issues for build -c uvcdat confises package and channel
rm -rf uvcdat
python ./prep_for_build.py -v `date +%Y.%m.%d`
conda build vcs -c conda-forge -c uvcdat 
anaconda -t $CONDA_UPLOAD_TOKEN upload -u $USER -l nightly $CONDA_BLD_PATH/$OS/$PKG_NAME-`date +%Y.%m.%d`-py27_0.tar.bz2 --force
if [ "${TRAVIS_OS_NAME}" = "linux" ]; then
    python ./prep_for_build.py -v `date +%Y.%m.%d` -f nox
    conda build vcs -c conda-forge -c uvcdat 
    anaconda -t $CONDA_UPLOAD_TOKEN upload -u $USER -l nightly $CONDA_BLD_PATH/$OS/$PKG_NAME-nox-`date +%Y.%m.%d`-py27_0.tar.bz2 --force
fi



python ./prep_for_build.py -v `date +%Y.%m.%d`
echo "Building now"
conda build -c conda-forge -c uvcdat vcs
anaconda -t $CONDA_UPLOAD_TOKEN upload -u $USER -l nightly $CONDA_BLD_PATH/$OS/$PKG_NAME-`date +%Y.%m.%d`-np19py27_0.tar.bz2 --force

