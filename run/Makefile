### PATH
export NLTK_DATA=../data/wordnet
export PATH := ../bin:.:${PATH}
BIN_PATH=../bin/
MATLAB_PATH=/mnt/opt/matlab/linux64/R2011a/bin/matlab -nojvm -nodisplay
TEST_NOUN=$(shell find ../data/training_data/nouns -name "*.xml" | sort)
TEST_VERB=$(shell find ../data/training_data/verbs -name "*.xml" | sort)
GOLD_ALL=../evaluation/unsup_eval/keys/all.key


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
	zcat test.gold.gz | perl -lane 'print $$1 if /^(.*\.\w\.\d+)\s/;' | gzip > $@

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

#TRAIN_LM=../data/wsj.lm.gz
TRAIN_LM=train.lm.gz

test.sub.gz: test.ngram.gz ${TRAIN_LM} test.word.gz
	zcat $< | fastsubs ${FS_OPTIONS} ${TRAIN_LM} | grep -P '^<X>\t' | cut -f2- | gzip > $@.tmp
	zpaste.py test.word.gz $@.tmp | awk '{$1="<"$1">"; print}' | > $@
	rm $@.tmp

### WORDSUB 

WORDSUB=100 # Number of random substitutes per word
WS_OPTIONS=-n ${WORDSUB} -s ${SEED}

%.pairs.gz: %.sub.gz ## WS_NSUB=64: time=20m55s wc=75121024 150242048 809663253
	perl -le 'print "$<" for 1..${WORDSUB}' | xargs zcat | grep -v '^</s>' | wordsub -s ${SEED} |gzip > $@


### RPART options:[??del or comment out]
RPART=2000 # Number of random partitions
NTEST=8915
RP_OPTIONS=-n ${NTEST} -p ${RPART} -s ${SEED}

%.rpart.pairs.gz: %.knn.gz %.word.gz ## RPART=65536: time=2m55s wc=1173766 2347532 14694702
	zcat $< | rpart.pl ${RP_OPTIONS} | join.pl $*.word.gz - | gzip > $@

### SCODE ###
SC_OPTIONS=-a -r 1 -d 25 -z 0.166 -p 50 -u 0.2 -s ${SEED} -v

%.scode.gz: %.pairs.100.gz 
	zcat $< | scode ${SC_OPTIONS} | gzip > $@

KM_OPTIONS=-k 200 -r 50 -s ${SEED} -v

%.kmeans.gz: %.scode.gz	
	zcat $< | perl -lane 'print join("\t",@F[0 .. 24])' | wkmeans ${KM_OPTIONS} | gzip > $@

%.xykmeans.gz: %.scode.gz
	zcat $< | wkmeans ${KM_OPTIONS} | gzip > $@

%.ykmeans.gz: %.scode.gz	
	zcat $< | perl -lane 'print join("\t",@F[25 .. $$#F])' | wkmeans ${KM_OPTIONS} | gzip > $@

%.ans: test.gold.gz %.gz 
	getans.py  $<  $*.gz > $@

train.gz: # wc = 879807 74055363 419437222
	./train-extract.py ${TEST_NOUN} ${TEST_VERB} | gzip > $@.tmp
	mv $@.tmp $@

train.tag.gz: train.gz # 1611.06s user 205.23s system wc=77468294 230649766
	zcat train.gz | awk '{print $$0 "</s>"}' | \
	../bin/tree-tagger/cmd/tree-tagger-english | gzip > $@

train.pos.gz train.lemma.gz train.tok.gz: train.tag.gz ./tagger2sentence.py
	zcat train.tag.gz | ./tagger2sentence.py 2>tag2sent.err

train.context.gz: ./train-context-create.py train.pos.gz train.tok.gz train.lemma.gz
	./train-context-create.py 2>train.context.err | gzip > $@

all.sub.1.gz all.sub.2.gz all.sub.3.gz: train.lm.gz train.context.gz
	zcat train.context.gz  | tail -n +000001 | head -250000 |\
	fastsubs ${FS_OPTIONS} train.lm.gz | gzip > all.sub.1.gz &\
	zcat train.context.gz | tail -n +250001 | head -250000 |\
	fastsubs ${FS_OPTIONS} train.lm.gz | gzip > all.sub.2.gz &\
	zcat train.context.gz | tail -n +500001 |\
	fastsubs ${FS_OPTIONS} train.lm.gz | gzip > all.sub.3.gz &\
	wait

target.sub.gz: all.sub.1.gz all.sub.2.gz all.sub.3.gz test.sub.gz # wc=744209 149586009 1481146411
	zcat $^ | grep -P '^<\w+\.\w+' | gzip > $@

pairs.100.gz: #target.sub.gz
	perl -le 'print "target.sub.gz" for 1..100' | xargs zcat | wordsub -s ${SEED} |gzip > $@

test.pairs.gz: pairs.100.gz
	zcat $< | grep -P "^<\w+\..\.\d{1,3}>" | gzip > $@

### HDP EXPERIMENTS ###

