import os
import string


class LexRemover:
	def populate_wordset(self):
		# Populate set from original wordlist:
		with open("wordlist-%dsyl.txt" % self.sylnum, "r") as f1:
			for line in f1:
				self.wordset.add(line.strip('\n').replace('.',''))


	def populate_found(self):
		# Populate set of lexicon words found in wordlist:
		with open(self.lex_filepath, "r") as f2:
			for line in f2:
				lsplit = line.split('=')
				lexeme = lsplit[0].translate(str.maketrans('', '', string.punctuation))
				if lexeme in self.wordset:
					print('found: ' + lexeme)
					self.found.add(lexeme)

	def write_new_list(self):
		# Write new wordlist (with lexicon words removed) to intermediate output:
		with open("wordlist-%dsyl.txt" % self.sylnum, "r") as f1:
			with open("output.txt", "w") as f2:
				for line in f1:
					if line.strip('\n').replace('.','') not in self.found:
						f2.write(line)

	def post_process(self):
		# Replace original wordlist file with new edited list:
		with open("output.txt", "r") as f1:
			with open("wordlist-%dsyl.txt" % self.sylnum, "w") as f2:
				lines = f1.readlines()
				for line in lines:
					f2.write(line)
		# Trash intermediate output:
		if os.path.exists("output.txt"):
			os.remove("output.txt")


	def __init__(self, sylnum, lex_filepath):
		self.sylnum = 2
		self.lex_filepath = 'lexicon.txt'
		self.wordset = set()
		self.found = set()