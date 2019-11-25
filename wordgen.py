import numpy as np
import pandas as pd
import random
import re
import os

# NB - 'q' represents glottal stop.
# The number of syllables per word you want to generate: #
sylnum = 2
# The number of words you want to generate: #
outputlines = 3000
# Patterns for post-processing (assimilation rules):
pats = {
			r'a\.a': 'a.qa',
			r'e\.e': 'e.qe',
			r'i\.i': 'i.qi',
			r'o\.o': 'o.qo',
			r'u\.u': 'u.qu',

			r'iy\.': 'i.',
			r'iw\.': 'i.',
			r'oy\.': 'o.',
			r'ow\.': 'o.',
			r'uy\.': 'u.',
			r'uw\.': 'u.',

			r'm\.n': 'n.n',
			r'm\.ny': 'n.ny',
			r'm\.t': 'n.t',
			r'm\.d': 'n.d',
			r'm\.c': 'n.c',
			r'n\.m': 'm.m',
			r'n\.p': 'm.p',
			r'n\.k': 'ng.k',
			r'n\.b': 'm.b',
			r'n\.g': 'ng.g',
			r'n\.y': '.ny',
			r'l\.r': 'r.r',
			r'r\.l': 'l.l'
}


def read_from_csv(datafile):
	df = pd.read_csv(datafile)
	rules = df['Rules'].dropna(how='all')
	vowels = df.iloc[:1,1:].dropna(axis=1)
	vowel_list = vowels.values.flatten().tolist()
	vowel_weights = df.iloc[1:2,1:len(vowel_list)+1].values.flatten().tolist()
	# Replace null consonant nan with underscore:
	if df.iloc[2:3,1:2].isnull().values.any():
		df.iloc[2:3,1:2] = '_'
	consonants = df.iloc[2:3,1:].dropna(axis=1)
	cons_list = consonants.values.flatten().tolist()
	cons_weights_map = {}
	idx = 0
	for rule in rules.values.flatten().tolist():
		cons_weights = []
		if len(rule.split(',')) > 1:
			cons_weights = df.iloc[idx:idx+1,1:len(cons_list)+1].fillna(value=0.0).values.flatten().tolist()
			cons_weights = [float(i) for i in cons_weights]
			cons_weights_map[rule] = cons_weights
		idx += 1
	vowel_df = pd.DataFrame(vowel_weights, index=vowel_list)
	cons_df = pd.DataFrame(cons_weights_map, index=cons_list)
	return vowel_df, cons_df


def random(chars, weights):
	normw = [w/sum(weights) for w in weights]
	choice = np.random.choice(chars, 1, p=normw)
	return choice


