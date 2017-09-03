export UVCDAT_ANONYMOUS_LOG=False
export PATH=${HOME}/miniconda/bin:${PATH}
#export VCS_BACKGROUND=0  # circleci seg faults on bg=1
python run_tests.py -n 1 -v2 -g --no-vtk-ui
RESULT=$?
echo "test command exit result:",$RESULT
if [ $RESULT -eq 0 -a $CIRCLE_BRANCH == "master" ]; then conda install conda-build anaconda-client ; fi
if [ $RESULT -eq 0 -a $CIRCLE_BRANCH == "master" ]; then bash ./ci-support/conda_upload.sh ; fi
exit $RESULT

