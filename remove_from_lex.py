import os
import string

sylnum = 1
lex_filepath = 'lexicon.txt'

wordset = set()
found = set()

# Populate set from original wordlist:
with open("wordlist-%dsyl.txt" % sylnum, "r") as f1:
	for line in f1:
		wordset.add(line.strip('\n').replace('.',''))

# Populate set of lexicon words found in wordlist:
with open(lex_filepath, "r") as f2:
	for line in f2:
		lsplit = line.split('=')
		lexeme = lsplit[0].translate(str.maketrans('', '', string.punctuation))
		if lexeme in wordset:
			print('found: ' + lexeme)
			found.add(lexeme)

# Write new wordlist (with lexicon words removed) to intermediate output:
with open("wordlist-%dsyl.txt" % sylnum, "r") as f1:
	with open("output.txt", "w") as f2:
		for line in f1:
			if line.strip('\n').replace('.','') not in found:
				f2.write(line)

# Replace original wordlist file with new edited list:
with open("output.txt", "r") as f1:
	with open("wordlist-%dsyl.txt" % sylnum, "w") as f2:
		lines = f1.readlines()
		for line in lines:
			f2.write(line)

# Trash intermediate output:
if os.path.exists("output.txt"):
	os.remove("output.txt")