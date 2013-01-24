#! /usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Osman Baskaya"
import sys


def main():
    if len(sys.argv) != 2:
        print "Error! Usage: sys.argv[0] output_path"
        exit()

    out_folder = sys.argv[1]
    for fi  in sys.stdin:
        infile = fi.strip()
        f = open(infile)
        #print >> sys.stderr, "Reading", infile
        print >> sys.stderr, "Reading", infile
        lines = f.readlines()
        fname =  infile.split('/')[-1]
        g = open(out_folder + "/" + fname + ".pre", 'w')
        for line in lines:
            #r = map(float, line.split())
            r = line.split()
            s = len(r)
            w = zip(map(str, range(1, s+1)), r)
            values = reduce(lambda e1, e2: e1+e2, w)
            g.write("%d " % s)
            g.write(' '.join(values))
            g.write('\n')
        g.close()

if __name__ == '__main__':
    main()

