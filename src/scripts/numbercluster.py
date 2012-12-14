#!/usr/bin/env python

import sys
import gzip
import re
from collections import defaultdict as dd

regWord = re.compile("^(.*?\.\w)\.(\d+)")
dic = dd(lambda : dd(int))

for line in gzip.open(sys.argv[1]):
    l = line.strip()
    m = regWord.search(l)
    if m:
        dic[m.group(1)][m.group(2)] += 1

for k,v in dic.items():
    print k+"\t"+str(len(v))
