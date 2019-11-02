import sys
import BitVector as BV
import math
import string
import numpy as np
from Rank import Rank

class Wavelet(object):
	def __init__(self, seq):
		self.seq = seq
		self.alphabet, self.alpha_map = self.hash_seq()
		self.levels = math.ceil(math.log2(len(self.get_alphabet())))
		self.alpha_bit_rep = []
		self.create_substr(BV.BitVector(size = self.get_levels()), 0, self.get_levels(), self.get_alpha_bit_rep())
		self.bv_list = self.gen_bv()
		self.hist = self.gen_hist()
		self.pos_vec_list = self.create_pos_vec_list()
		self.gen_wavelet()
		self.wavelet = self.print_wavelet()
		self.rank = self.gen_rank()
		self.select = self.gen_select()

		#self.T_bit

	def get_seq(self):
		return self.seq

	def get_alphabet(self):
		return self.alphabet

	def get_alpha_map(self):
		return self.alpha_map

	def get_levels(self):
		return self.levels

	def get_alpha_bit_rep(self):
		return self.alpha_bit_rep

	def get_bv_list(self):
		return self.bv_list

	def get_pos_vec_list(self):
		return self.pos_vec_list

	def get_hist(self):
		return self.hist

	def get_wavelet(self):
		return self.wavelet

	def get_rank(self):
		return self.rank

	def get_select(self):
		return self.select

	def get_select(self):
		return self.select

	def hash_seq(self):
		alphabet = sorted(list(set(self.get_seq())))
		int_alpha_dict = dict()
		for i in range(len(alphabet)):
			int_alpha_dict[alphabet[i]] = i
		return(alphabet, int_alpha_dict)

	def create_substr(self, bv, i, n, vals):
		if(i == n):
			vals.append(bv.deep_copy())
			return
		bv[i] = 0
		self.create_substr(bv, i+1, n, vals)
		bv[i] = 1
		self.create_substr(bv, i+1, n, vals)

	def create_pos_vec_list(self):
		pos_vec_list = list()
		for l in range(self.get_levels()):
			pos_vec = list()
			for i in range(len(self.get_alphabet())):
				pos_vec.append(BV.BitVector(size = math.ceil(math.log2(len(self.get_seq())))+1))
			pos_vec_list.append(pos_vec)
		return pos_vec_list

	def gen_bv(self):
		T = self.get_seq()
		str_len = len(T)
		levels = self.get_levels()
		int_alpha_map = self.get_alpha_map()

		bv_list = list()
		for i in range(levels):
			bv_list.append(BV.BitVector(size = str_len))
		for i in range(str_len):
			key = int_alpha_map[T[i]]
			bv_list[0][i] = self.get_alpha_bit_rep()[key][0]

		return bv_list

	def gen_wavelet(self):

		S_pos_list = self.get_pos_vec_list()
		hist = self.get_hist()
		l_hist = len(hist)
		levels = self.get_levels()
		T = self.get_seq()
		len_alpha = len(self.get_alphabet())
		bv_list = self.get_bv_list()
		int_alpha_map = self.get_alpha_map()
		T_sub = self.get_alpha_bit_rep()
		
		for l in reversed(range(1, levels)):

			for i in range(int(math.pow(2,l))):
				#print(i)
				if((2*i + 1) >= l_hist):
					break
				if (2*i+1) < l_hist:
					hist[i] = hist[2*i] + hist[2*i + 1]

			if (l_hist-1) == (2*i):
				hist[i] = hist[2*i]

			for i in range(1, min(int(math.pow(2,l)), len_alpha)):
				S_pos_list[l][i] = S_pos_list[l][i-1].deep_copy()				
				Rank.add_num(S_pos_list[l][i], hist[i-1])

			for i in range(len(T)):
				interval = Wavelet.get_prefix(T_sub[int_alpha_map[T[i]]], l)
				pos = S_pos_list[l][interval].int_val()
				Rank.add_num(S_pos_list[l][interval], 1)
				bv_list[l][pos] = T_sub[int_alpha_map[T[i]]][l]

			l_hist = math.ceil(l_hist/2)

	def print_wavelet(self):
		bv_list = self.get_bv_list()
		pos_list = self.get_pos_vec_list()
		pos = pos_list[-1]
		map_vec = self.get_alpha_map()
		final_out = list()
		for bv in bv_list:
			final_out.append(str(bv))
		out = list()
		min_pos = 0
		str_ele = list(map_vec.keys())

		#print(final_out)
		#print(str_ele)
		for i in range(len(map_vec)):
			if(i*2+1) < len(str_ele):
				#print(i)
				max_pos = pos[i].int_val()
				out.extend([str_ele[i*2]]*Wavelet.get_count(bv[min_pos:max_pos], 0))
				out.extend([str_ele[i*2 + 1]]*Wavelet.get_count(bv[min_pos:max_pos], 1))
				min_pos = max_pos
		max_pos = len(bv)
		#print(min_pos, max_pos,i)
		if(min_pos < len(bv)-1	):
			out.extend([str_ele[i]]*(max_pos - min_pos))
		out = ''.join(out)
		final_out.append(out)
		return('\n'.join(final_out))
	
	def gen_hist(self):
		hist = dict()
		T = self.get_seq()
		int_alpha_map = self.get_alpha_map()
		l = len(T)
		for i in range(len(T)):
			key = int_alpha_map[T[i]]
			#	print(key)
			if(key in hist.keys()):
				hist[key] += 1
			else:
				hist[key] = 1
		return(hist)

	def gen_rank(self):
		bv_list = self.get_bv_list()
		rank_list = list()
		for i in range(len(bv_list)):
			rank_list.append(Rank(bv_list[i]))
		return rank_list

	def gen_select(self):
		bv_list = self.get_bv_list()
		select_list = list()
		for i in range(len(bv_list)):
			select_list.append(Rank(bv_list[i]))
		return select_list

	def access(self, ind):
		bv_list = self.get_bv_list()
		rank_list = self.get_rank()
		pos_list = self.get_pos_vec_list()
		pos = 0
		r = 0
		sub_ind = 0
		for l in range(self.get_levels()):
			if(pos != 0):
				sub_ind = pos_list[l][pos-1].int_val() 
				print(sub_ind, "sub")
				ind = sub_ind + r - 1
			val = bv_list[l][ind]

			if(val == 1):
				r = rank_list[l].rank1(ind) - rank_list[l].rank1(sub_ind)
				print(r, 'rank')
				pos = pos*2 + 1
			else:
				r = rank_list[l].rank0(ind) - rank_list[l].rank1(sub_ind)
				pos = pos*2
			print(ind, "ind")
		print(ind)


	@staticmethod
	def get_prefix(bv, l):
		return bv[0:l].int_val()	

	@staticmethod
	def get_count(bv, n):
		count = 0
		for i in range(len(bv)):
			if(bv[i] == n):
				count += 1
		return count

	#def
def gen_rand_string(num_char, str_len):
	letters = string.ascii_lowercase
	rand_numbers = np.random.choice(len(letters), num_char, replace = False)
	letters = [letters[i] for i in rand_numbers]
	s_inds = list(np.random.choice(num_char, num_char, replace = False))
#	print(np.random.randint(0, num_char, str_len-num_char))
	s_inds.extend(list(np.random.randint(0, num_char, str_len-num_char)))
#	print(s_inds)
	final_str = ''.join([letters[i] for i in s_inds])
	return final_str

def main():
	T = gen_rand_string(7,10)
	T = "xbqcgmmbmxxnqwcxwcmxmxwbmnmhqh"
	T = "0167154263"
	print(T)
	ob = Wavelet(T)
	print(ob.get_wavelet())
	for bv in ob.get_pos_vec_list():
		print(list(map(str,bv)))
	ob.access(2)
	#ob.gen_wavelet()
	#print(list(map(str, ob.get_pos_vec_list())))
	#print(ob.get_hist())

if __name__ == "__main__":
	ob = main()