def write_file(vowel_df, cons_df):
	# Writes a wordlist output file: #
	with open("output.txt", "w") as f:
		# Do this as many times as the number of words you want in the output: #
		for i in range (0, outputlines):
			# Do this for each syllable: #
			for j in range (0, sylnum):
				if j == 0:
					oldsyl = ''
				syl = ''
				# Generate nucleus: #
				nuc = random(list(vowel_df.index), [float(i) for i in vowel_df.iloc[:,0].tolist()])
				# Generate onset: #
				onsc1 = ['' if c == '_' else c for c in list(cons_df.index)]
				# First syllable: #
				if oldsyl == '':
					onsc1weights = [float(i) for i in cons_df["onsc1,first syl"].tolist()]
					onsc1 = random(onsc1, onsc1weights)
				# After first syllable: #
				else:
					if oldsyl[0] == 'p' or oldsyl[0] == 'b' or oldsyl[0] == 'f':
						onsc1weights = [float(i) for i in cons_df["onsc1,prec labial ons"].tolist()]
						onsc1 = random(onsc1, onsc1weights)
					elif oldsyl[0] == 't' or oldsyl[0] == 'd' or oldsyl[0] == 's':
						onsc1weights = [float(i) for i in cons_df["onsc1,prec alveolar ons"].tolist()]
						onsc1 = random(onsc1, onsc1weights)
					elif oldsyl[0] == 'k' or oldsyl[0] == 'g':
						onsc1weights = [float(i) for i in cons_df["onsc1,prec velar ons"].tolist()]
						onsc1 = random(onsc1, onsc1weights)
					elif oldsyl[0] == 'm' or oldsyl[0] == 'n':
						onsc1weights = [float(i) for i in cons_df["onsc1,prec nasal ons"].tolist()]
						onsc1 = random(onsc1, onsc1weights)
					elif oldsyl[0] == 'l' or oldsyl[0] == 'r':
						onsc1weights = [float(i) for i in cons_df["onsc1,prec liquid ons"].tolist()]
						onsc1 = random(onsc1, onsc1weights)
					elif oldsyl[0] == 'z' or oldsyl[0] == 'x' or oldsyl[0] == 'c':
						onsc1weights = [float(i) for i in cons_df["onsc1,prec sibilant ons"].tolist()]
						onsc1 = random(onsc1, onsc1weights)
					elif oldsyl[0] == 'h' or oldsyl[0] == 'q':
						onsc1weights = [float(i) for i in cons_df["onsc1,prec glottal ons"].tolist()]
						onsc1 = random(onsc1, onsc1weights)
					elif oldsyl[0] == 'w' or oldsyl[0] == 'y':
						onsc1weights = [float(i) for i in cons_df["onsc1,prec semivowel ons"].tolist()]
						onsc1 = random(onsc1, onsc1weights)
					else:
						onsc1weights = [float(i) for i in cons_df["onsc1,prec no ons"].tolist()]
						onsc1 = random(onsc1, onsc1weights)
				# Generate coda: #
				coda = ['' if c == '_' else c for c in list(cons_df.index)]
				# Before penultimate syllable: #
				if j < sylnum-2:
					if len(oldsyl) > 2:
						if oldsyl[2] == 'm' or oldsyl[2] == 'n' or oldsyl[2] == 'ng':
							codaweights = [float(i) for i in cons_df["coda,before penult prec nasal coda"].tolist()]
							coda = random(coda, codaweights)
						elif oldsyl[2] == 'p':
							codaweights = [float(i) for i in cons_df["coda,before penult prec p coda"].tolist()]
							coda = random(coda, codaweights)
						elif oldsyl[2] == 't':
							codaweights = [float(i) for i in cons_df["coda,before penult prec t coda"].tolist()]
							coda = random(coda, codaweights)
						elif oldsyl[2] == 'k':
							codaweights = [float(i) for i in cons_df["coda,before penult prec k coda"].tolist()]
							coda = random(coda, codaweights)
						elif oldsyl[2] == 's':
							codaweights = [float(i) for i in cons_df["coda,before penult prec s coda"].tolist()]
							coda = random(coda, codaweights)
						elif oldsyl[2] == 'l' or oldsyl[2] == 'r':
							codaweights = [float(i) for i in cons_df["coda,before penult prec liquid coda"].tolist()]
							coda = random(coda, codaweights)
						else:
							codaweights = [float(i) for i in cons_df["coda,before penult prec semivowel coda"].tolist()]
							coda = random(coda, codaweights)
					else:
						codaweights = [float(i) for i in cons_df["coda,before penult prec no coda"].tolist()]
						coda = random(coda, codaweights)
				# Penultimate syllable: #
				if j == sylnum-2:
					if len(oldsyl) > 2:
						if oldsyl[2] == 'm' or oldsyl[2] == 'n' or oldsyl[2] == 'ng':
							codaweights = [float(i) for i in cons_df["coda,penult prec nasal coda"].tolist()]
							coda = random(coda, codaweights)
						elif oldsyl[2] == 'p':
							codaweights = [float(i) for i in cons_df["coda,penult prec p coda"].tolist()]
							coda = random(coda, codaweights)
						elif oldsyl[2] == 't':
							codaweights = [float(i) for i in cons_df["coda,penult prec t coda"].tolist()]
							coda = random(coda, codaweights)
						elif oldsyl[2] == 'k':
							codaweights = [float(i) for i in cons_df["coda,penult prec k coda"].tolist()]
							coda = random(coda, codaweights)
						elif oldsyl[2] == 's':
							codaweights = [float(i) for i in cons_df["coda,penult prec s coda"].tolist()]
							coda = random(coda, codaweights)
						elif oldsyl[2] == 'l' or oldsyl[2] == 'r':
							codaweights = [float(i) for i in cons_df["coda,penult prec liquid coda"].tolist()]
							coda = random(coda, codaweights)
						else:
							codaweights = [float(i) for i in cons_df["coda,penult prec semivowel coda"].tolist()]
							coda = random(coda, codaweights)
					else:
						codaweights = [float(i) for i in cons_df["coda,penult prec no coda"].tolist()]
						coda = random(coda, codaweights)
				# Final syllable: #
				if j == sylnum-1:
					if len(oldsyl) > 2:
						if oldsyl[2] == 'm' or oldsyl[2] == 'n' or oldsyl[2] == 'ng':
							codaweights = [float(i) for i in cons_df["coda,last syl prec nasal coda"].tolist()]
							coda = random(coda, codaweights)
						elif oldsyl[2] == 'p':
							codaweights = [float(i) for i in cons_df["coda,last syl prec p coda"].tolist()]
							coda = random(coda, codaweights)
						elif oldsyl[2] == 't':
							codaweights = [float(i) for i in cons_df["coda,last syl prec t coda"].tolist()]
							coda = random(coda, codaweights)
						elif oldsyl[2] == 'k':
							codaweights = [float(i) for i in cons_df["coda,last syl prec k coda"].tolist()]
							coda = random(coda, codaweights)
						elif oldsyl[2] == 's':
							codaweights = [float(i) for i in cons_df["coda,last syl prec s coda"].tolist()]
							coda = random(coda, codaweights)
						elif oldsyl[2] == 'l' or oldsyl[2] == 'r':
							codaweights = [float(i) for i in cons_df["coda,last syl prec liquid coda"].tolist()]
							coda = random(coda, codaweights)
						else:
							codaweights = [float(i) for i in cons_df["coda,last syl prec semivowel coda"].tolist()]
							coda = random(coda, codaweights)
					else:
						codaweights = [float(i) for i in cons_df["coda,last syl prec no coda"].tolist()]
						coda = random(coda, codaweights)
				# Write to output file: ##
				syl += onsc1[0] + nuc[0] + coda[0] + '.'
				oldsyl = syl
				f.write(syl)
			f.write('\n')


def post_process():
	# Post-process output: #
	with open("output.txt", "r") as f1:
		seen = set()
		with open("wordlist-%dsyl.txt" % sylnum, "w") as f2:
			for line in f1:
				if line not in seen:
					seen.add(line)
					for k, v in pats.items():
						sub = re.sub(k, v, line)
						line = sub
					f2.write(line)
	# Trash intermediate output:
	if os.path.exists("output.txt"):
		os.remove("output.txt")


def main():
	datafile = 'data.csv'
	vowel_df, cons_df = read_from_csv(datafile)
	write_file(vowel_df, cons_df)
	post_process()

if __name__ == '__main__':
	main()
