### PATH
TEST_DATA_PATH=../data/test_data/
export NLTK_DATA=../data/wordnet
export bin
TEST_KEY=../data/test.key.gz
export PATH := ../bin:${PATH}
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


clean:
	-rm test.tok.gz test.ngram.gz test.gold.gz test.word.gz test.sub.gz *~