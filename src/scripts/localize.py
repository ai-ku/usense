#! /usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Osman Baskaya"

import gzip
import os
import fnmatch

#PATH = '../../run/'
OUT = 'local/' 

def divide_into_files(words, subs):
    filename = ""
    g = open('word.order', 'w')
    f = None
    for i, line in enumerate(words):
        line = line.split('.')[:-1]
        inst = '.'.join(line)
        if filename == inst:
            f.write(subs[i])
        else:
            if f is not None:
                f.close()
            filename = inst
            f = open(OUT + filename, 'w')
            f.write(subs[i])
            g.write(filename + '\n')
    g.close()
            
        
def gold_split():
    """ Creating gold files into gold/ """

    files = [f for f in os.listdir("local") if fnmatch.fnmatch(f, "*.[vn]" )]
    for fname in files:
        os.system("zcat test.gold.gz | grep %s | gzip > gold/%s.gold" % (fname, fname))

def main():
    words = gzip.open('test.word.gz').readlines()
    subs = gzip.open('test.sub.gz').readlines()
    divide_into_files(words, subs)
    gold_split()    



if __name__ == '__main__':
    main()

