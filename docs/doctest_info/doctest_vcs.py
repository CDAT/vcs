import vcs, sys, doctest, argparse, importlib

# TODO: add cleanup function
# TODO: add args for only running cleanup, only logging missing doctests
#   *.png, filename.*, ex_*, example.*
def log_missing(module_name):
    import re

    fp = open(module_name+".results")
    # will want to open in append mode instead
    log = open('missing_doctests.md', 'w+')
    missing_header = re.compile("Document:")


parser = argparse.ArgumentParser()
parser.add_argument('module', type=str, help="Name of the VCS module to test.")
parser.add_argument('-v', '--verbose', action='store_true', default=False,
                    help='Passing doctests logged. Report includes number of untested functions.')
parser.add_argument('-r', '--report', action='store_true', default=False, help='Print a report after running tests')
parser.add_argument('-m', '--missing', action='store_true', default=False, help='Print a report after running tests')
args = parser.parse_args()
m = importlib.import_module("vcs."+args.module)
doctest.testmod(m, optionflags=doctest.ELLIPSIS, report=args.report, verbose=args.verbose)