import numpy as np
import random

# The number of syllables per word you want to generate: #
sylnum = 1
# The number of words you want to generate: #
outputlines = 10000

# Writes a wordlist output file: #
with open("output1syl.txt", "w") as f:
	# Do this as many times as the number of words you want in the output: #
	for i in range (0, outputlines):
		# Do this for each syllable: #
		for j in range (0, sylnum):
			syl = ''
			# Generate nucleus: #
			vowels = ['a', 'e', 'i', 'o', 'u'] 
			vowelweights = [38.56, 13.96, 19.13, 13.11, 15.24]
			normalized_vw = [vw/sum(vowelweights) for vw in vowelweights]
			nuc = np.random.choice(vowels, 1, p=normalized_vw)
			# Generate onset: #
			onsc1 = ['', 'm', 'n', 'ny', 'p', 't', 'k', 'b', 'd', 'g', 'f', 's', 'z', 'x', 'c', 'l', 'r', 'y', 'w', 'h']
			onsc1weights = [17.69, 9.09, 5.25, 0.87, 4.67, 7.44, 10.00, 5.69, 4.35, 3.50, 1.90, 4.48, 1.03, 1.14, 2.77, 4.43, 2.07, 2.78, 2.49, 3.68]
			normalized_onscw = [onscw/sum(onsc1weights) for onscw in onsc1weights]
			onsc1 = np.random.choice(onsc1, 1, p=normalized_onscw)
			# Generate coda: #
			coda = ['', 'm', 'n', 'ng', 'p', 't', 'k', 's', 'l', 'r', 'y', 'w']
			codaweights = [465.18, 6.63, 21.18, 7.38, 3.03, 8.53, 8.41, 3.72, 7.03, 7.17, 6.46, 2.55]
			normalized_cw = [cw/sum(codaweights) for cw in codaweights]
			coda = np.random.choice(coda, 1, p=normalized_cw)
			if nuc[0] not in ('a', 'e') and coda[0] in ('y', 'w'):
				coda[0] = ''
			# Write to output file: ##
			syl += onsc1[0] + nuc[0] + coda[0]
			oldsyl = syl
			f.write(syl)
		f.write('\n')
