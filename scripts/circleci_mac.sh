export UVCDAT_ANONYMOUS_LOG=False
vcs_download_sample_data
conda config --set anaconda_upload no
cd /git_repo
ls -l
python setup.py install --old-and-unmanageable
git clone git://github.com/uv-cdat/uvcdat-testdata
python run_tests.py -v2 -g

