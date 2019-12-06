# WordGen
A program written in Python 3.7 for generating random words based on a predefined phonology. Both deterministic rule-based and character model (LSTM) modes available.

## Features

Wordgen has the following features by default:

### Rule-based mode
1. Example phoneme inventory: /a e i o u m n ŋ ɲ p t k ʔ b d g f s z ʃ h tʃ l r j w/
2. Example phoneme weights based on an average across Swadesh lists from an 100-language sample; statistical differentiation between word-initial onsets, medial onsets and coda consonants
3. Example syllable structure: (C)V(C) with possible onsets /m n ɲ p t k b d g f s z ʃ h tʃ l r j w/ and possible codas /m n ŋ p t k s l r j w/
4. Can specify syllable count and number of output words
5. Example weights have built-in dispreference for repeated syllables with same point of articulation (reduced weight if previous syllable has same POA)
6. Output file format: .txt with newline for each word; syllables separated by dot
7. Post-processing according to assimilation rules included in `patterns.json`

These default settings can be changed by altering the phoneme inventory and weights in the input CSV, or by changing the number of lines/syllables in the output.

### LSTM mode
The submodule `char_rnn` includes [Sherjil Ozair](https://github.com/sherjilozair)'s character-level language model [char-rnn-tensorflow](https://github.com/sherjilozair/char-rnn-tensorflow). The scripts `lstm_train.sh` and `lstm_sample.sh` can be edited as desired. Default input consists of a text file list of lexemes, e.g. the provided `data/wordlist_2.txt`.

## Additional tools
1. `lex_remove.py` removes a specific set of words from the generated wordlist; this functionality is included in `wordgen.py` with the `-r` flag.
2. The `-a` flag can be used to replace IPA characters with ASCII-only according to patterns in `data/ascii_map.json`.
3. `find_overlap.py` can be run to print overlapping lexemes between two wordlists.

# Installation
For easiest setup, create a Python environment using [Miniconda](https://docs.conda.io/en/latest/miniconda.html). After installing conda, run the following to set up your environment:

```
conda create -n wordgen python=3.7
conda activate wordgen
pip install -r requirements.txt
```

This will install all necessary Python dependencies and ensure you are using the correct versions.

# Usage

## Rule-based

The script should be called from root directory as follows:

```
python wordgen.py [options]
```

Rules mode is run by default. The logic for the rule-based mode is hard-coded in `wordgen.py`. The phoneme weights are read from a CSV-formatted file, for example the provided `data/example.csv`. The `read_from_csv` function in `wordgen.py` assumes the following structure, where the phonotactic contexts are represented by rules in the leftmost column and weights for each rule in the respective phoneme columns.

| Rules | | | | | | 
| --- | --- | --- | --- | --- | --- | 
| V | a | e | i | o | ... |
| "all" | 1.0 | 1.0 | 1.0 | 1.0 | ... |
| C | _ | m | n | p | ... |
| "onsc1,rule 1" | 1.0 | 1.0 | 1.0 | 1.0 | ... |
| "onsc1,rule 2" | 1.0 | 1.0 | 1.0 | 1.0 | ... |
| "coda,rule 1" | 1.0 | 1.0 | 1.0 | 1.0 | ... |

Consonantal rule names should be in quotation marks and formatted as "[segment],[context]"; the vowel rule in the example applies to all nuclei. The hard-coded logic in `wordgen.py` must be changed if different syllable structures are desired, such as additional onset or coda consonants, vowel length rules, diphthongs, tones etc.

### Options

#### Custom phoneme weights

A custom input CSV file with different rules and weights can be provided by the `-c` flag; the default path is `data/example.csv`.

```
python wordgen.py -c path/to/mycsv
```

If you want to use a different input format, edit the `read_from_csv` function in `wordgen.py`.

#### Number of syllables and output words

By default, a random number of syllables is chosen for each output word (option `-n 0`), but a specific number can be specified using the `-n` flag. The default number of output words is 3000, but a different number can be specified using the `-o` flag.

```
python wordgen.py -n 2 -o 1000
```

## Character-level language model

