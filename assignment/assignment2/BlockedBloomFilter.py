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
	parser = ag.ArgumentParser()
	parser_build = ag.ArgumentParser(add_help = False)
	parser_query = ag.ArgumentParser(add_help = False)
	#subparsers = parser.add_subparsers()

	#parser_build.add_argument('command', type = str, default = 'build')
	parser_build.add_argument('-k', type = str, help = "Key File", required = True, dest = 'k')
	parser_build.add_argument('-f', type = float, help = "FPR", required = True, dest = 'f')
	parser_build.add_argument('-n', type = int, help = "Number of distinct keys", required = True)
	parser_build.add_argument('-o', type = str, help = "Output file to store input", required = True)

	parser_query.add_argument('-i', type = str, help = "Input file containing bloomFilter array", required = True)
	parser_query.add_argument('-q', type = str, help = "Input file containing queries", required = True)

	subparsers = parser.add_subparsers()
	subparser_build = subparsers.add_parser("build", parents = [parser_build])
	subparser_build.set_defaults(which="build")
	subparser_query = subparsers.add_parser("query", parents = [parser_query])
	subparser_query.set_defaults(which="query")


	args = parser.parse_args()
	#print(parser_build)
	
	
	if(args.which == 'build'):
		#args = parser.parse_args()
		BF = BloomFilter(args.f, args.n)
		BF.insert(args.k)
		with open(args.o, "wb") as f:
			Pi.dump(BF, f)

	elif(args.which == 'query'):
		if(os.path.exists(args.i)):
			with open(args.i, "rb") as f:
				BF = Pi.load(f)
				BF.query_file(args.q)
		else:
			sys.exit("Input file does not exists")

if __name__ == '__main__':
	main()
