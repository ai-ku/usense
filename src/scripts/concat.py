#!/usr/bin/env python

import sys
import gzip
import re


path = sys.argv[2]
for line in  gzip.open(sys.argv[1]):
    line = line.strip()
    print >> sys.stderr, path+line
    for l in open(path+line+".cluster.txt"):
        l = l.strip()
        print l
