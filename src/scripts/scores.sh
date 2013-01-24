#!/bin/csh
set results = `ls ../results/res*`
foreach result ($results)
    echo $result
end
#python ../src/scripts/scores.py > ../results/SCORES2
