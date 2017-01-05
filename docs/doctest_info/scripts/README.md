Doctest Scripts
---------------

This directory contains the scripts used to run VCS's modules through doctest.testmod.

#### doctest_vcs.py ####

doctest_vcs.py lets us run doctests on a single module. It can also be used to generate reports and .md logs of important
details from the doctests, such as which tests aren't passing along with the errors that they have, and which parts of the module are missing doctests.

##### using doctest_vcs #####

__These scripts need to be run from the doctest_info/scripts directory (I'm sure that can be fixed, but I haven't done so yet).__

If you want to run all the VCS modules through doctest_vcs, all you have to do is run ```./run_all_doctests.sh``` in the terminal (make sure it has executable permissions on your machine)

Testing individual modules can require several more steps.

To test a module and have it output to the screen:

	$ python doctest_vcs.py $MODULE_NAME

is all you need. This will print the simplest form of doctest output, which contains all of the failing doctest in the module.

Currently to obtain the log information you have to use the terminal to redirect doctest output to a file: 

	$ doctest.py -v -r $MODULE_NAME > ../reports/$MODULE_NAME.report
        $ doctest.py --LO $MODULE_NAME

The second step parses the report file for doctest errors and missing doctests. You can omit it and redirect output to anywhere if you just want a report. 
The report file MUST be named $MODULE_NAME.report and be located in doctest_info/reports if you want to generate the markdown-formatted summary log.

If there are things being reported in the 'Missing Doctests' section of the .md summary that shouldn't be there, follow the instructions in doctest_info/ignore/README.md
to add an ignore file for the module (if one does not exist). Then, when you run the logging function provide that file as the --ifile option:
	
	$ doctest.py --LO --ifile ../ignore/$MODULE_NAME.ignore $MODULE_NAME

#### run_all_doctest.sh ####

This script runs all of the modules in VCS through doctest.py, redirects their output to doctest_info/reports/$MODULE_NAME.report,
and runs the logging function on the .report using the appropriate .ignore file.

If you find that the script is missing some modules, simply add their names to the MODULES array declared at the start of the script.
