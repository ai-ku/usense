#! /usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Osman Baskaya"

""" tree tagger to sentence """
import sys
import gzip

files = map(lambda x: gzip.open('train.'+x+'.gz', 'w'), "tok pos lemma".split())
lines = [[], [], []]

targetword=""

is_start = True
for line in sys.stdin:
    if is_start:
        targetword = line
        is_start = False
    else:
        if line.startswith("</s>"):
            for i in xrange(3):
                lines[i].append('\n')
                files[i].write(' '.join(lines[i]))
                lines[i] = []
            is_start = True
        else:
            line = line.strip().split('\t')
            if len(line) != 3:
                print >> sys.stderr, line
                line = ["<unknown>", 'EE', '<unknown>']
            for i in xrange(3):
                lines[i].append(line[i])

map(lambda f: f.close(), files)


