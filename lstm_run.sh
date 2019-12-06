#!/usr/bin/env bash

echo "Training LSTM..."

DATA_DIR=data
RNN_SIZE=128
N_LAYERS=2
SEQ_LENGTH=10
N_EPOCHS=50
LR=0.0001
MDY=$(date +"%m-%d-%y")
OUT_DIR=output/$MDY-h$RNN_SIZE-l$N_LAYERS-seq$SEQ_LENGTH-e$N_EPOCHS
SAVE_DIR=$OUT_DIR/checkpoints
TRAIN_LOG=$OUT_DIR/train_log.txt

mkdir -p $OUT_DIR

now=$(date +"%D %T")
echo "Starting at: $now" >> $TRAIN_LOG

python3 char_rnn/train.py --data_dir=$DATA_DIR \
	--save_dir=$SAVE_DIR \
	--log_dir=$OUT_DIR \
	--model='lstm' \
	--rnn_size=$RNN_SIZE \
	--num_layers=$N_LAYERS \
	--seq_length=$SEQ_LENGTH \
	--num_epochs=$N_EPOCHS \
	--learning_rate=$LR >> $TRAIN_LOG

now=$(date +"%D %T")
echo "Ending at: $now" >> $TRAIN_LOG
echo "Finished training!"

NUM_CHARS=30000

echo "Sampling..."

python3 char_rnn/sample.py --save_dir=$SAVE_DIR \
	-n $NUM_CHARS \
	--sample 1 >> $OUT_DIR/sample.txt

# Remove duplicate lines:
sort $OUT_DIR/sample.txt | uniq -u > $OUT_DIR/temp_sample.txt
shuf $OUT_DIR/temp_sample.txt > $OUT_DIR/sample.txt
rm $OUT_DIR/temp_sample.txt

echo "Finished sampling!"