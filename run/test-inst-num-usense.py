#! /usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Osman Baskaya"

import sys
import gzip
from collections import defaultdict as dd



sub_file = gzip.open('test.sub.gz')

d = dd(int)
for line in sub_file:
    inst = line.split()[0][1:-1]
    tw =  inst.rsplit('.', 1)[0]
    d[tw] += 1

total = 0
for key, val in d.iteritems():
    print key, val
    total += val

print >> sys.stderr, "sanity check: {} number of instances".format(total)
