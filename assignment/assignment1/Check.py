from Select import Select
from Rank import Rank
import _pickle as Pi
import sys
import BitVector as BV
import math
import numpy as np
import time
import os

class Check(object):

	def __init__(self, min_bits, max_bits, save_file):
		self.min = min_bits
		self.max = max_bits
		self.save = save_file
		#self.n_queries = n_queries
		if(os.path.exists(save_file)):
			with open(save_file, "rb") as f:
				self.r_ob_list = Pi.load(f)
		else:
			self.r_ob_list = self.create_rb()

	def get_min_bits(self):
		return self.min

	def get_max_bits(self):
		return self.max

	def get_save_file(self):
		return self.save

	def get_r_ob_list(self):
		return self.r_ob_list

	# def get_queries(self):
	# 	return self.n_queries

	def create_rb(self):
		min_bits = self.get_min_bits()
		max_bits = self.get_max_bits()
		save_file = self.get_save_file()
		rank_arr = list()
		bv = BV.BitVector(bitstring = "11111100011100111")
		count = 0
		prev = int(math.pow(2, min_bits-1))
		for bits in range(min_bits, (max_bits+1)):
			curr = int(math.pow(2,bits))
			bv = bv.gen_random_bits(curr)
			rank_arr.append(Rank(bv))
			bv = bv.gen_random_bits(curr + prev)
			rank_arr.append(Rank(bv))
			prev = curr
			count += 2
			if(bits < 20):
				if(count % 10 == 0):
					with open(save_file, "wb") as f_write:
						Pi.dump(rank_arr, f_write)
				if(bits == (max_bits)):
					with open(save_file, "wb") as f_write:
						Pi.dump(rank_arr, f_write)
			else:
				with open(save_file, "wb") as f_write:
					Pi.dump(rank_arr, f_write)
		return rank_arr

	def perform_queries_rank(self):
		r_ob_list = self.get_r_ob_list()
		t_end_list = list()
		for r_ob in r_ob_list:
			bv_len = r_ob.get_bit_vector().length()
			quer_inds = np.random.randint(0, bv_len, n_queries)		
			t_start = time.time()
			ranks = [r_ob.rank1(i) for i in quer_inds]
			t_end = time.time()	- t_start
			t_end_list.append(t_end)
		return(t_end_list)

	def create_plots(self, queries):
		t_r_list = self.perform_queries_rank(queries)
		
			


def main():
	ob = Check(3, 24, "rank.pickle")
	ob.create_rb()

if __name__ == '__main__':
	main()
