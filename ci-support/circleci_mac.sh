export UVCDAT_ANONYMOUS_LOG=False
export UVCDAT_SETUP_PATH=${HOME}
export PATH=${HOME}/miniconda/bin:${PATH}
#export VCS_BACKGROUND=0  # circleci seg faults on bg=1
source activate py2
conda list
python run_tests.py -v2 -n 2 -g --no-vtk-ui
RESULT=$?
echo "py2 test command exit result:",$RESULT
source activate py3
conda list
python run_tests.py -n 2 -g --no-vtk-ui
RESULT=$(( $RESULT + $? ))
cd docs
make doctest
RESULT=$(( $RESULT + $? ))
cd ..
echo "py3 test command exit result:",$RESULT
if [ $RESULT -eq 0 -a $CIRCLE_BRANCH == "master" ]; then conda install -n root conda-build anaconda-client ; fi
if [ $RESULT -eq 0 -a $CIRCLE_BRANCH == "master" ]; then bash ./ci-support/conda_upload.sh ; fi
exit $RESULT

