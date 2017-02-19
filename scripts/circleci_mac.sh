export UVCDAT_ANONYMOUS_LOG=False
export PATH=${HOME}/miniconda/bin:${PATH}
python run_tests.py -v2 -g -H -p  # -H and -p for collection by artifacts

