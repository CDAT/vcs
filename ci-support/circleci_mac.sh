export UVCDAT_ANONYMOUS_LOG=False
export UVCDAT_SETUP_PATH=${HOME}
export PATH=${HOME}/miniconda/bin:${PATH}
#export VCS_BACKGROUND=0  # circleci seg faults on bg=1
source activate py2
conda list
python run_tests.py -v2 -n 2 --no-vtk-ui
RESULT=$?
echo "py2 test command exit result:",$RESULT
source activate py3
conda list
python run_tests.py -n 2 --no-vtk-ui
RESULT=$(( $RESULT + $? ))
echo "py3 test command exit result:",$RESULT
exit $RESULT

