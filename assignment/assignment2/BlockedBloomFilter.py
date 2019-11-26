import mmh3
from bitarray import bitarray
import math
import os
import numpy as np
import argparse as ag
import _pickle as Pi
import sys

from BloomFilter import BloomFilter

class BlockedBloomFilter( BloomFilter ):

	def __init__(self, fpr, n_dist_keys, cache_size = 512):
		BloomFilter.__init__(self, fpr, n_dist_keys)
		self.n_blocks = math.ceil(self.get_m()/cache_size)
		self.cache_size = cache_size 
		self.create_blocks()

	def get_n_blocks(self):
		return self.n_blocks

	def get_cache_size(self):
		return self.cache_size

	def create_blocks(self):
		m = self.get_m()
		#ba = self.get_ba()
		n_blocks = self.get_n_blocks()
		cache_size = self.get_cache_size()
		self.ba = []
		mod = self.get_m() % cache_size
		for i in range(n_blocks):
			if(i == (n_blocks - 1) and mod != 0):
				self.ba.append(bitarray(mod))
			else:
				self.ba.append(bitarray(cache_size))
			self.ba[i].setall(0)

	def add(self, key):
		k = self.get_hash_counts()
		ba = self.get_ba()
		n_blocks = self.get_n_blocks()
		block = mmh3.hash(key, 0) % n_blocks
		cache_size = self.get_cache_size()

		for i in range(k-1):
			val = mmh3.hash(key, i + 1) % len(ba[block])
			ba[block][val] = True

	def query(self, key):
		k = self.get_hash_counts()
		ba = self.get_ba()
		n_blocks = self.get_n_blocks()
		block = mmh3.hash(key, 0) % n_blocks

		for i in range(k-1):
			val = mmh3.hash(key, i + 1) % len(ba[block])
			if not ba[block][val]:
				return False
		return True

def main():
	bbf = BlockedBloomFilter(0.01, 10)
	bbf.add('1')
	print(bbf.query('1'))
	print(bbf.query('2'))
	print(bbf.query('3'))
	print(bbf.query('100'))
	bbf.add('2')
	bbf.add('3')
	bbf.add('100')
	print(bbf.query('1'))
	print(bbf.query('2'))
	print(bbf.query('3'))
	print(bbf.query('100'))

if __name__ == '__main__':
	main()
