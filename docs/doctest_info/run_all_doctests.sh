#!/usr/bin/env bash
MODULES=("Canvas" "Pboxeslines" "Pdata" "Pformat" "Plegend" "Ptext" "Pxlabels"
"Pxtickmarks" "Pylabels" "Pytickmarks" "validation_functions" "VTKAnimate" "VTKPlots"
"animate_helper" "boxfill" "colormap" "colorpicker" "colors" "configurator" "displayplot"
"dv3d" "editors" "error" "fillarea" "isofill" "isoline" "line" "manageElements"
"marker" "meshfill" "projection" "queries" "taylor" "template" "textcombined"
"textorientation" "texttable" "unified1D" "utils" "vcs2vtk" "vcshelp" "vcsvtk" "vector"
"vtk_ui")


for module in "${MODULES[@]}"; do python doctest_vcs.py "$module" -v -r -l > "$module.report"; done;