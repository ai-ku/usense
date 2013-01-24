#! /usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Osman Baskaya"

import gzip


GOLD = 'evaluation/unsup_eval/keys/all.key'

def word_split():
    words = gzip.open('test.word.gz').readlines()
    subs = gzip.open('test.sub.gz').readlines()

def get_goldtags(filenames=GOLD):
    return open(filenames).readlines()


#def create_gold_dict():
    #goldtags = get_goldtags()
    #d = {}
    #for line in goldtags:
        #focusword, inst, tag = line.split()
        #d[inst] = tag.split('.')[-1]
    #return d


#def main_goldtag():
    #goldtags = create_gold_dict()
    #g = open('test.gold_new', 'w')
    #f = open('test.gold')
    #for line in f.readlines():
        #inst = line.replace(' ', '.').strip()
        #g.write(inst + ' ' + goldtags[inst] + '\n')
    #g.close()

def main():
    word_split()


if __name__ == '__main__':
    main()

