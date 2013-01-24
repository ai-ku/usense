#! /usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import division
__author__ = "Osman Baskaya"

import sys
import fnmatch
import os

#path = "./"
path = "../../results/"


def getscores(fname, wtype='all'):
    words = open(path + 'words').readlines()
    words.sort()

    w = [pos.strip().split('.')[-1] for pos in words]
    
    scores = open(fname).readlines()


    correct = 0
    false = 0
    for i, score in enumerate(scores):
        if w[i] == wtype or wtype == 'all':
            line = score.split()
            correct += int(line[0])
            false += int(line[1])

    try: 
        return correct / (correct+false)
    except:
        return 0


dd = {'0': 'euc', '1': 'cos', '2': 'man', '3': 'max', '4': 'jensen'}

def main():
    if  len(sys.argv) != 2:
        print "usage:", sys.argv[0], "input_file_regex(i.e 'res*')"
        exit()
    file_regex = sys.argv[1]
    for filename in os.listdir(path):
        if fnmatch.fnmatch(filename, file_regex):
            ff = filename.split('.') 
            k = ff[-1]
            dist = dd.get(ff[-2])
            if "iso.dist" in filename:
                dist1 = dd.get(ff[2])
                c = int(ff[3])
                if c in (2, 4, 8, 16):
                    if c > 8:
                        print '{}\t{}\t{}\t{}\t{}\t{}'.format(k, 'all', dist1, dist, c, 
                                                    getscores(path+filename, 'all'))
                    else:
                        for t in ('all', 'v', 'n'):
                            print '{}\t{}\t{}\t{}\t{}\t{}'.format(k, t, dist1, dist, c, 
                                                        getscores(path+filename, t))
            else:
                for t in ('all', 'v', 'n'):
                    print '{}\t{}\t{}\t{}'.format(k, t, dist, getscores(path+filename, t))

if __name__ == '__main__':
    main()

