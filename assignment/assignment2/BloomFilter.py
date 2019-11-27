import mmh3
from bitarray import bitarray
import math
import os
import numpy as np
import argparse as ag
import _pickle as Pi
import sys

class BloomFilter(object):
	def __init__(self, fpr, n_dist_keys):
		self.fpr = fpr
		self.n = n_dist_keys
		self.m = self.compute_m()
		self.k = self.compute_hash_counts()
		self.ba = bitarray(self.get_m())
		self.ba.setall(0)

	def get_n(self):
		return self.n

	def get_fpr(self):
		return self.fpr

	def get_ba(self):
		return self.ba

	def compute_m(self):
		fpr = self.get_fpr()
		n = self.get_n()
		m = -(n*math.log(fpr))/(math.log(2)**2)
		int_m = int(m)
		if(int_m == 0):
			int_m = 1
		return int_m

	def get_m(self):
		return self.m

	def compute_hash_counts(self):
		fpr = self.get_fpr()
		n = self.get_n()
		m = self.get_m()
		k = m/n*math.log(2)
		int_k = int(k)
		if(int_k == 0):
			int_k = 1
		return int_k

	def get_hash_counts(self):
		return self.k

	def add(self, key):
		k = self.get_hash_counts()
		ba = self.get_ba()
		m  = self.get_m()
		for i in range(k):
			val = mmh3.hash(key.strip(), i) % m
			ba[val] = True


	def insert(self, file):
		if(os.path.exists(file)):
			with open(file, 'r') as f:
				for key in f.readlines():
					self.add(key.strip())
		else:
			sys.exit(file + "File does not exist")

	def query(self, key):
		k = self.get_hash_counts()
		ba = self.get_ba()
		m = self.get_m()
		for i in range(k):
			val = mmh3.hash(key.strip(), i) % m
			if(not ba[val]):
				return False
		return True
	
	def query_file(self, file):
		if(os.path.exists(file)):
			with open(file, 'r') as f:
				for q in f.readlines():
					val = self.query(q.strip())
					if(val):
						print("{}:Y".format(q.strip()))
					else:
						print("{}:N".format(q.strip()))


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