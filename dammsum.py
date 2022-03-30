# DammSum: efficient mnemonic seeds from quasigroup checksums
#
# This code is for prototyping only, and has not been written as a secure implementation.
# Do not use in production!

import secrets
from typing import List

class DammSum:
    def __init__(self, k:int, m:int, words:List[str]) -> None:
        # Define the monic irreducible polynomials for masking
        # See https://www.hpl.hp.com/techreports/98/HPL-98-135.pdf for the table of values
        # These have an implied constant term that we account for later
        polys = {}
        polys[2] = (2,1)
        polys[3] = (3,1)
        polys[4] = (4,1)
        polys[5] = (5,2)
        polys[6] = (6,1)
        polys[7] = (7,1)
        polys[8] = (8,4,3,1)
        polys[9] = (9,1)
        polys[10] = (10,3)
        polys[11] = (11,2)
        polys[12] = (12,3)
        polys[13] = (13,4,3,1)
        polys[14] = (14,5)
        polys[15] = (15,1)
        polys[16] = (16,5,3,1)
        polys[17] = (17,3)
        polys[18] = (18,3)
        polys[19] = (19,5,2,1)
        polys[20] = (20,3)
        polys[21] = (21,2)
        polys[22] = (22,1)
        polys[23] = (23,5)
        polys[24] = (24,4,3,1)
        polys[25] = (25,3)
        polys[26] = (26,4,3,1)
        polys[27] = (27,5,2,1)
        polys[28] = (28,1)
        polys[29] = (29,2)
        polys[30] = (30,1)
        polys[31] = (31,3)
        polys[32] = (32,7,3,2)
        
        # Input checks
        if k not in polys: # for other values (up to 10000), see the original table
            raise ValueError('Invalid word list size!')
        if m < 1:
            raise ValueError('Invalid seed size!')
        if len(words) != 1 << k or len(words) != len(set(words)): # all words must be distinct
            raise ValueError('Word list must be distinct!')
        
        self.k = k
        self.m = m
        self.words = words
        self.digits = {word:words.index(word) for word in words}

        # Compute the bitmask, accounting for the implied constant term
        self.mask = 1
        for bit in polys[k]:
            self.mask += (1 << bit)
    
    # Compute a checksum (or include the checksum if verifying)
    def checksum(self, seed:List[str], has_checksum:bool) -> str:
        # Input checks
        if not has_checksum and len(seed) != self.m:
            raise ValueError('Invalid seed size!')
        if has_checksum and len(seed) != self.m + 1:
            raise ValueError('Invalid seed size!')
        for word in seed:
            if word not in self.words:
                raise ValueError('Invalid seed!')
        
        # Perform the Damm algorithm
        result = 0
        for word in seed:
            digit = self.digits[word]
            result ^= digit # add
            result <<= 1 # multiply by 2
            if result & (1 << self.k): # reduce using the irreducible monic polynomial
                result ^= self.mask
        return self.words[result]
    
    # Verify a seed with checksum
    def verify(self, seed:List[str]) -> bool:
        # Input checks
        if len(seed) != self.m + 1:
            raise ValueError('Invalid seed size!')
        for word in seed:
            if word not in self.words:
                raise ValueError('Invalid seed!')
        
        # We can verify against a zero value
        if self.checksum(seed, True) != self.words[0]:
            return False
        return True
    
    # Generate a random seed with checksum
    def generate(self) -> List[str]:
        result = [self.words[secrets.randbelow(1 << self.k)] for _ in range(self.m)]
        result.append(self.checksum(result, False))
        return result
    
    # Attempt to correct single substitution and transposition errors; this is neither guaranteed nor unique on arbitrary input!
    def correct(self, seed:List[str]) -> List[str]:
        # The seed is already valid
        if self.verify(seed):
            raise ValueError('The seed is already valid!')

        seeds = [] # valid seed candidates

        # Test transpositions
        for j in range(self.m):
            if seed[j] == seed[j+1]:
                continue

            seed_ = seed.copy()
            seed_[j], seed_[j+1] = seed_[j+1], seed_[j]
            if self.verify(seed_):
                if seed_ not in seeds:
                    seeds.append(seed_.copy())
        
        # Test substitutions
        for j in range(self.m+1):
            seed_ = seed.copy()
            for i in range(1 << self.k):
                if seed[j] == self.words[i]:
                    continue
                seed_[j] = self.words[i]
                if self.verify(seed_):
                    if seed_ not in seeds:
                        seeds.append(seed_.copy())

        return seeds
