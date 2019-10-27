from Select import Select
from Rank import Rank
import _pickle as Pi
import sys
import BitVector as BV
import math
import numpy as np
import time
import os
import matplotlib.pyplot as plt

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
		self.sel_ob_list = self.create_sel_list()

	def get_min_bits(self):
		return self.min

	def get_max_bits(self):
		return self.max

	def get_save_file(self):
		return self.save

	def get_r_ob_list(self):
		return self.r_ob_list

	def get_sel_ob_list(self):
		return self.sel_ob_list
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

	def create_sel_list(self):
		r_ob_list = self.get_r_ob_list()
		sel_arr = [0]*len(r_ob_list)
		for i in xrange(r_ob_list):
			sel_arr[i] = Select(r_ob_list[i])
		return sel_arr

	def perform_queries_rank(self, queries, round_by = 5):
		r_ob_list = self.get_r_ob_list()
		t_end_list = list()
		for r_ob in r_ob_list:
			bv_len = r_ob.get_bit_vector().length()
			quer_inds = np.random.randint(0, bv_len, queries)		
			t_start = time.time()
			ranks = [r_ob.rank1(i) for i in quer_inds]
			t_end = time.time()	- t_start
			t_end_list.append(t_end)
		t_end_list = np.round(t_end_list, round_by)
		print(t_end_list)
		return(t_end_list)

	def perform_queries_select(self, queries, round_by = 5):
		sel_ob_list = self.get_sel_ob_list()
		t_end_list = list()
		for sel_ob in sel_ob_list:
			max_rank = sel_ob.get_max_rank()
			quer_inds = np.random.randint(0, max_rank, queries)
			t_start = time.time()
			sel_inds = [sel_ob.select1(i) for i in quer_inds]
			t_end = time.time()	- t_start
			t_end_list.append(t_end)
		t_end_list = np.round(t_end_list, round_by)
		print(t_end_list)
		return(t_end_list)

	def overhead_queries(self, queries):
		r_ob_list = self.get_r_ob_list()
		overhead = [r_ob.overhead() for r_ob in r_ob_list]
		return overhead

	def create_plots(self, queries):
		t_r_list = self.perform_queries_rank(queries)
		r_ob_list = self.get_r_ob_list()
		sel_ob_list = sle

		lengths = [r_ob.get_bit_vector().length() for r_ob in r_ob_list]
		plt.scatter(lengths, t_r_list, c = 'r')
		plt.plot(lengths, t_r_list)#, lengths, t_r_list, "-bl")
		plt.xlabel("Length of bit string")
		plt.ylabel("Time in seconds")
		plt.show()

		overhead = self.overhead_queries(queries)
		plt.scatter(lengths, overhead, c = 'r')
		plt.plot(lengths, overhead)#, lengths, overhead, "bl")
		plt.xlabel("Length of bit string")
		plt.ylabel("Overhead in bits")
		plt.show()

def main():
	ob = Check(3, 24, "rank.pickle")

if __name__ == '__main__':
	main()
