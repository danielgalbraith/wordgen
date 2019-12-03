#!/usr/bin/env bash

echo "Training LSTM..."
mkdir -p output

DATA_DIR='data'
SAVE_DIR='output/checkpoints'
OUT_DIR='output'
TRAIN_LOG='output/train_log.txt'

now=$(date +"%D %T")
echo "Starting at: $now" >> $TRAIN_LOG

python3 char_rnn/train.py --data_dir=$DATA_DIR \
	--save_dir=$SAVE_DIR \
	--log_dir=$OUT_DIR \
	--model='lstm' \
	--seq_length=10 >> $TRAIN_LOG

now=$(date +"%D %T")
echo "Ending at: $now" >> $TRAIN_LOG
echo "Finished training!"