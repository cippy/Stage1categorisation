#!/usr/bin/env python  

from shutil import copyfile
import re, sys, os, os.path, subprocess, json, ROOT
import numpy as np
from collections import OrderedDict

from Tools.variableDefinitions import allVarsGen, dijetVars

default_variables = allVarsGen + dijetVars

from optparse import OptionParser
parser = OptionParser(usage="%prog [options] infile.root")
parser.add_option('-t', '--tree',          dest='tree',      default='', type='string', help='Tree name (with possible path) inside root file')
parser.add_option('-v', '--variables',          dest='variables',      default='', type='string', help='Comma separated list of variables to check (list is appended to default one hardcoded in this script')
(options, args) = parser.parse_args()

if len(sys.argv) < 1:
    parser.print_usage()
    quit()

if not options.tree:
    print "Please specify the name of the tree (possibly with path) inside the root file"
    quit()
    
fname = args[0]
tf = ROOT.TFile.Open(fname,"READ")
if not tf or tf.IsZombie():
    print "Error opening file %s " % fname
    quit()
tree = tf.Get(options.tree)
if not tree:
    print "Error getting tree %s " % options.tree
    quit()

variables = [str(x) for x in default_variables]
if options.variables:
    variables.append(str(x) for x in options.variables.split(','))

# remove possible duplicates
variables = list(OrderedDict.fromkeys(variables))
    
print "-"*30
print "Following branches were not found in tree"
print "-"*30

listOfLeaves = [l.GetName() for l in tree.GetListOfLeaves()]
nMiss = 0
for iv,v in enumerate(variables):    
    if v not in listOfLeaves:
        print "{: <10} {n}".format(iv,n=v)
        nMiss += 1
print "-"*30
print "Missing %d variables" % nMiss

