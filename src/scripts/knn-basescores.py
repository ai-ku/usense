#! /usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import division
import sys
import gzip
from random import randint

def random_test(lines):
    goldtags = [line.split()[1].strip() for line in lines]
    s = list(set(goldtags))
    num_inst = len(goldtags)
    t = len(s)
    correct = 0
    for instance in goldtags:
        r = randint(0,t-1)
        if instance == s[r]:
            correct += 1
    # correct, false, mean
    return (correct, num_inst - correct, correct / num_inst)


    
def main():
    for fi in sys.stdin:
        infile = fi.strip()
        goldtags = gzip.open(infile).readlines()
        correct, false, mean = random_test(goldtags)
        print "{}\t{}\t{}".format(correct, false, mean)

if __name__ == '__main__':
    main()

