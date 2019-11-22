import numpy as np
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


def random(chars, weights):
	normw = [w/sum(weights) for w in weights]
	choice = np.random.choice(chars, 1, p=normw)
	return choice


def write_file():
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
				vowels = ['a', 'e', 'i', 'o', 'u'] 
				vowelweights = [38.56, 13.96, 19.13, 13.11, 15.24]
				nuc = random(vowels, vowelweights)
				# Generate onset: #
				# First syllable: #
				if oldsyl == '':
					onsc1 = ['', 'm', 'n', 'ny', 'p', 't', 'k', 'b', 'd', 'g', 'f', 's', 'z', 'x', 'c', 'l', 'r', 'y', 'w', 'h']
					onsc1weights = [17.69, 9.09, 5.25, 0.87, 4.67, 7.44, 10.00, 5.69, 4.35, 3.50, 1.90, 4.48, 1.03, 1.14, 2.77, 4.43, 2.07, 2.78, 2.49, 3.68]
					onsc1 = random(onsc1, onsc1weights)
				# After first syllable: #
				else:
					if oldsyl[0] == 'p' or oldsyl[0] == 'b' or oldsyl[0] == 'f':
						onsc1= ['', 'm', 'n', 'ny', 'p', 't', 'k', 'q', 'b', 'd', 'g', 'f', 's', 'z', 'x', 'c', 'l', 'r', 'y', 'w', 'h']
						onsc1weights = [10.29, 6.55, 8.62, 1.05, 0.3, 9.25, 7.36, 1.64, 0.48, 2.89, 3.72, 0.17, 4.20, 0.64, 0.97, 1.33, 9.27, 9.65, 2.25, 2.18, 3.93]
						onsc1 = random(onsc1, onsc1weights)
					elif oldsyl[0] == 't' or oldsyl[0] == 'd' or oldsyl[0] == 's':
						onsc1 = ['', 'm', 'n', 'ny', 'p', 't', 'k', 'q', 'b', 'd', 'g', 'f', 's', 'z', 'x', 'c', 'l', 'r', 'y', 'w', 'h']
						onsc1weights = [9.47, 6.55, 8.62, 1.05, 3.05, 0.93, 7.36, 1.64, 4.81, 0.29, 3.72, 1.67, 0.42, 0.64, 0.97, 1.33, 9.27, 9.65, 2.25, 2.18, 3.93]
						onsc1 = random(onsc1, onsc1weights)
					elif oldsyl[0] == 'k' or oldsyl[0] == 'g':
						onsc1 = ['', 'm', 'n', 'ny', 'p', 't', 'k', 'q', 'b', 'd', 'g', 'f', 's', 'z', 'x', 'c', 'l', 'r', 'y', 'w', 'h']
						onsc1weights = [10.11, 6.55, 8.62, 1.05, 3.05, 9.25, 0.74, 1.64, 4.81, 2.89, 0.37, 1.67, 4.20, 0.64, 0.97, 1.33, 9.27, 9.65, 2.25, 2.18, 3.93]
						onsc1 = random(onsc1, onsc1weights)
					elif oldsyl[0] == 'm' or oldsyl[0] == 'n':
						onsc1 = ['', 'm', 'n', 'ny', 'p', 't', 'k', 'q', 'b', 'd', 'g', 'f', 's', 'z', 'x', 'c', 'l', 'r', 'y', 'w', 'h']
						onsc1weights = [9.49, 0.66, 0.86, 0.11, 3.05, 9.25, 7.36, 1.64, 4.81, 2.89, 3.72, 1.67, 4.20, 0.64, 0.97, 1.33, 9.27, 9.65, 2.25, 2.18, 3.93]
						onsc1 = random(onsc1, onsc1weights)
					elif oldsyl[0] == 'l' or oldsyl[0] == 'r':
						onsc1 = ['', 'm', 'n', 'ny', 'p', 't', 'k', 'q', 'b', 'd', 'g', 'f', 's', 'z', 'x', 'c', 'l', 'r', 'y', 'w', 'h']
						onsc1weights = [9.16, 6.55, 8.62, 1.05, 3.05, 9.25, 7.36, 1.64, 4.81, 2.89, 3.72, 1.67, 4.20, 0.64, 0.97, 1.33, 0.93, 0.97, 2.25, 2.18, 3.93]
						onsc1 = random(onsc1, onsc1weights)
					elif oldsyl[0] == 'z' or oldsyl[0] == 'x' or oldsyl[0] == 'c':
						onsc1 = ['', 'm', 'n', 'ny', 'p', 't', 'k', 'q', 'b', 'd', 'g', 'f', 's', 'z', 'x', 'c', 'l', 'r', 'y', 'w', 'h']
						onsc1weights = [11.09, 6.55, 8.62, 1.05, 3.05, 9.25, 7.36, 1.64, 4.81, 2.89, 3.72, 1.67, 4.20, 0.06, 0.09, 0.13, 9.27, 9.65, 2.25, 2.18, 3.93]
						onsc1 = random(onsc1, onsc1weights)
					elif oldsyl[0] == 'h' or oldsyl[0] == 'q':
						onsc1 = ['', 'm', 'n', 'ny', 'p', 't', 'k', 'q', 'b', 'd', 'g', 'f', 's', 'z', 'x', 'c', 'l', 'r', 'y', 'w', 'h']
						onsc1weights = [10.78, 6.55, 8.62, 1.05, 3.05, 9.25, 7.36, 0.16, 4.81, 2.89, 3.72, 1.67, 4.20, 0.64, 0.97, 1.33, 9.27, 9.65, 2.25, 2.18, 0.39]
						onsc1 = random(onsc1, onsc1weights)
					elif oldsyl[0] == 'w' or oldsyl[0] == 'y':
						onsc1 = ['', 'm', 'n', 'ny', 'p', 't', 'k', 'q', 'b', 'd', 'g', 'f', 's', 'z', 'x', 'c', 'l', 'r', 'y', 'w', 'h']
						onsc1weights = [10.92, 6.55, 8.62, 1.05, 3.05, 9.25, 7.36, 1.64, 4.81, 2.89, 3.72, 1.67, 4.20, 0.64, 0.97, 1.33, 9.27, 9.65, 0.22, 0.22, 3.93]
						onsc1 = random(onsc1, onsc1weights)
					else:
						onsc1 = ['', 'm', 'n', 'ny', 'p', 't', 'k', 'q', 'b', 'd', 'g', 'f', 's', 'z', 'x', 'c', 'l', 'r', 'y', 'w', 'h']
						onsc1weights = [11.45, 6.55, 8.62, 1.05, 3.05, 9.25, 7.36, 1.64, 4.81, 2.89, 3.72, 1.67, 4.20, 0.64, 0.97, 1.33, 9.27, 9.65, 2.25, 2.18, 3.93]
						onsc1 = random(onsc1, onsc1weights)
				# Generate coda: #
				# Before penultimate syllable: #
				if j < sylnum-2:
					if len(oldsyl) > 2:
						if oldsyl[2] == 'm' or oldsyl[2] == 'n' or oldsyl[2] == 'ng':
							coda = ['', 'm', 'n', 'ng', 'p', 't', 'k', 's', 'l', 'r', 'y', 'w']
							codaweights = [201.68, 0.66, 2.12, 0.74, 3.03, 8.53, 8.41, 3.72, 7.03, 7.17, 6.46, 2.55]
							coda = random(coda, codaweights)
						elif oldsyl[2] == 'p':
							coda = ['', 'm', 'n', 'ng', 'p', 't', 'k', 's', 'l', 'r', 'y', 'w']
							codaweights = [317.44, 6.63, 21.18, 7.38, 0.3, 8.53, 8.41, 3.72, 7.03, 7.17, 6.46, 2.55]
							coda = random(coda, codaweights)
						elif oldsyl[2] == 't':
							coda = ['', 'm', 'n', 'ng', 'p', 't', 'k', 's', 'l', 'r', 'y', 'w']
							codaweights = [297.64, 6.63, 21.18, 7.38, 3.03, 0.85, 8.41, 3.72, 7.03, 7.17, 6.46, 2.55]
							coda = random(coda, codaweights)
						elif oldsyl[2] == 'k':
							coda = ['', 'm', 'n', 'ng', 'p', 't', 'k', 's', 'l', 'r', 'y', 'w']
							codaweights = [298.08, 6.63, 21.18, 7.38, 3.03, 8.53, 0.84, 3.72, 7.03, 7.17, 6.46, 2.55]
							coda = random(coda, codaweights)
						elif oldsyl[2] == 's':
							coda = ['', 'm', 'n', 'ng', 'p', 't', 'k', 's', 'l', 'r', 'y', 'w']
							codaweights = [314.96, 6.63, 21.18, 7.38, 3.03, 8.53, 8.41, 0.37, 7.03, 7.17, 6.46, 2.55]
							coda = random(coda, codaweights)
						elif oldsyl[2] == 'l' or oldsyl[2] == 'r':
							coda = ['', 'm', 'n', 'ng', 'p', 't', 'k', 's', 'l', 'r', 'y', 'w']
							codaweights = [277.24, 6.63, 21.18, 7.38, 3.03, 8.53, 8.41, 3.72, 0.7, 0.72, 6.46, 2.55]
							coda = random(coda, codaweights)
						elif oldsyl[2] == 'y' or oldsyl[2] == 'w':
							coda = ['', 'm', 'n', 'ng', 'p', 't', 'k', 's', 'l', 'r', 'y', 'w']
							codaweights = [295.96, 6.63, 21.18, 7.38, 3.03, 8.53, 8.41, 3.72, 7.03, 7.17, 0.65, 0.26]
							coda = random(coda, codaweights)
						else:
							coda = ['', 'm', 'n', 'ng', 'p', 't', 'k', 's', 'l', 'r', 'y', 'w']
							codaweights = [328.36, 6.63, 21.18, 7.38, 3.03, 8.53, 8.41, 3.72, 7.03, 7.17, 6.46, 2.55]
							coda = random(coda, codaweights)
					else:
						coda = ['', 'm', 'n', 'ng', 'p', 't', 'k', 's', 'l', 'r', 'y', 'w']
						codaweights = [328.36, 6.63, 21.18, 7.38, 3.03, 8.53, 8.41, 3.72, 7.03, 7.17, 6.46, 2.55]
						coda = random(coda, codaweights)
				# Penultimate syllable: #
				if j == sylnum-2:
					if len(oldsyl) > 2:
						if oldsyl[2] == 'm' or oldsyl[2] == 'n' or oldsyl[2] == 'ng':
							coda = ['', 'm', 'n', 'ng', 'p', 't', 'k', 's', 'l', 'r', 'y', 'w']
							codaweights = [117.65, 0.66, 2.12, 0.74, 3.03, 8.53, 8.41, 3.72, 7.03, 7.17, 6.46, 2.55]
							coda = random(coda, codaweights)
						elif oldsyl[2] == 'p':
							coda = ['', 'm', 'n', 'ng', 'p', 't', 'k', 's', 'l', 'r', 'y', 'w']
							codaweights = [185.17, 6.63, 21.18, 7.38, 0.3, 8.53, 8.41, 3.72, 7.03, 7.17, 6.46, 2.55]
							coda = random(coda, codaweights)
						elif oldsyl[2] == 't':
							coda = ['', 'm', 'n', 'ng', 'p', 't', 'k', 's', 'l', 'r', 'y', 'w']
							codaweights = [173.62, 6.63, 21.18, 7.38, 3.03, 0.85, 8.41, 3.72, 7.03, 7.17, 6.46, 2.55]
							coda = random(coda, codaweights)
						elif oldsyl[2] == 'k':
							coda = ['', 'm', 'n', 'ng', 'p', 't', 'k', 's', 'l', 'r', 'y', 'w']
							codaweights = [173.88, 6.63, 21.18, 7.38, 3.03, 8.53, 0.84, 3.72, 7.03, 7.17, 6.46, 2.55]
							coda = random(coda, codaweights)
						elif oldsyl[2] == 's':
							coda = ['', 'm', 'n', 'ng', 'p', 't', 'k', 's', 'l', 'r', 'y', 'w']
							codaweights = [183.73, 6.63, 21.18, 7.38, 3.03, 8.53, 8.41, 0.37, 7.03, 7.17, 6.46, 2.55]
							coda = random(coda, codaweights)
						elif oldsyl[2] == 'l' or oldsyl[2] == 'r':
							coda = ['', 'm', 'n', 'ng', 'p', 't', 'k', 's', 'l', 'r', 'y', 'w']
							codaweights = [161.72, 6.63, 21.18, 7.38, 3.03, 8.53, 8.41, 3.72, 0.7, 0.72, 6.46, 2.55]
							coda = random(coda, codaweights)
						elif oldsyl[2] == 'y' or oldsyl[2] == 'w':
							coda = ['', 'm', 'n', 'ng', 'p', 't', 'k', 's', 'l', 'r', 'y', 'w']
							codaweights = [172.64, 6.63, 21.18, 7.38, 3.03, 8.53, 8.41, 3.72, 7.03, 7.17, 0.65, 0.26]
							coda = random(coda, codaweights)
						else:
							coda = ['', 'm', 'n', 'ng', 'p', 't', 'k', 's', 'l', 'r', 'y', 'w']
							codaweights = [191.54, 6.63, 21.18, 7.38, 3.03, 8.53, 8.41, 3.72, 7.03, 7.17, 6.46, 2.55]
							coda = random(coda, codaweights)
					else:
						coda = ['', 'm', 'n', 'ng', 'p', 't', 'k', 's', 'l', 'r', 'y', 'w']
						codaweights = [191.54, 6.63, 21.18, 7.38, 3.03, 8.53, 8.41, 3.72, 7.03, 7.17, 6.46, 2.55]
						coda = random(coda, codaweights)
				# Final syllable: #
				if j == sylnum-1:
					if len(oldsyl) > 2:
						if oldsyl[2] == 'm' or oldsyl[2] == 'n' or oldsyl[2] == 'ng':
							coda = ['', 'm', 'n', 'ng', 'p', 't', 'k', 's', 'l', 'r', 'y', 'w']
							codaweights = [89.25, 0.66, 2.12, 0.74, 3.03, 8.53, 8.41, 3.72, 7.03, 7.17, 6.46, 2.55]
							coda = random(coda, codaweights)
						elif oldsyl[2] == 'p':
							coda = ['', 'm', 'n', 'ng', 'p', 't', 'k', 's', 'l', 'r', 'y', 'w']
							codaweights = [140.45, 6.63, 21.18, 7.38, 0.3, 8.53, 8.41, 3.72, 7.03, 7.17, 6.46, 2.55]
							coda = random(coda, codaweights)
						elif oldsyl[2] == 't':
							coda = ['', 'm', 'n', 'ng', 'p', 't', 'k', 's', 'l', 'r', 'y', 'w']
							codaweights = [131.71, 6.63, 21.18, 7.38, 3.03, 0.85, 8.41, 3.72, 7.03, 7.17, 6.46, 2.55]
							coda = random(coda, codaweights)
						elif oldsyl[2] == 'k':
							coda = ['', 'm', 'n', 'ng', 'p', 't', 'k', 's', 'l', 'r', 'y', 'w']
							codaweights = [131.9, 6.63, 21.18, 7.38, 3.03, 8.53, 0.84, 3.72, 7.03, 7.17, 6.46, 2.55]
							coda = random(coda, codaweights)
						elif oldsyl[2] == 's':
							coda = ['', 'm', 'n', 'ng', 'p', 't', 'k', 's', 'l', 'r', 'y', 'w']
							codaweights = [139.38, 6.63, 21.18, 7.38, 3.03, 8.53, 8.41, 0.37, 7.03, 7.17, 6.46, 2.55]
							coda = random(coda, codaweights)
						elif oldsyl[2] == 'l' or oldsyl[2] == 'r':
							coda = ['', 'm', 'n', 'ng', 'p', 't', 'k', 's', 'l', 'r', 'y', 'w']
							codaweights = [122.68, 6.63, 21.18, 7.38, 3.03, 8.53, 8.41, 3.72, 0.7, 0.72, 6.46, 2.55]
							coda = random(coda, codaweights)
						elif oldsyl[2] == 'y' or oldsyl[2] == 'w':
							coda = ['', 'm', 'n', 'ng', 'p', 't', 'k', 's', 'l', 'r', 'y', 'w']
							codaweights = [130.97, 6.63, 21.18, 7.38, 3.03, 8.53, 8.41, 3.72, 7.03, 7.17, 0.65, 0.26]
							coda = random(coda, codaweights)
						else:
							coda = ['', 'm', 'n', 'ng', 'p', 't', 'k', 's', 'l', 'r', 'y', 'w']
							codaweights = [145.3, 6.63, 21.18, 7.38, 3.03, 8.53, 8.41, 3.72, 7.03, 7.17, 6.46, 2.55]
							coda = random(coda, codaweights)
					else:
						coda = ['', 'm', 'n', 'ng', 'p', 't', 'k', 's', 'l', 'r', 'y', 'w']
						codaweights = [145.3, 6.63, 21.18, 7.38, 3.03, 8.53, 8.41, 3.72, 7.03, 7.17, 6.46, 2.55]
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
	write_file()
	post_process()

if __name__ == '__main__':
	main()
