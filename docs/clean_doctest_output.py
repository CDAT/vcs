import os, sys, re

try:
    fp=open('_build/doctest/output.txt')
except:
    raise("You should probably run `make doctest` first")
dict={}
line=fp.readline()
header=re.compile('^Document')

while(line != ''):
    if(re.match(header, line)):


