#! /usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import division
import sys
import gzip
import os
import math
from collections import defaultdict as dd


PATH = '/home/tyr/playground/usense/'

def calc_perp(filename):
    lines = gzip.open(filename).readlines()
    d = dd(list)
    total = 0
    for line in lines:
        total += 1
        inst, key = line.split()
        d[key].append(inst)

    entropy = 0.0
    for key in d.keys():
        p = len(d[key]) / total
        entropy += -p * math.log(p, 2)

    return 2 ** entropy, total

def mfs_score(filename):
    #print filename
    lines = gzip.open(filename).readlines()
    d = dd(list)
    total = 0
    for line in lines:
        total += 1
        inst, key = line.split()
        d[key].append(inst)

    maximum = -1
    max_sense = None

    for key in d.keys():
        n = len(d[key]) 
        if maximum < n:
            maximum = n
            max_sense = key

    #print len(d[max_sense]), total - len(d[max_sense]), len(d[max_sense]) / total
    return len(d[max_sense]), total - len(d[max_sense]), len(d[max_sense]) / total

def main_mfs():
    path = PATH + 'run/local/'
    count = 0
    total_cor = 0
    total_false = 0
    for filename in os.listdir(path):
        if 'gold' in filename:
            count += 1
            #mfs_score(path + filename)
            correct, false, mfs = mfs_score(path + filename)
            total_cor += correct
            total_false += false
    print total_cor, total_false, total_cor / (total_cor + total_false)


def main_perp():
    path = PATH + 'run/local/'
    total_perp = 0
    total_inst = 0
    count = 0
    for filename in os.listdir(path):
        if 'gold' in filename:
            count += 1
            perp, num_inst = calc_perp(path + filename)
            total_perp += perp
            total_inst += num_inst

    print total_perp / count, total_inst
    

def main():
    #experiment = sys.argv[1]
    #wordname = sys.argv[2]
    #if experiment == 'calc_perp':
        #calc_perp(wordname)
    main_mfs()
    #main_perp()

if __name__ == '__main__':
    main()

