#!/usr/bin/env python


import sys
import gzip
from itertools import izip

#1 clsuters
#2 pairs
#concatanate 1 to first column of 2
for i,j in izip(gzip.open(sys.argv[1]), gzip.open(sys.argv[2])):
    i,j = i.strip(), j.strip().split()
    j[0]+=i
    print "\t".join(j)
    



