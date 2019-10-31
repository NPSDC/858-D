import sys
import BitVector as BV
import math

class Wavelet(object):
	def __init__(self, seq):
		self.seq = seq
		self.alphabet, self.int_alp_dict = self.hash_seq()
		self.T_bit

	def hash_seq(self):
		alphabet = sorted(list(set(T)))
		int_alpha_dict = dict()
		for i in range(len(alphabet)):
			int_alp_dict[alphabet[i]] = i
		return(alphabet, int_alp_dict)

	def create_substr(bv, i, n, vals):
		if(i == n):
			vals.append(bv.deep_copy())
			return
		bv[i] = 0
		create_substr(bv, i+1, n, vals)
		bv[i] = 1
		create_substr(bv, i+1, n, vals)