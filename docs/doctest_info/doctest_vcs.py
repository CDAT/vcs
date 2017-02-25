import doctest, argparse, importlib, re


def log_stats(module_name, verbose):
    # open .results file to read, and .md file to log
    try:
        results = open(module_name+".report", "r+")
    except:
        raise SystemError("File not found: " + module_name + ".results")
    else:
        log = open(module_name+'.md', 'w+')
        missing_header = re.compile("^[0-9]+ items had no tests:$")
        # missing tests will be followed by either passed all tests or "tests in items" entry
        passing_header = re.compile("^[0-9]+ items passed all tests:$")
        tests_in_items = re.compile("^[0-9]+ tests in [0-9]+ items\.$")
        no_tests = re.compile("^[0-9]+ items had no tests:$")
        trying = re.compile("^Trying:$")
        err_header = re.compile('File "')
        err_indicator = re.compile('\*\*\*\*')
        line = results.readline()
        if verbose:
            err_endpoints = [trying, no_tests]
            missing_endpoints = [passing_header, tests_in_items, err_indicator]
        else:
            err_endpoints = [err_indicator,]
        while line != '':
            if re.match(err_header, line):
                where = line.split()[-1]
                log.write(where+"\n")
                for i in range(len(where)):
                    log.write("-")
                log.write("\n")
                log.write("```python\n")
                consume_entry(results, log, err_endpoints, "", "")
                log.write("```\n\n")
            if re.match(missing_header, line):
                header="Missing Doctests"
                log.write(header+"\n")
                map(lambda x: log.write('-'), range(len(header)))
                log.write("\n")
                consume_entry(results, log, missing_endpoints, ":x:```", "```\n")
            line = results.readline()
        log.close()
        results.close()
    print ("Done logging "+module_name+".md")


# note: will only consume the first full error
def consume_entry(readfile, writefile, endpoints, prepend, append):
    more = True
    line = readfile.readline()
    while more and line != '':
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
    import glob, os
    gb = glob.glob
    patterns = ["example.*", "*.json", "*.svg", "ex_*", "my*", "filename.*"]
    files = []
    for pattern in patterns:
        fnames = gb(pattern)
        for name in fnames:
            files.append(name)
    for file in files:
        try:
            os.remove(file)
        except:
            pass


# Make parser and add options
parser = argparse.ArgumentParser()
parser.add_argument('module', type=str, help="Name of the VCS module to test.")
parser.add_argument('-v', '--verbose', action='store_true', default=False,
                    help='Passing doctests logged. Report includes number of untested functions.')
parser.add_argument('-r', '--report', action='store_true', default=False, help='Print a report after running tests.')
parser.add_argument('-l', '--log', action='store_true', default=False, help='Log stats in a .md file.\nImplies -r.')
parser.add_argument('--LO', action='store_true', default=False, help='ONLY read .results and make .md log.')
parser.add_argument('-p', '--package', type=str, default='vcs',
                    help="Supply a package name in which to look for the module.\nDefault is vcs.")
parser.add_argument('-a', '--all', action="store_true", default=False,
                    help="Report all failures.\nIf not set, will report only the first failure in each doctest")
# Check parser args
args = parser.parse_args()

if not args.LO:
    import vcs
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
        log_stats(args.module, args.verbose)
else:
    log_stats(args.module, args.verbose)
exit()
