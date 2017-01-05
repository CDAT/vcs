Ignore Files
------------

This directory is to hold ignore files.

These ignore files are used to ignore certain regular expressions when parsing doctest report logs for missing doctests.

If you have things showing up in the 'Missing Doctests' section of your markdown reports that shouldn't be there, make or append to a ```$MODULE_NAME.ignore``` file in this directory.

.ignore files should contain a newline-delimited list of regular expressions for the signatures of properties/functions that you want to ignore, when looking for missing doctests.

For example, given a ```boxfill.ignore``` file with the following contents:

	Gfb
	process_src

The missing report in boxfill.md will omit any lines which have 'Gfb' or 'process_src' after the last '.' for their signature.

As of now, this will only ignore the last part of the signature flagged as missing. i.e. ```vcs.Canvas.Canvas.animate``` and ```vcs.Canvas.Canvas.animate_info``` would both be ignored if
Canvas.ignore contained ```animate```, but would not be ignored if it contained ```vcs.Canvas.Canvas.animate```.
