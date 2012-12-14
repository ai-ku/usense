#!/usr/bin/env python

import sys
from itertools import izip
import gzip


for i,j in izip(gzip.open(sys.argv[1]), gzip.open(sys.argv[2])):
    i,j = i.strip(), j.strip()
    print i+"\t"+j