TEST_WORDS=$(shell ls ../data/test_data/* | grep '.xml' | sed 's/.xml//g' | sort)
NSAMPLE=1000
hdp-input-create: test.pairs.gz #target.sub.gz
	python wordsub-collect.py $< ${SEED} ${NSAMPLE} ${TEST_WORDS}

num_test_instances.all.txt: hdp-wsi/ ./test-inst-num-usense.py
	test-inst-num-usense.py > hdp-wsi/wsi_input/example/$@

# alpha experiment
eval/hdp.exp-alpha-%.ans: 
	cd hdp-wsi/; ./run_wsi.sh 0.1 $*; wait
	cp hdp-wsi/wsi_output/tm_wsi $@
	cp hdp-wsi/wsi_output/tm_wsi.topics eval/hdp.exp-alpha-$*.topics
	wait

# gamma experiment
eval/hdp.exp-gamma-%.ans:
	cd hdp-wsi/; ./run_wsi.sh $* 1; wait
	cp hdp-wsi/wsi_output/tm_wsi $@
	cp hdp-wsi/wsi_output/tm_wsi.topics eval/hdp.exp-gamma-$*.topics
	wait

hdp-input-stats.tab:
	for tw in ${TEST_WORDS}; do\
		cat input-hdp-test/$$tw.lemma  | awk '{print $$0 "<sentence>"}' |\
		../bin/tree-tagger/cmd/tree-tagger-english | ./hdp-vocab-stat.py $$tw >> $@;\
		wait;\
	done

### POS-BASED EXPERIMENTS ###

sampled.train.tok.gz sampled.train.pos.gz sampled.train.lemma.gz: train.tok.gz \
	train.pos.gz train.lemma.gz sample-lines.py
	./sample-lines.py ${SEED} 80000 train.tok.gz train.pos.gz train.lemma.gz

global.sub1.gz global.sub2.gz: sampled.train.tok.gz # train.lm.gz
	zcat sampled.train.tok.gz | tail -n +00001 | head -20000 |\
	fastsubs ${FS_OPTIONS} train.lm.gz | gzip > global.sub1.gz &\
	zcat sampled.train.tok.gz | tail -n +20001 | head -20000 |\
	fastsubs ${FS_OPTIONS} train.lm.gz | gzip > global.sub2.gz &\
	wait

global.sub3.gz global.sub4.gz: sampled.train.tok.gz
	zcat sampled.train.tok.gz | tail -n +40001 | head -20000 |\
	fastsubs ${FS_OPTIONS} train.lm.gz | gzip > global.sub3.gz &\
	zcat sampled.train.tok.gz | tail -n +60001 | \
	fastsubs ${FS_OPTIONS} train.lm.gz | gzip > global.sub4.gz &\
	wait

global.sub.gz: #global.sub1.gz global.sub2.gz global.sub3.gz global.sub4.gz
	zcat $^ | grep -v -P '^</s>' | gzip > $@

verb.sub.gz noun.sub.gz: global.sub.gz
	zcat $< | ./split-vnj.py sampled.train.lemma.gz sampled.train.pos.gz 

verb.pairs.100.gz: verb.sub.gz pairs.100.gz
	perl -le 'print "$<" for 1..100' | xargs zcat | wordsub -s ${SEED} > $@.tmp
	zcat pairs.100.gz | grep -P "^<\w+\.v\.\d{1,3}>" >> $@.tmp
	cat $@.tmp | gzip > $@
	rm -rf $@.tmp

noun.pairs.100.gz: noun.sub.gz pairs.100.gz
	perl -le 'print "$<" for 1..100' | xargs zcat | wordsub -s ${SEED} > $@.tmp
	zcat pairs.100.gz | grep -P "^<\w+\.n\.\d{1,3}>" >> $@.tmp
	cat $@.tmp | gzip > $@
	rm -rf $@.tmp

%.scode.pos.gz: %.pairs.100.gz
	zcat $< | scode -i 50 ${SC_OPTIONS} | gzip > $@

pos-cluster-test: noun.scode.pos.gz verb.scode.pos.gz
	./y-cluster-pos-test.py ${SEED} 350 400 450 500 #4 8 16 24 32 40 60 70 80 100 120 150 180 210

eval/pos.%.ans: eval/noun.%.ans eval/verb.%.ans
	cat $^ > $@
	wc $@

eval/%.scores: eval/%.ans
	java -jar ${BIN_PATH}ssp.jar -s ${GOLD_ALL} $< > eval/$*.ssp.eval
	java -jar ${BIN_PATH}fscore.jar eval/$*.ans ${GOLD_ALL} all > eval/$*.fa.eval
	java -jar ${BIN_PATH}vmeasure.jar eval/$*.ans ${GOLD_ALL}  all > eval/$*.va.eval
	tail -n 2 eval/$*.*.eval > $@
	cat $@
	./topics-stat.py $< > eval/$*.dist
	tail -3 eval/$*.dist
	rm -rf eval/*.eval

clean:
	-rm test.tok.gz test.ngram.gz test.gold.gz test.word.gz test.sub.gz *ans *~

.PRECIOUS: %.ans test.c%.kmeans.gz %.xykmeans.gz %.ykmeans.gz %.ans %.yscode.gz \
	train.sub.gz
.SECONDARY:
