### PATH
export NLTK_DATA=../data/wordnet
export PATH := ../bin:${PATH}
MATLAB_PATH=/mnt/opt/matlab/linux64/R2011a/bin/matlab -nojvm -nodisplay

## PARAMETERS
TEST_KEY=../data/test.key.gz
TEST_DATA_PATH=../data/test_data/
SEED=1

### BIN SETUP

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

##Get gold cluster numbers
test.nclu.gz: test.pos.gz
	numbercluster.py $< | gzip > $@

#Get word labels
test.word.gz: test.gold.gz
	zcat test.gold.gz | perl -lane 'print $$1 if /^(.*\.\w)\.\d+\s/;' | gzip > $@

### DISTANCE METRICS

KNN=10000
NCPU=40
#Manhattan
DIS=2
test.knn.gz: test.sub.gz  ## KNN=1000 KNN_METRIC=1 NCPU=24: time=21h40m, wc=1173766 2348705766 18877273290
	zcat $< | preinput.py | dists -k ${KNN} -v -d ${DIS} -p ${NCPU} 2> knn${DIS}.err | gzip > $@ 

## CLUSTERING

%.spectral: %.knn.gz
	${MATLAB_PATH} < ../bin/runsc.m > $*.spectral 2> $*.spectral.err
	gzip $*.spectral.c*

KM_OPTIONS=
test.c%.kmeans.gz: test.spectral.c%.gz
	zcat $< | wkmeans -k $* -r 5 -s ${SEED} -v | gzip > $@


### FASTSUBS options:
FS_NSUB=100 # go until you have this many substitutes
FS_PSUB=1.0 # or this much cumulative probability
FS_OPTIONS=-n ${FS_NSUB} -p ${FS_PSUB}

TRAIN_LM=../data/wsj.lm.gz

%.sub.gz: %.ngram.gz ${TRAIN_LM} test.word.gz
	zcat $< | fastsubs ${FS_OPTIONS} ${TRAIN_LM} | grep -P '^<X>\t' | cut -f2- | gzip > $@.tmp
	zpaste test.word.gz $@.tmp > $@
	rm $@.tmp

### WORDSUB 

WORDSUB=1 # Number of random substitutes per word
WS_OPTIONS=-n ${WORDSUB} -s ${SEED}

%.pairs.gz: %.sub.gz ## WS_NSUB=64: time=20m55s wc=75121024 150242048 809663253
	perl -le 'print "$<" for 1..${WORDSUB}' | xargs zcat | grep -v '^</s>' | wordsub -s ${SEED} |gzip > $@

### SCODE ###
SC_OPTIONS=-r 1 -i 50 -d 25 -z 0.166 -p 50 -u 0.2 -s ${SEED} -v -e 1

%.yscode.gz: %.pairs.gz 
	zcat $< | scode ${SC_OPTIONS} | gzip > $@

KM_OPTIONS=-k 200 -r 50 -s ${SEED} -v

%.xykmeans.gz: %.yscode.gz
	zcat $< | wkmeans ${KM_OPTIONS} | gzip > $@

%.ykmeans.gz: %.yscode.gz	
	zcat $< | perl -lane 'print join("\t",@F[25 .. $$#F])' | wkmeans ${KM_OPTIONS} | gzip > $@

%.ans: test.gold.gz %.gz 
	getans.py  $<  $*.gz > $@

%.eval: %.ans
	java -jar fscore.jar $< ../evaluation/unsup_eval/keys/all.key n >$*.fn.eval
	java -jar fscore.jar $< ../evaluation/unsup_eval/keys/all.key v > $*.fv.eval
	java -jar fscore.jar $< ../evaluation/unsup_eval/keys/all.key all > $*.fa.eval
	java -jar vmeasure.jar $< ../evaluation/unsup_eval/keys/all.key n >$*.vn.eval
	java -jar vmeasure.jar $< ../evaluation/unsup_eval/keys/all.key v >$*.vv.eval
	java -jar vmeasure.jar $< ../evaluation/unsup_eval/keys/all.key all >$*.va.eval
	tail -n 1 $*.*.eval > $@

clean:
	-rm test.tok.gz test.ngram.gz test.gold.gz test.word.gz test.sub.gz *ans *~

.PRECIOUS: %.ans test.c%.kmeans.gz %.xykmeans.gz %.ykmeans.gz %.ans