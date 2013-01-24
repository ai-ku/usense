#!/bin/sh
#TODO 
#dosya ismi res, onu duzelt
#res dosyalarini silmen gerekli, >> ediyor cunku.
# JENSEN hala sikintili
# removing the old results
rm -rf ../results/$1*

SCRIPTS="../../src/scripts"
RESULTS="../../results"

cd $1
files=$2
for fname in $files
    do
        for k in 5 10 15
            do
                echo $fname
                orig=`echo $fname | sed s/.dist.*//`
                gold=$orig.gold
                if [ $1 = "iso.dist" ]; then
                    #access.n.dist.0.iso.c16.dist.0
                    d1=`echo $fname | sed "s/.iso.*//" | sed "s/.*dist.//"`
                    d2=`echo $fname | sed "s/.*iso//" | sed "s/.*dist.//"`
                    c=`echo $fname | sed "s/.*iso.c//" | sed "s/.dist.*//"`
                    # format: distance1, # of c, distance2, # of neighbor
                    out="$RESULTS/$1.$d1.$c.$d2.$k"
                else
                    d=`echo $fname | sed s/$orig.dist.//`
                    # format: distance1, # of neighbor
                    out="$RESULTS/$1.$d.$k"
                fi
                cat $fname | $SCRIPTS/knnsparse.py ../gold/$gold $k >> $out
            done
    done

python $SCRIPTS/scores.py $1.* > $RESULTS/$1-SCORES
