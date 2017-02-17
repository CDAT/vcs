import unittest
import glob
import sys
import os
import argparse
import multiprocessing
import subprocess
import image_compare
import codecs
import time
import webbrowser

# We need to clone baselines
p = subprocess.Popen('git rev-parse --abbrev-ref HEAD'.split(),shell=False,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
o,e = p.communicate()
b = o.strip()
if not os.path.exists("uvcdat-testdata"):
    subprocess.call("git clone git://github.com/uv-cdat/uvcdat-testdata".split())
os.chdir("uvcdat-testdata")
subprocess.call("git pull".split())  # lock issues on mac
subprocess.call(("git checkout %s" % (b)).split())
os.chdir("..")

cpus = multiprocessing.cpu_count()

parser = argparse.ArgumentParser(description="Run VCS tests",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("-H","--html",action="store_true",help="create and show html result page")
parser.add_argument("-p","--package",action="store_true",help="package test results (not implemented)")
parser.add_argument("-c","--coverage",action="store_true",help="run coverage (not implemented)")
parser.add_argument("-u","--upload",action="store_true",help="upload packaged tests results (not implemented)")
parser.add_argument("-v","--verbosity",default=1,choices=[0,1,2],type=int,help="verbosity output level")
parser.add_argument("-n","--cpus",default=cpus,type=int,help="number of cpus to use")
parser.add_argument("tests",nargs="*",help="tests to run")


def abspath(path,name,prefix):
    import shutil
    full_path = os.path.abspath(os.path.join(os.getcwd(),"..",path))
    if not os.path.exists(name):
        os.makedirs(name)
    new = os.path.join(nm,prefix+"_"+os.path.basename(full_path))
    shutil.copy(full_path,new)
    return new



def findDiffFiles(log):
   i = -1
   file1 = ""
   file2 = ""
   N = len(log)
   while log[i].find("Source file")==-1 and i>-N:
       i -= 1
   if i>-N:
       file2 = log[i].split()[-1]
       file1 = log[i-1].split()[-1]
   return file1, file2

args = parser.parse_args()
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "tests"))
if len(args.tests)==0:
    names = glob.glob("tests/test_*.py")
else:
    names = args.tests
if args.verbosity>1:
    print("Names:",names)

def run_nose(test_name):
    command = ["nosetests","-s",test_name]
    if args.verbosity>0:
        print "Executing %s in %s" % (" ".join(command),os.getcwd())
    start = time.time()
    P =  subprocess.Popen(command, stdout = subprocess.PIPE, stderr=subprocess.STDOUT,bufsize=0,cwd=os.getcwd())
    out = []
    while P.poll() is None:
        read = P.stdout.readline().rstrip()
        out.append(read)
        if args.verbosity>1 and len(read)!=0: print read
    end=time.time()
    return {test_name:{"result":P.poll(),"log":out,"times":{"start":start,"end":end}}}

p = multiprocessing.Pool(args.cpus)
outs = p.map(run_nose, names)
results = {}
failed = []
for d in outs:
    results.update(d)
    nm = d.keys()[0]
    if d[nm]["result"]!=0:
        failed.append(nm)

if args.verbosity>0: 
    print "Ran %i tests, %i failed (%.2f%%)" % (len(outs),len(failed),float(len(failed))/len(outs)*100.)
    if len(failed)>0:
        print "Failed tests:"
        for f in failed:
            print "\t",f
if args.html or args.package:
    if not os.path.exists("tests_html"):
        os.makedirs("tests_html")
    os.chdir("tests_html")

    js = image_compare.script_data()

    fi=open("index.html","w")
    print>>fi,"<!DOCTYPE html>"
    print>>fi,"""<html><head><title>VCS Test Results %s</title>
    <link rel="stylesheet" type="text/css" href="http://cdn.datatables.net/1.10.12/css/jquery.dataTables.css">
    <script type="text/javascript" src="http://code.jquery.com/jquery-1.12.4.js"></script>
    <script type="text/javascript" charset="utf8" src="http://rawgit.com/WCRP-CMIP/CMIP6_CVs/master/src/jquery.dataTables.js"></script>
    <script>
    $(document).ready( function () {
            $('#table_id').DataTable();
                } );
    </script>
    </head>""" % time.asctime()
    print>>fi,"<body><h1>VCS Test results: %s</h1>" % time.asctime()
    print>>fi,"<table id='table_id' class='display'>"
    print>>fi,"<thead><tr><th>Test</th><th>Result</th><th>Start Time</th><th>End Time</th><th>Time</th></tr></thead>"
    print>>fi,"<tfoot><tr><th>Test</th><th>Result</th><th>Start Time</th><th>End Time</th><th>Time</th></tr></tfoot>"

    for t in sorted(results.keys()):
        result = results[t]
        nm = t.split("/")[-1][:-3]
        print>>fi,"<tr><td>%s</td>" % nm,
        fe=codecs.open("%s.html"%nm,"w",encoding="utf-8")
        print>>fe,"<!DOCTYPE html>"
        print>>fe,"<html><head><title>%s</title>" % nm
        if result["result"] == 0:
            print>>fi,"<td><a href='%s.html'>OK</a></td>" % nm,
            print>>fe,"</head><body>"
            print>>fe,"<a href='index.html'>Back To Results List</a>"
        else:
            print>>fi,"<td><a href='%s.html'>Fail</a></td>" % nm,
            print>>fe,"<script type='text/javascript'>%s</script></head><body>" % js
            print>>fe,"<a href='index.html'>Back To Results List</a>"
            print>>fe,"<h1>Failed test: %s on %s</h1>"%(nm,time.asctime())
            file1,file2 = findDiffFiles(result["log"])
            print>>fe,'<div id="comparison"></div><script type="text/javascript"> ImageCompare.compare(document.getElementById("comparison"), "%s", "%s"); </script>' % (abspath(file2,nm,"test"),abspath(file1,nm,"source"))
        print>>fe,"<a href='index.html'>Back To Results List</a>"
        print>>fe,'<div id="output"><h1>Log</h1><pre>%s</pre></div>' % "\n".join(result["log"])
        print>>fe,"<a href='index.html'>Back To Results List</a>"
        print>>fe,"</body></html>"
        fe.close()
        t = result["times"]
        print>>fi,"<td>%s</td><td>%s</td><td>%s</td></tr>" % (time.ctime(t["start"]),time.ctime(t["end"]),t["end"]-t["start"])

    print>>fi,"</table></body></html>"
    fi.close()
    if args.html:
        webbrowser.open("file://%s/index.html"% os.getcwd())
    os.chdir("..")

if args.package:
    import tarfile
    tnm = "results_%s.tar.bz2" % time.strftime("%Y-%m-%d_%H:%M")
    t = tarfile.open(tnm,"w:bz2")
    t.add("tests_html")
    t.close()
    if args.verbosity>0:
        print "Packaged Result Info in:",tnm




sys.exit(len(failed))
