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
from sklearn import cross_validation
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.multiclass import OneVsRestClassifier
from sklearn.grid_search import GridSearchCV
import gzip

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
parser.add_option("-n", "--n_folds", dest="n_folds", default=5,
                  help="number of folds for classifiers: default 10", metavar="NFOLDS")

(opts, args) = parser.parse_args() 
#mandatories = ['func_name', 'inpath', 'regex', 'outpath']
mandatories = []


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

### Auxiliary functions ###

def get_files(path, regex):
    return [f for f in os.listdir(path) if fnmatch.fnmatch(f, regex)]

def get_goldtag(fname):
    gold_path = PATH + 'run/gold/'
    lines = gzip.open(gold_path + fname).readlines()
    return [line.split()[1] for line in lines]

def read2sparse(filename, start=1):
    
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
    if start == 1:
        col = map(lambda x: x-1, col) # substract 1 from all indexes
    return coo_matrix((data, (row, col)))


def create_arff(fname, mat, gold):


    """ create files for Weka input format """
    
    gold = [int(g.split('.')[-1]) for g in gold]
    
    g = set(gold)

    gold = np.matrix(gold)
    
    c = np.concatenate((mat.todense(), gold.T), axis=1)

    ncol = mat.shape[1]
    #@TODO: path
    out = "/home/tyr/Desktop/local.weka/" + fname + '.arff'
    f = open(out, 'w')
    f.write("@relation %s\n\n" % fname)
    for i in xrange(ncol):
        f.write("@attribute a%d numeric\n" % i)
    s = ','.join(map(str, g))
    f.write("@attribute class {%s}\n\n" % s)
    f.write("@data\n")
    #@ Avoid writing two times
    np.savetxt(f, c, delimiter=',', fmt='%5f')
    f.close()
    lines = open(out).readlines()
    f = open(out, 'w')
    for line in lines:
        if line[0] != '@' and len(line) != 1:
            line = line.split(',')
            tag = line[-1].strip()
            tag = str(int(float(tag))) + '\n'
            line[-1] = tag
            f.write(','.join(line))
            f.write('\n')
        else:
            f.write(line)
    f.close()


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


func_list = ['calc_dists', 'run_svd', 'run_logistic']

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
    
    #check_dest(dest) # prepare destination directory

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


def grid_search(clf, X, y, parameters, cv, n_jobs=4):
    model_tunning = GridSearchCV(clf, param_grid=parameters, cv=cv, n_jobs=n_jobs) 
    model_tunning.fit(X, y)
    #print model_tunning.best_score_
    #print model_tunning.best_params_
    return (model_tunning.best_params_, model_tunning.best_score_)


def logistic_score(X, y, n_folds):

    # weak check, #of instance should be equal with gold
    assert X.shape[0] == len(y)

    cv = cross_validation.KFold(len(y), n_folds=n_folds)
    clf = LogisticRegression()
    #clf.verbose = 1
    #clf.fit(X,y)

    parameters = {"C": range(1, 2000, 10)}
    best_param, best_score = grid_search(clf, X, y, parameters, cv, 4)

    print best_param, best_score
    #clf = LogisticRegression(C=best_param['C'])
    #clf.fit(X,y)
    #scores = cross_validation.cross_val_score(clf, X, y, cv=cv, verbose=0, n_jobs=4)
    #print scores.mean(), scores.std()
    #print clf


    #from sklearn.grid_search import GridSearchCV
    #clf2 = OneVsRestClassifier(SVC())
    #model_tunning = GridSearchCV(clf2, param_grid=parameters, cv=cv, n_jobs=4) 
    #model_tunning.fit(X, y)
    #print model_tunning.best_score_
    #print model_tunning.best_params_
    
    #if model_tunning.best_score_ - scores.mean() > 0.01:
        #print model_tunning.best_score_
        #print model_tunning.best_params_

    #print "####"
    
    return best_score

def run_logistic():
    temp = "temp"
    if os.path.isdir(temp):
        shutil.rmtree(temp)
    os.mkdir(temp)

    inpath = opts.inpath
    regex = opts.regex
    n_folds = int(opts.n_folds)

    files = get_files(inpath, regex)

    start = 1
    scores = []
    if  'local' in inpath:
        start = 0 
    for fn in files:

        # b
        #if fn in ['separate.v', 'deploy.v', 'sniff.v']:
            #continue
        if fn not in ['accommodate.v', 'display.n', 'bow.v', 'haunt.v', 'owe.v',
                        ]:
            continue
        #if fn != 'weigh.v':
            #continue
        # e

        #print >> sys.stderr, fn
        fulln = os.path.join(inpath, fn)
        command = "cat %s | ../bin/scripts/preinput.py > %s/%s.preinp" %(fulln, temp, fn)
        os.system(command)
        mat = read2sparse("%s/%s.preinp" % (temp, fn), start)
        gold = get_goldtag(fn + '.gold')
        
        ## b
        #create_arff(fn, mat, gold)
        #continue
        ## e
        score = logistic_score(mat.todense(), gold, n_folds)
        print fn, score
        scores.append(score)
    print sum(scores) / len(scores)

    shutil.rmtree(temp)

def get_svd(mat, k):
    # mat is a sparse matrix
    m, n = mat.shape
    k = min(k, n)
    u, s, v = svds(mat, k=k)
    return (u, s, v)

def run_svd():
    # inpath, outpath, k, regex


    #../bin/scripts/usense.py -f run_dimred 
        #   -i /home/tyr/playground/usense/run/pre -r "*" -o svd -k 10
    temp = "temp"
    if os.path.isdir(temp):
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
        u, s, v = get_svd(mat, k=k)
        out = os.path.join(dest, fn)
        writedense("%s" % out, u)
    
    shutil.rmtree(temp)

def main():
    input_check()
    func = globals()[opts.func_name]
    func()



if __name__ == '__main__':
    main()

