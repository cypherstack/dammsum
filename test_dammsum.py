from dammsum import *
from typing import List
import pytest
from random import randrange

k = 11 # word list contains 2**11 == 2048 words
m = 12 # number of words in a seed (excluding checksum)
words_path = 'words.txt' # relative path to word list

# Fetch the word list
def get_words() -> List[str]:
	words = []
	try:
		words_file = open(words_path,'r')
		for line in words_file:
			words.append(line.strip())
		return words
	except:
		raise IOError

# Test that generated seeds are not obviously broken
def test_generate():
	d = DammSum(k, m, get_words())
	seed_1 = d.generate()
	seed_2 = d.generate()

	# Seeds should be of the correct length
	assert len(seed_1) == m + 1
	assert len(seed_2) == m + 1

	# Seeds should verify
	assert d.verify(seed_1)
	assert d.verify(seed_2)

	# Seeds should contain at least some unique values
	assert len(set(seed_1)) > 1

	# Seeds should be unique
	assert seed_1 != seed_2

# Test that substitutions are detected
def test_substitution_detect():
	d = DammSum(k, m, get_words())
	seed = d.generate()

	# Check all substitutions
	for j in range(m+1):
		seed_ = seed.copy()
		for i in range(1 << k):
			if seed[j] == d.words[i]:
				continue
			seed_[j] = d.words[i]

			# Substitutions should always fail
			assert not d.verify(seed_)

# Test that transpositions are detected
def test_transpositions():
	d = DammSum(k, m, get_words())
	seed = d.generate()

	# Check all transpositions
	for j in range(m):
		if seed[j] == seed[j+1]:
			continue

		seed_ = seed.copy()
		seed_[j], seed_[j+1] = seed_[j+1], seed_[j]

		# Transpositions should always fail
		assert not d.verify(seed_)

# Test some corrections
def test_corrections():
	d = DammSum(k, m, get_words())
	seed = d.generate()

	# Test the correct seed
	with pytest.raises(ValueError):
		d.correct(seed)

	# Perform a random substitution
	evil_seed = seed.copy()
	while True: # require a nontrivial substitution
		evil_seed[randrange(0, m)] = d.words[randrange(0, 1 << k)]
		if evil_seed != seed:
			break
	seeds = d.correct(evil_seed)
	assert seed in seeds # we should get the original seed...
	assert len(seeds) == m + 1 # ... and other valid seeds

	# Perform a random transposition
	evil_seed = seed.copy()
	while True: # require a nontrivial transposition
		j = randrange(m)
		evil_seed[j], evil_seed[j+1] = seed[j+1], seed[j]
		if evil_seed != seed:
			break
	seeds = d.correct(evil_seed)
	assert seed in seeds # we should get the original seed...
	assert len(seeds) > 0 # ... and may get other valid seeds
