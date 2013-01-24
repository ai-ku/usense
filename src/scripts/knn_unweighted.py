#! /usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import division
import sys
import gzip

def calculate(dist, k, gold):
    true = 0
    total = 0
    for i, instance in enumerate(dist):
        p, p_k = predict(instance.strip(), k, gold)
        if gold[i] == p:
            #print "true", i, gold[i], p, p_k
            true += 1
        #else:
            #print "false", i, gold[i], p, p_k
        total += 1

    print true, total-true, true/total

def predict(instance, k, gold):
    inst = instance.split()
    neighbors = inst[1:k*2+1:2]
    neighbors = map(int, neighbors) #parse to int
    n_tags = dict() # neighbors' tags
    for n in neighbors:
        g = gold[n]
        if g not in n_tags:
            n_tags[g] = 1
        else:
            n_tags[g] += 1

    label = ""
    maxim = -1
    for key in n_tags:
        m = n_tags[key]
        if m > maxim:
            maxim = m
            label = key

    return label, maxim


def main():
    if len(sys.argv) != 4:
        print "usage:", sys.argv[0], "dists_file number_of_neighbor gold_file"
        print sys.argv
        exit()
    infile = sys.argv[1] # input file
    dist = open(infile).readlines() # input file, dists output
    gold = gzip.open(sys.argv[3]).readlines() # gold file
    gold = [line.split()[1] for line in gold]
    k = int(sys.argv[2]) # number of neighbors
    calculate(dist, k, gold)

if __name__ == '__main__':
    main()
