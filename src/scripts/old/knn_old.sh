#!/bin/csh

rm -rf ../results/res*
cd local/
set files = `ls *.[vn]`
cd ../

foreach fname ($files)
    echo $fname
    zcat test.gold.gz | grep $fname | gzip > local/$fname.gold
    foreach d (0 1 2 3 4)
        #echo $d
        foreach k (5 10 15 20)
            #echo $k
            cat local/$fname.dist.$d | ../src/scripts/knnsparse.py local/$fname.gold $k >> ../results/res.$k.$d
        end
    end
end
python ../src/scripts/scores.py > ../results/SCORES


