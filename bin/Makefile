all: getdata.py fastsubs

getdata.py: check
	test -e $@ || ln -s ../src/scripts/* .

fastsubs:
	test -e $@ || ln -s ../src/fastsubs .

check:
	true
clean:
	rm *py fastsubs