all: getdata.py fastsubs runiso.m readsparse.mexa64 runpca.m

getdata.py: check
	test -e $@ || ln -s ../src/scripts/*

fastsubs:
	test -e $@ || ln -s ../src/fastsubs .

runiso.m: check
	cd ../src/iso
	test -e $@ || ln -s ../src/iso/runiso.m
	test -e IsomapII.m || ln -s ../src/iso/IsomapII.m
	test -e dijkstra.mexa64 || ln -s ../src/iso/dijkstra.mexa64
	test -e dfun.m || ln -s ../src/iso/dfun.m
	test -e L2_distance.m || ln -s ../src/iso/L2_distance.m

runpca.m: check
	cd ../src/pca
	test -e $@ || ln -s ../src/pca/runpca.m


readsparse.mexa64:
	test -e $@ || ln -s ../src/readsparse.mexa64

check:
	true

clean:
	rm *py fastsubs
