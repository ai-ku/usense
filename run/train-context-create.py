#! /usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Osman Baskaya"

import gzip
import sys
from itertools import count, izip

target_word = ""

lemma_file = gzip.open("train.lemma.gz")
pos_file = gzip.open("train.pos.gz")
tok_file = gzip.open("train.tok.gz")
tw_file = gzip.open("train.gz") #target words


for l_tok, l_pos, l_lem, t_line, line in izip(tok_file, pos_file, lemma_file, tw_file, count(1)):
    l_tok = l_tok.split()
    l_pos = l_pos.split()
    l_lem = l_lem.split()
    t_line = t_line.split()[0].split('.')
    tw = t_line[0]
    tw_pos = t_line[1]
    lemma_count = t_line[2]
    if not (len(l_tok) == len(l_pos) == len(l_lem)):
        sys.stderr.write(str(line) + ': ' + ' '.join(l_tok) + "\n")
        sys.stderr.write(str(line) + ': ' + ' '.join(l_pos) + "\n")
        sys.stderr.write(str(line) + ': ' + ' '.join(l_lem) + "\n")
        continue
    for i in xrange(len(l_lem)):
        if l_lem[i] == tw and l_pos[i][0].lower() == tw_pos:
            print "%s <%s.%s.%s> %s" % (' '.join(l_tok[i - 3:i]),
                                        l_lem[i],
                                        l_pos[i][0].lower(),
                                        lemma_count,
                                        ' '.join(l_tok[i + 1:i + 4]))
            break # only one instance per line

