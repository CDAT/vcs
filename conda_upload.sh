PKG_NAME=vcs
USER=uvcdat
if [ "$TRAVIS_OS_NAME" = "linux" ]; then
    OS=linux-64
else
    OS=osx-64
fi

mkdir ~/conda-bld
conda config --set anaconda_upload no
export CONDA_BLD_PATH=~/conda-bld
export VERSION=`date +%Y.%m.%d`
git clone git://github.com/UV-CDAT/conda-recipes
cd conda-recipes
python ./prep_for_build.py -v `date +%Y.%m.%d`
conda build vcs -c conda-forge -c uvcdat 
anaconda -t $CONDA_UPLOAD_TOKEN upload -u $USER -l nightly $CONDA_BLD_PATH/$OS/$PKG_NAME-`date +%Y.%m.%d`-py27_0.tar.bz2 --force
if [ "${TRAVIS_OS_NAME}" = "linux" ]; then
    python ./prep_for_build.py -v `date +%Y.%m.%d` -f nox
    conda build vcs -c conda-forge -c uvcdat 
    anaconda -t $CONDA_UPLOAD_TOKEN upload -u $USER -l nightly $CONDA_BLD_PATH/$OS/$PKG_NAME-nox-`date +%Y.%m.%d`-py27_0.tar.bz2 --force
fi

