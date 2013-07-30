#! /usr/bin/python
# -*- coding: utf-8 -*-
import gzip
from itertools import izip

pos_file = gzip.open('sampled.train.pos.gz')
tok_file = gzip.open('sampled.train.tok.gz')


for tok, pos in izip(tok_file, pos_file):
    tok = tok.split()
    pos = pos.split()
    for t, p in izip(tok, pos):
        if p[0] in ['V', 'J', 'N']:
            print t, p
