### PATH
TEST_DATA_PATH=../data/test_data/
export NLTK_DATA=../data/wordnet
export bin
TEST_KEY=../data/test.key.gz
export PATH := ../bin:${PATH}
SCRIPTS=../src/scripts
BIN_PATH=../bin/
MATLAB_PATH=/usr/local/MATLAB/R2012a/bin/matlab -nojvm -nodisplay
###

bin:
	cd ../bin; make

#Get the word pos id word_ngram_frame
test.tok.gz:
	find ${TEST_DATA_PATH} -type f | grep .xml | getdata.py | gzip > $@ 

#Get ngram and gold tag set
test.ngram.gz: test.tok.gz
	zcat $< | cut -f1 | getgold.py ${TEST_KEY} | gzip >test.gold.gz
	zcat $< | cut -f2 | gzip > $@

#Get pos tags
test.pos.gz: test.gold.gz
	zcat test.gold.gz | perl -lane 'print $$F[1]' | gzip > $@

#Get word labels
test.word.gz: test.gold.gz
	zcat test.gold.gz | perl -lane 'print $$F[0]' | gzip > $@


### FASTSUBS options:
FS_NSUB=100 # go until you have this many substitutes
FS_PSUB=1.0 # or this much cumulative probability
FS_OPTIONS=-n ${FS_NSUB} -p ${FS_PSUB}

TRAIN_LM=../data/wsj.lm.gz

%.sub.gz: %.ngram.gz ${TRAIN_LM}
	zcat $< | fastsubs ${FS_OPTIONS} ${TRAIN_LM} | grep -P '^<X>\t' | gzip > $@
	
localize: test.sub.gz test.word.gz test.gold.gz
	@rm -rf local gold
	mkdir local gold
	../src/scripts/localize.py
	#../src/scripts/getdists.sh

%.dist: %
	# calculating distances examp: local.dist
	rm -rf $@
	-mkdir $@
	../src/scripts/getdists.sh $* "*" #2>$@.err

%.knn: %.dist
	../src/scripts/knn.sh $< "*"

	
knn_exp_unweight:
	rm -r ../results/knn_unw*
	../src/scripts/knn_unweighted.sh

knn_exp:
	#../src/scripts/knn_old.sh eski
	../src/scripts/knn.sh local "*.[vn]"

random_gold:
	#gold tag sayisi kadar random secenek ile sonuc
	find local/ -type f | grep .gold | sort | ${SCRIPTS}/knn-basescores.py > ../results/random
	python ${SCRIPTS}/scores.py random

run.logistic:
	../bin/scripts/usense.py -f run_logistic -i local/ -r "*" -n 10

run.iso:
	# some file removing needed
	rm -rf iso/
	-mkdir iso
	iso.sh
	#gzip $*.iso.c*

run.pca:
	rm -rf pca/
	-mkdir pca

run.svd%:
	#example: make run.svd10
	@rm -rf svd$*
	../bin/scripts/usense.py -f run_svd -i local/ -r "*" -o svd$* -k $*

clean:
	-rm -r test.tok.gz test.ngram.gz test.gold.gz test.word.gz test.sub.gz local/ *~

#.PHONY: iso
