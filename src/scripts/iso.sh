#!/bin/csh

set MATLAB_PATH = "/usr/local/MATLAB/R2012a/bin/matlab -nojvm -nodisplay"
set PWD = `pwd`
set files = `ls $PWD/local.dist/*dist*`

cd ../src/iso/
foreach fname ($files)

    echo $fname
    $MATLAB_PATH -r "runiso $fname" > $*.iso 2> $*.iso.err

    #cat $fname | ../src/scripts/preinput.py > $fname.pre  
    #../bin/dists -d $d < $fname.pre > $fname.dist.$d
    #rm $fname.pre
end
cd $PWD
