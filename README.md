# VCS (Visualization Control System)

The Visualization Control System (VCS) is expressly designed to meet the needs of scientific community. VCS allows wide-ranging changes to be made to the data display, provides for hardcopy output, and includes a means for recovery of a previous display.

In the VCS model, the data display is defined by a trio of named object sets, designated the “primary objects” (or “primary elements”). These include:

- Data Ingestion: The data, which drives the visualization is ingested into the system via cdms2 or other numeric modules such as numpy;.
- Graphics Method: The graphics method, which specifies the display technique.
- Template: The picture template, which determines the appearance of each segment of the display. Tables for manipulating these primary objects are stored in VCS for later recall and possible use.

In addition, detailed specification of the primary objects’ attributes is provided by eight “secondary objects” (or secondary elements”):

- colormap: Specification of combinations of 256 available colors
- fill area: Style, style index, and color index
- format: Specifications for converting numbers to display strings
- line: Line type, width and color index
- list: A sequence of pairs of numerical and character values
- marker: Marker type, size, and color index
- text: Text font type, character spacing, expansion and color index
- text orientation: Character height, angle, path, and horizontal/vertical alignment

By combining primary and secondary objects in various ways (either at the command line or in a program), the VCS user can comprehensively diagnose and intercompare climate model simulations. VCS provides capabilities to:

- View, select and modify attributes of data variables and of their dimensions
- Create and modify existing template attributes and graphics methods
- Save the state-of-the-system as a script to be run interactively or in a program
- Save a display as a Computer Graphics Metafile (CGM), GIF, Postscript, Sun Raster, or Encapsulated Postscript file
- Perform grid transformations and compute new data variables
- Create and modify color maps
- Zoom into a specified portion of a display
- Change the orientation (portrait vs. landscape) or size (partial vs. full-screen) of a display
- Animate a single data variable or more than one data variable simultaneously
- Display data in various geospatial projections

[![CircleCI](https://circleci.com/gh/CDAT/vcs.svg?style=svg)](https://circleci.com/gh/CDAT/vcs)
[![Coverage Status](https://coveralls.io/repos/github/CDAT/vcs/badge.svg?branch=master)](https://coveralls.io/github/CDAT/vcs?branch=master)

## Installation

VCS is installed through [Conda](https://docs.conda.io/projects/conda/en/latest/index.html), you can find an installation guide [here](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html)

```bash
conda create -n cdat -c conda-forge -c cdat vcs
```

For headless systems, mesalib needs to be installed as well.

```bash
conda create -n cdat -c conda-forge -c cdat vcs mesalib
```

## Documentation

Visit the [VCS User Guide](https://cdat-vcs.readthedocs.io/en/latest/user-guide.html) to find details on usage.

## Tutorials

View the various [tutorials](https://cdat-vcs.readthedocs.io/en/latest/notebooks.html) to see some examples of VCS usage. Some additional tutorials can be found on the [CDAT](https://cdat.llnl.gov/tutorials.html) tutorial page.

## Developers

Many tasks have been automated using a Makefile. See the [targets](#targets) and [variables](#variables) sections for details.

### Targets

- conda-info: Activates conda environment and executes `conda info`.
- conda-list: Activates conda environment and executes `conda list`.
- setup-build: Uses conda-recipes to setup conda environment to build package.
- setup-tests: Creates environment to run tests.
- conda-rerender: Uses conda-recipes and rerenders conda recipe.
- conda-build: Builds conda packages.
- conda-upload: Uploads conda package.
- conda-dump-env: Dumps conda env using `conda list --explicit`.
- get-testdata: Clones uvcdat testdata.
- run-tests: Runs tests.
- run-doc-test: Runs doc tests.
- run-coveralls: Runs coveralls tests.

### Variables

- conda_env: Name of the conda environment to use.
- last_stable: Package version.
- branch: Branch to build from.
- extra_channels: Extra conda channels to use while building.
- conda: Path to the conda executable.
- artifact_dir: Directory to store artifacts.
- copy_conda_package: Will copy the output from `conda build`.

## VCS Model
VCS Allows scientists to produce highly customized plots. Everything can be precisely and logically controlled, without any guessing game

Essentially a vcs plot can be broken down into three parts

WHAT is plotted (e.g data and labels) HOW it is rendered (isolines, boxfill, isofill, vectors, etc…) WHERE (location on the page each elements is to be plotted)

### What
This is the scientific piece of information that the user is trying to represent for others (or self) to understand. It can be as raw as a simple numpy object. But it is recommended to use [CDMS2](https://github.com/CDAT/cdms).

### How
This description of the data representation, at the highest level it is a “graphics method” i.e boxfill, isofill, vectors, streamlines, line plot, etc… But it also contains information to further control these plot types, e.g which colors to use, which levels, lines thickness, etc…

Graphic methods also describe how axes and labels show be represented (e.g which axes values to show and which text to use for it, the user might want to show the -20. longitude represented as 20S or the date 2020-01-15 shown as Jan 2020

### Where
This is the most complicated part of VCS but also one of the most powerful. This controls precisely the location of every component on the plot, these control objects are called templates. Templates also contain one exception to the WHAT/HOW/WHERE rule as they control texts information, albeit via primary objects.

