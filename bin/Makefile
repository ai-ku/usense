all: getdata.py fastsubs scode wordsub wkmeans dists runsc.m readsparse.mexa64

getdata.py: check
	test -e $@ || ln -s ../src/scripts/* .

fastsubs:
	test -e $@ || ln -s ../src/fastsubs .

scode:
	test -e $@ || ln -s ../src/scode .

wordsub:
	test -e $@ || ln -s ../src/wordsub .

wkmeans:
	test -e $@ || ln -s ../src/wkmeans .

dists:
	test -e $@ || ln -s ../src/dists .

runsc.m: check
	cd ../src/spectral;
	test -e $@ || ln -s ../src/spectral/runsc.m
	test -e sc.m || ln -s ../src/spectral/sc.m

readsparse.mexa64:
	test -e $@ || ln -s ../src/readsparse.mexa64

check:
	true
clean:
	rm *py fastsubs *~ *pl