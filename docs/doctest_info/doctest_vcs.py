import vcs, sys, doctest, argparse, importlib

# TODO: add cleanup function
# TODO: add args for only running cleanup, only logging missing doctests
#   *.png, filename.*, ex_*, example.*
def log_stats(module_name, verbose):
    import re
    fp = open(module_name+".results")
    log = open(module_name+'.md', 'w+')
    missing_header = re.compile("[0-9]+ items had no tests:")
    # missing tests will be followed by either passed all tests or "tests in items" entry
    passing_header = re.compile("[0-9]+ items passed all tests:")
    tests_in_items = re.compile("[0-9]+ tests in [0-9]+ items\.")
    trying = re.compile("Trying:")
    expecting_something = re.compile("Expecting:")
    expecting_nothing = re.compile("Expecting nothing")
    err_header = re.compile('File "')
    err_indicator = re.compile('\*\*\*\*')
    line = fp.readline()
    while line != '':



# Make parser and add options
parser = argparse.ArgumentParser()
parser.add_argument('module', type=str, help="Name of the VCS module to test.")
parser.add_argument('-v', '--verbose', action='store_true', default=False,
                    help='Passing doctests logged. Report includes number of untested functions.')
parser.add_argument('-r', '--report', action='store_true', default=False, help='Print a report after running tests.')
parser.add_argument('-l', '--log', action='store_true', default=False, help='Log stats in a .md file.\nImplies -r.')
pkg_help="Supply a package name in which to look for the module.\nDefault is vcs."
parser.add_argument('-p', '--package', type=str, default='vcs', help=pkg_help)

# Check parser args
args = parser.parse_args()
if args.log and not args.report:
    args.report=True

# Import module and run doctests
m = importlib.import_module(args.package + '.' + args.module)
doctest.testmod(m, optionflags=doctest.ELLIPSIS, report=args.report, verbose=args.verbose)

