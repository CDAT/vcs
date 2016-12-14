#!/usr/bin/env bash
MODULES=("Canvas" "Pboxeslines" "Pdata" "Pformat" "Plegend" "Ptext" "Pxlabels"
"Pxtickmarks" "Pylabels" "Pytickmarks" "VCS_validation_functions" "boxfill" 
"colormap" "colors" "configurator" "displayplot"
"dv3d" "editors" "error" "fillarea" "isofill" "isoline" "line" "manageElements"
"marker" "meshfill" "projection" "queries" "taylor" "template" "textcombined"
"textorientation" "texttable" "unified1D" "utils" "vcshelp" "vector")


for module in "${MODULES[@]}"; do python doctest_vcs.py "$module" -a -v -r > "$module.report"; done;
for module in "${MODULES[@]}"; do python doctest_vcs.py "$module" -v -r --LO; done;
