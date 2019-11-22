# wordgen
A script written in Python 3.7 for generating random words based on a predefined phonology. 

This sample script has the following features:

1. Phoneme inventory: /a e i o u m n ŋ ɲ p t k ʔ b d g f s z ʃ h tʃ l r j w/
2. Phoneme weights based on an average across Swadesh lists from an 100-language sample; statistical differentiation between word-initial onsets, medial onsets and coda consonants
3. Syllable structure: (C)V(C) with possible onsets /m n ɲ p t k b d g f s z ʃ h tʃ l r j w/ and possible codas /m n ŋ p t k s l r j w/
4. Can specify syllable count and number of output words
5. Built-in dispreference for repeated syllables with same point of articulation (reduced weight if previous syllable has same POA)
6. Output file format: .txt with newline for each word; syllables separated by dot
7. Post-processing according to assimilation rules included in wordgen.py

These default settings can be changed by altering the phoneme inventory and weights, or by changing the number of lines/syllables in the output.

The additional script remove_from_lex.py can be used to remove a specific set of words from the generated wordlist.
