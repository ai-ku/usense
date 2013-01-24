#! /usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Osman Baskaya"

""" similar to getdists.sh """ 

import sys
import os
import fnmatch
from optparse import OptionParser
import shutil
from scipy.sparse import coo_matrix
from scipy.sparse.linalg import svds
import numpy as np

CWD = os.getcwd()


### PATH ###
filepath = os.path.dirname(os.path.realpath(__file__))
idx = filepath.find('src')
PATH = filepath[:idx]
del filepath, idx


### Input Parsing ###
parser = OptionParser()
parser.add_option("-f", "--function", dest="func_name", default=None,
                  help="function you would like to call", metavar="FUNC_NAME")
parser.add_option("-i", "--inpath", dest="inpath", default=None,
                  help="input path", metavar="INPATH")
parser.add_option("-o", "--outpath", dest="outpath", default=None,
                  help="output path", metavar="OUTPATH")
parser.add_option("-r", "--regex", dest="regex", default=None,
                  help="regex for input files", metavar="REGEX")
parser.add_option("-d", "--distances", dest="distances", default='all',
                  help="distance metric(s)", metavar="DISTANCES")
parser.add_option("-k", "--nfactor", dest="nfactor", default=10,
                  help="number of factor for svd: default 10", metavar="NFACTOR")

(opts, args) = parser.parse_args() 
mandatories = ['func_name', 'inpath', 'regex', 'outpath']


def input_check():
    """ Making sure all mandatory options appeared. """ 
    run = True
    for m in mandatories:
        if not opts.__dict__[m]:
            print "mandatory option is missing: %s" % m
            run = False
    if not run:
        print
        parser.print_help()
        exit(-1)

def get_files(path, regex):
    return [f for f in os.listdir(path) if fnmatch.fnmatch(f, regex)]


### Auxiliary functions ###

def read2sparse(filename):
    
    lines = open(filename).readlines()
    col = []
    row = []
    data = []
    for i, line in enumerate(lines):
        line = line.split()
        c = line[1::2]
        col.extend(c)
        row.extend([i] * len(c))
        data.extend(line[2::2])

    data = map(float, data)
    col = map(int, col)
    col = map(lambda x: x-1, col) # substract 1 from all indexes
    return coo_matrix((data, (row, col)))

def writedense(filename, mat):

    # matrix should be dense and it forms: [ [], [], ... ] 
    f = open(filename, 'w')
    for row in mat:
        f.write(' '.join(map(str, row)))
        f.write('\n')
    f.close()

def check_dest(dest):
    
    n = dest+"_remove"
    if os.path.isdir(n):
        shutil.rmtree(n)
   
    if os.path.isdir(dest):
        shutil.move(dest, n)
    os.mkdir(dest)

### Important Functions ###


func_list = ['calc_dists', 'run_svd']

def calc_dists():
    """../bin/scripts/calcdists.py -f calc_dists -i 
        /home/tyr/playground/usense/run/isolocal -r "*" -d 4 
        2>/home/tyr/calc.err"""
    
    # infile, outfile, d (

    if opts.distances == 'all':
        distances = range(0,5)
    else:
        distances = [int(opts.distances)]

    #FIXME: Jensen'de sikinti var.
    distances = [0,1,2,3]
    dest = opts.outpath
    
    check_dest(dest) # prepare destination directory

    files = get_files(opts.inpath, opts.regex)

    for fn in files:
        print >> sys.stderr, fn
        fulln = os.path.join(opts.inpath, fn)
        #command = "cat %s | ../src/scripts/preinput.py > /home/tyr/Desktop/a.rm" \
                        #% (fn)
        for d in distances:
            #command = "..bin/dists -d %d < %s > %s.dist.%d" % (d, fn, fn, d)
            command = "../bin/dists -d %d < %s > %s/%s.dist.%d" % (d, fulln, dest, fn, d)
            #print command
            os.system(command)
            #exit()


def get_svd(mat, k):
    # mat is a sparse matrix
    m, n = mat.shape
    k = min(k, n)
    print "k is", k
    u, s, v = svds(mat, k=k)
    return (u, s, v)

def run_svd():
    # inpath, outpath, k, regex


    #../bin/scripts/calcdists.py -f run_dimred 
        #   -i /home/tyr/playground/usense/run/pre -r "*" -o svd -k 10
    
    temp = "temp"
    shutil.rmtree(temp)
    os.mkdir(temp)

    dest = opts.outpath
    inpath = opts.inpath
    regex = opts.regex
    k = int(opts.nfactor)

    check_dest(dest) # prepare destination directory
    files = get_files(inpath, regex)
    for fn in files:
        print >> sys.stderr, fn
        fulln = os.path.join(inpath, fn)
        command = "cat %s | ../bin/scripts/preinput.py > %s/%s.preinp" %(fulln, temp, fn)
        os.system(command)
        mat = read2sparse("%s/%s.preinp" % (temp, fn))
        print mat
        exit()
        u, s, v = get_svd(mat, k=k)
        out = os.path.join(dest, fn)
        writedense("%s.%d" % (out, k), u)

def main():
    input_check()
    func = globals()[opts.func_name]
    func()



if __name__ == '__main__':
    main()

