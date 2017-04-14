export UVCDAT_ANONYMOUS_LOG=False
export PATH=${HOME}/miniconda/bin:${PATH}
#export VCS_BACKGROUND=0  # circleci seg faults on bg=1
#python run_tests.py -v2 -g -H -p  # -H and -p for collection by artifacts
python run_tests.py --dropbox -v2 -g --no-vtk-ui

