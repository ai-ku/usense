#!/bin/sh
SCRIPTS="../../src/scripts"
BIN="../../bin"
TEMP="../temp"

mkdir temp

cd $1
files=$2

for fname in $files
    do
        if [ $1 = "local" ]; then
            cat $fname | $SCRIPTS/preinput.py > $TEMP/$fname.pre
        else
            echo $fname | $SCRIPTS/predist.py $TEMP
        fi
        for d in 0 1 2 3 4
            do
            $BIN/dists -d $d < $TEMP/$fname.pre > ../$1.dist/$fname.dist.$d
        done
done

rm -rf $TEMP
