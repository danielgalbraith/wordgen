#!/usr/bin/env bash

echo "Sampling..."
mkdir -p output

SAVE_DIR='output/checkpoints'
OUT_DIR='output'
NUM_CHARS=30000

python3 char_rnn/sample.py --save_dir=$SAVE_DIR \
	-n $NUM_CHARS \
	--sample 1 >> $OUT_DIR/sample.txt

# Remove duplicate lines:
sort $OUT_DIR/sample.txt | uniq -u > $OUT_DIR/temp_sample.txt
shuf $OUT_DIR/temp_sample.txt > $OUT_DIR/sample.txt
rm $OUT_DIR/temp_sample.txt

echo "Finished sampling!"
