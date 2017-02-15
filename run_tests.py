import unittest
import glob
import sys
import os
import argparse
import multiprocessing
import logging

cpus = multiprocessing.cpu_count()

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "tests"))
if len(sys.argv)==1:
    names = glob.glob("tests/test_*.py")
else:
    names = sys.argv[1:]

print "NAMES:",names

#suite = unittest.defaultTestLoader.loadTestsFromNames(names)
#runner = unittest.TextTestRunner(verbosity=2).run(suite)
from nose.plugins.multiprocess import MultiProcess
import nose
import subprocess

#results = nose.run(argv=["nosetests","-v","--process-restartworker","--processes=%i" % cpus] + names)
p =  subprocess.Popen(["nosetests","-v","--process-restartworker","--processes=%i" % cpus] + names, stdout = subprocess.PIPE, stderr=subprocess.STDOUT,bufsize=0)
out = []
while p.poll() is None:
    read = p.stdout.readline()[:-1]
    out.append(read)
    print read

print "Done",p.poll()
sys.exit(p.poll())
