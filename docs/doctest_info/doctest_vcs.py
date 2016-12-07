import vcs, sys, doctest, argparse, importlib, re

# TODO: add cleanup function
# TODO: add args for only running cleanup, only logging missing doctests
#   *.png, filename.*, ex_*, example.*


def log_stats(module_name, verbose):
    # open .results file to read, and .md file to log
    results = open(module_name+".results", "r+")
    log = open(module_name+'.md', 'w+')
    missing_header = re.compile("^[0-9]+ items had no tests:$")
    # missing tests will be followed by either passed all tests or "tests in items" entry
    passing_header = re.compile("^[0-9]+ items passed all tests:$")
    tests_in_items = re.compile("^[0-9]+ tests in [0-9]+ items\.$")
    trying = re.compile("^Trying:$")
    expecting_something = re.compile("^Expecting:$")
    expecting_nothing = re.compile("^Expecting nothing$")
    err_header = re.compile('File "')
    err_indicator = re.compile('\*\*\*\*')
    line = results.readline()
    if verbose:
        err_endpoint = [trying]
        missing_endpoints = [passing_header, tests_in_items]
    else:
        err_endpoint = [err_indicator]
    while line != '':
        if re.match(err_header, line):
            where = line.split()[-1]
            log.write(where+"\n")
            for i in range(len(where)):
                log.write("-")
            log.write("\n")
            log.write("```python\n")
            consume_entry(results, log, err_endpoint, "")
            log.write("```\n\n")
        if re.match(missing_header, line):
            log.write("\nMissing Docstrings\n------------------\n")
            consume_entry(results, log, missing_endpoints, "- [ ] ")
        line = results.readline()


# note: will only consume the first full error
def consume_entry(readfile, writefile, endpoints, prepend):
    more = True
    line = readfile.readline()
    while more and line != '':
        writefile.write(prepend + line)
        line = readfile.readline()
        for endpoint in endpoints:
            if re.match(endpoint, line):
                more = False


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
    if args.log and not args.report:
        args.report=True
    options=doctest.ELLIPSIS
    if not args.all:
        options=options|doctest.REPORT_ONLY_FIRST_FAILURE
    # Import module and run doctests
    m = importlib.import_module(args.package + '.' + args.module)
    doctest.testmod(m, optionflags=options, report=args.report, verbose=args.verbose)

if args.log or args.LO:
    log_stats(args.module, args.verbose)
exit()

