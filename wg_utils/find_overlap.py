import os
import string
import argparse

wordset = set()
found = set()


def populate_wordset(file_1):
	# Populate wordlist from file 1:
	with open(file_1, "r") as f1:
		for line in f1:
			wordset.add(line.strip('\n').lower().translate(str.maketrans('', '', string.punctuation)))


def populate_found(file_2):
	# Populate set of words found in file 2:
	with open(file_2, "r") as f2:
		for line in f2:
			lexeme = line.strip('\n').lower().translate(str.maketrans('', '', string.punctuation))
			if lexeme in wordset:
				print('overlap: ' + lexeme)
				found.add(lexeme)

def write_new_list(output):
	# Write new wordlist of overlaps to output:
	with open(output, "w") as f:
		for lexeme in found:
			f.write(lexeme + '\n')


def main():
	parser = argparse.ArgumentParser()
	parser.add_argument("-f1", "--file_1", help="First wordlist file to compare.", default="data/wordlist_1.txt")
	parser.add_argument("-f2", "--file_2", help="Second wordlist file to compare.", default="data/wordlist_2.txt")
	parser.add_argument("-o", "--output", help="Path to output file.", default="output/overlap.txt")
	args = parser.parse_args()
	
	file_1 = args.file_1
	file_2 = args.file_2
	output = args.output

	populate_wordset(file_1)
	populate_found(file_2)
	write_new_list(output)
		

if __name__ == '__main__':
	main()
