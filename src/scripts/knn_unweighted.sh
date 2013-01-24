#!/bin/csh

set files = `ls local/*.[vn]`

set k = 10

foreach d (0 1 2 3 4)
echo "Distance $d"
foreach fname ($files)
    ../src/scripts/knn_unweighted.py $fname.dist.$d $k $fname.gold >> ../results/knn_unw.$k.$d
end
end
