#! /usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Osman Baskaya"
#import re
from bs4 import BeautifulSoup
import sys
import time
import os

start_time = time.clock()

files = sys.argv[1:]
print >> sys.stderr, "# of files:", len(files)

#fast version
count=0
for filename in files:
    print >> sys.stderr, "{} processing".format(filename),
    tw = os.path.basename(filename)[:-4] # get basename and remove .xml
    soup = BeautifulSoup(open(filename), 'xml')
    train = soup.find(tw + '.train')
    if len(train) < 1:
        print >> sys.stderr, "No instance found.."
        continue
    print >> sys.stderr, "{} instances found".format(len(train))
    for instance in train:
        # tw.n.1 -> tw.n.1001
        ins = instance.name.split('.')
        ins_name = '.'.join(ins[:2])
        inst_id = int(ins[2]) + 1000
        ins = "{}.{}".format(ins_name, inst_id)
        print "{}\t{}".format(ins, instance.text.encode('utf-8'))
        count += 1

print >> sys.stderr, time.clock() - start_time,  "seconds"
print >> sys.stderr, "# of total instances: {}".format(count)


#old version
#regex = re.compile(r'<(\w+\.\w\.\d+)>(.*)</\1>')
##FIXME: Performansi berbat yukardaki regex'in. Rewrite
#for filename in files:
    #print >> sys.stderr, "{} processing".format(filename),
    #ff = open(filename).read()
    #lines = regex.findall(ff)
    #print >> sys.stderr, "{} instances found".format(len(lines))
    #for inst, text in lines:
        #print "{}\t{}".format(inst, text)
