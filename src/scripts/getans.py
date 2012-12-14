#!/usr/bin/env python

import sys
from itertools import izip
import gzip
import re

regWord = re.compile("^(.*?\.\w)\.\d+$")

for i,j in izip(gzip.open(sys.argv[1]), gzip.open(sys.argv[2])):
    i,j = i.strip().split(), j.strip()
    m = regWord.search(i[0])
    if m:
        print m.group(1)+" "+i[0]+" "+m.group(1)+"."+j
    else:
        sys.exit("die "+" ".join(i)+j+"\n")
