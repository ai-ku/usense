#!/usr/bin/env python


import sys
import gzip

dic = {}
for line in gzip.open(sys.argv[1]):
    l = line.strip().split()
    if l[1] not in dic:
        dic[l[1]] = l[2]
    else:
        sys.exit("duplicate key:"+l[1]+"\n")

for line in sys.stdin:
    l = line.strip().split()
    word = ".".join(l)
    if word not in dic:
        sys.exit("missing key:"+ word + "\n")
    tag = dic[word]
    print word+ "\t" + tag





