import doctest, argparse, importlib, re, os


def log_stats(module_name, ignore):
    """Parses a .report file for the given module and writes the doctest errors to a .md file.
    The .md file will be named to match the module_name.
    If the report was generated using the --verbose or -v flag, the .md file will also contain a list of locations
    within the module where therea re no doctests.

    The .report file is assumed to exist in ../reports/ directory.

    :param module_name: String name of the module for which the .report file will be parsed.
        If no .report file exists for that module, this function exits with a SystemError.
    :param verbose: Boolean to indicate whether the parsed report was produced using the verbose flag.
    :return:
    """
    # open .results file to read, and .md file to log
    try:
        results = open("../reports/" + module_name + ".report", "r+")
    except:
        raise SystemError("File not found: " + "../reports/" + module_name + ".results")
    else:
        log = open("../markdown/" + module_name + '.md', 'w+')
        missing_header = re.compile("^[0-9]+ items had no tests:$")
        # missing tests will be followed by either passed all tests or "tests in items" entry
        passing_header = re.compile("^[0-9]+ items passed all tests:$")
        tests_in_items = re.compile("^[0-9]+ tests in [0-9]+ items\.$")
        no_tests = re.compile("^[0-9]+ items had no tests:$")
        trying = re.compile("^Trying:$")
        err_header = re.compile('File "')
        err_indicator = re.compile('\*\*\*\*')
        line = results.readline()
        err_endpoints = [trying, no_tests, err_indicator]
        missing_endpoints = [passing_header, tests_in_items, err_indicator]
        while line != '':
            if re.match(err_header, line):
                where = line.split()[-1]
                log.write(where+"\n")
                for i in range(len(where)):
                    log.write("-")
                log.write("\n")
                log.write("```python\n")
                consume_entry(results, log, err_endpoints)
                log.write("```\n\n")
            if re.match(missing_header, line):
                header="Missing Doctests"
                log.write(header+"\n")
                map(lambda x: log.write('-'), range(len(header)))
                log.write("\n")
                consume_entry(results, log, missing_endpoints, ":x:```", "```\n", ignore)
            line = results.readline()
        log.close()
        results.close()
    print ("Done logging "+module_name+".md")


# note: will only consume the first full error (maybe)
def consume_entry(readfile, writefile, endpoints, prepend="", append="", ignore=[]):
    """Consumes a log entry from readfile up to one of a list of possible endpoints.
    Writes each line in the entry to writefile.

    :param readfile: File to read from
    :param writefile: File to write to
    :param endpoints: List of compiled regular expressions which are the possible points at which a log entry can end.
    :param prepend: A string to prepend to the line from readfile before outputting to writefile
    :param append: A string to append to the line from readfile before outputting to writefile
    :param ignore: A list of regular expressions containing function signatures to ignore (for logging missing doctests
        only. Gets brought in through commandline or a file via ArgParse.
    """
    more = True
    sigs = [re.compile("_[_A-z0-9]+")] # func signatures to ignore. Add private functions by default.
    if len(ignore):
        for sig in ignore:
           sigs.append(re.compile(sig))
    line = readfile.readline()
    while more and line != '':
        no_write = False
        for sig in sigs:
            if re.match(sig, line.split('.')[-1]):
                no_write = True
        if not no_write:
            if append != "":
                index = line.find("\n")
                new_line = prepend + line[:index] + append + line[index:]
                writefile.write(new_line)
            else:
                writefile.write(prepend + line + append)
        line = readfile.readline()
        for endpoint in endpoints:
            if re.match(endpoint, line):
                more = False


def cleanup():
    """Cleanup for the doctests. If some files aren't being deleted after testing, add their glob signature to the
    patterns list.

    .. warning::

        Do NOT add a "*.py" glob, or anything that would delete a name matching either doctest_vcs.py
        or run_all_doctests.sh. The files that get cleaned up are generated in this directory.

    """
    import glob, os
    gb = glob.glob
    patterns = ["example.*", "*.json", "*.svg", "ex_*", "my*", "filename.*", "*.png", "deft_box.py", "*.mpeg"]
    for pattern in patterns:
        fnames = gb(pattern)
        for name in fnames:
            try:
                os.remove(name)
            except:
                continue


# Make parser and add options
parser = argparse.ArgumentParser()
parser.add_argument('module', type=str, help="Name of the VCS module to test.")
parser.add_argument('-v', '--verbose', action='store_true', default=False,
                    help='Passing doctests logged. Report includes number of missing doctests, minus any for ' +
                         'function signatures explicitly ignored via -i or --ifile options.')
parser.add_argument('-r', '--report', action='store_true', default=False, help='Print a report after running tests.')
parser.add_argument('-l', '--log', action='store_true', default=False, help='Log stats in a .md file.\nImplies -r.')
parser.add_argument('--LO', action='store_true', default=False, help='ONLY read .results and make .md log.')
parser.add_argument('-p', '--package', type=str, default='vcs',
                    help="Supply a package name in which to look for the module.\nDefault is vcs.")
parser.add_argument('-a', '--all', action="store_true", default=False,
                    help="Report all failures.\nIf not set, will report only the first failure in each doctest")
parser.add_argument('-i', '--ignore', nargs='*', default=[],
                    help="List of regular expressions representing function signatures to ignore, when parsing report "
                    + "output for missing doctests.\n" + "Used for logging purposes only. If -i is provided, --ifile "
                    + "will be ignored.\n If provided, -i must be specified after the module name.")
parser.add_argument('--ifile', type=file, default=None, help="File containing a list of function signatures to ignore"
                    + "when parsing report output for missing doctests. The file must be a newline-delimited list of "
                    + "regular expressions. Only provide --ifile if -i(--ignore) has not been provided.")
# Check parser args
args = parser.parse_args()

ignore = []
if len(args.ignore):
    ignore = args.ignore
elif args.ifile:
    for line in args.ifile:
        ignore.append(line)
if not args.LO:
    import vcs
    if not os.path.exists(vcs.sample_data):
        vcs.download_sample_data_files()
    if args.log and not args.report:
        args.report = True
    options=doctest.ELLIPSIS
    if not args.all:
        options=options|doctest.REPORT_ONLY_FIRST_FAILURE
    # Import module and run doctests
    m = importlib.import_module(args.package + '.' + args.module)
    doctest.testmod(m, optionflags=options, report=args.report, verbose=args.verbose)
    cleanup()
    if args.log:
        log_stats(args.module, ignore)
else:
    log_stats(args.module, ignore)
exit()
