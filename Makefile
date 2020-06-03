.PHONY: conda-info conda-list setup-build setup-tests conda-rerender \
	conda-build conda-upload conda-dump-env conda-cp-output get_testdata \
	run-tests run-doc-tests run-coveralls

SHELL = /bin/bash

os = $(shell uname)
pkg_name = vcs
build_script = conda-recipes/build_tools/conda_build.py

test_pkgs = udunits2 testsrunner matplotlib image-compare nbformat ipywidgets \
						nb_conda nb_conda_kernels coverage coveralls
docs_pkgs = sphinxcontrib-websupport nbsphinx jupyter_client jupyterlab vcsaddons 
ifeq ($(os),Linux)
pkgs = "mesalib=18.3.1"
else
pkgs = "mesalib=17.3.9"
endif

conda_env ?= base
workdir ?= $(PWD)/workspace
last_stable ?= 8.2
branch ?= $(shell git rev-parse --abbrev-ref HEAD)
extra_channels ?= cdat/label/nightly conda-forge
conda ?= $(or $(CONDA_EXE),$(shell find /opt/*conda*/bin $(HOME)/*conda* -type f -iname conda))
artifact_dir ?= $(PWD)/artifacts
conda_env_filename ?= spec-file

conda_base = $(patsubst %/bin/conda,%,$(conda))
conda_activate = $(conda_base)/bin/activate

conda-info:
	source $(conda_activate) $(conda_env); conda info

conda-list:
	source $(conda_activate) $(conda_env); conda list

setup-build:
ifeq ($(wildcard $(workdir)/conda-recipes),)
	git clone -b build_tool_update https://github.com/CDAT/conda-recipes $(workdir)/conda-recipes
else
	cd $(workdir)/conda-recipes; git pull
endif

setup-tests:
	source $(conda_activate) base; conda create -y -n $(conda_env) --use-local $(foreach x,$(extra_channels),-c $(x)) \
		$(pkg_name) $(test_pkgs) $(docs_pkgs) $(pkgs) $(extra_pkgs)

conda-rerender: setup-build 
	python $(workdir)/$(build_script) -w $(workdir) -l $(last_stable) -B 0 -p $(pkg_name) \
		-b $(branch) --do_rerender --conda_env $(conda_env) --ignore_conda_missmatch \
		--conda_activate $(conda_activate)

conda-build:
	python $(workdir)/$(build_script) -w $(workdir) -p $(pkg_name) --build_version noarch \
		--do_build --conda_env $(conda_env) --extra_channels $(extra_channels) \
		--conda_activate $(conda_activate)

conda-upload:
	source $(conda_activate) $(conda_env); \
		output=$$(conda build --output $(workdir)/vcs); \
		anaconda -t $(conda_upload_token) upload -u $(user) -l $(label) $${output} --force

conda-dump-env:
	source $(conda_activate) $(conda_env); conda list --explicit > $(artifact_dir)/$(conda_env_filename).txt

conda-cp-output:
	source $(conda_activate) $(conda_env); output=$$(conda build --output $(workdir)/vcs/); \
		cp $${output} $(artifact_dir)/

get-testdata:
ifeq ($(wildcard uvcdat-testdata),)
	git clone git://github.com/CDAT/uvcdat-testdata
else
	cd uvcdat-testdata; git pull
endif

run-tests:
	source $(conda_activate) $(conda_env); python run_tests.py -n 4 -H -v2 --timeout=100000 \
		--checkout-baseline --no-vtk-ui

run-doc-test:
	source $(conda_activate) $(conda_env); cd docs; make doctest;

run-coveralls:
	source $(conda_activate) $(conda_env); coveralls;
