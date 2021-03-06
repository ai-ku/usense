#!/usr/bin/env python

from lxml import etree
from collections import defaultdict as dd
from nltk.stem.wordnet import WordNetLemmatizer
import sys
import re
###
regIsWord = re.compile("^(.*?)\.(\w)\.(\d+)$");
###
lmtzr = WordNetLemmatizer()
###
dict = {"half-straightened":"straighten","figger":"figure", "figgered":"figure","lay":"lie","lah":"lie"}

class WordTarget(object):
    def __init__(self):
        self.text = dd(lambda: "")
        self.currentWord = None
        self.currentPos = None
        self.currentSense = None
        self.isTargetSentence = None

    def start(self, tag, attrib):
        m = regIsWord.search(tag)
        if m:
            self.currentWord = m.groups()[0]
            self.currentPos = m.groups()[1]
            self.currentSense = int(m.groups()[2])

        elif tag == "TargetSentence":
            self.isTargetSentence = True

    def end(self,tag):
        if tag == "TargetSentence":
            self.isTargetSentence = False 

    def data(self, data):
        if self.isTargetSentence:
            self.text[(self.currentWord,self.currentPos, self.currentSense)] += data.encode('utf-8')
    def close(self):
        return self.text

def get_window(word, tag, sentence, n = 4):
    ss = sentence.strip().split()
    tar,st,end= -1,0,0
    for i in range(len(ss)):
        tt = ss[i].lower()
        word_1 = word[:-1]
        if  tt == word:
            tar = i
        elif lmtzr.lemmatize(tt,tag) == word:            
            tar = i
        elif tt in dict and dict[tt] == word:
            tar = i
            
    if tar == -1:
        return None
    else:
        ss[tar] = "<X>"

    if tar - n + 1 >= 0:
        st = tar - n + 1
    else:
        st = 0

    if tar + n - 1 < len(ss):
        end = tar + n
    else:
        end = len(ss)
#    print st,i,end,ss[tar],ss[st], ss[end-1]
    return ss[st:end]

#print >> sys.stderr ,"Stem:",Stemmer.stem("sniffing")
#sys.exit(1)

#read 
for fi in sys.stdin:
    infile = fi.strip()
    print >> sys.stderr, "Reading ",infile
    parser = etree.XMLParser(target = WordTarget())
    results = etree.parse(infile, parser)
    for k,v in sorted(results.items(), key=lambda x: x[0][2]):
        w = get_window(k[0],k[1],v)
        if w:
            print " ".join(map(str,k)) + "\t"+" ".join(w)
        else:
            tag = " ".join(map(str,k))
            print >> sys.stderr, "Warning/Error Missed["+tag+ "]\t"+v

