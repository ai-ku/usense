#!/bin/csh

set files = `ls local/*.[vn]`

foreach fname ($files)

    echo $fname
    cat $fname | ../src/scripts/preinput.py > $fname.pre  
    ../bin/dists -d $d < $fname.pre > $fname.dist.$d
    rm $fname.pre
end
