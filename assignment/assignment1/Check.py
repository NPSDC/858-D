from Select import Select
from Rank import Rank
import _pickle as Pi
import sys
import BitVector as BV
import math

class Check(object):

	def __init__(self, min_bits, max_bits, save_file):
		self.min = min_bits
		self.max = max_bits
		self.save = save_file

	def get_min_bits(self):
		return self.min

	def get_max_bits(self):
		return self.max

	def get_save_file(self):
		return self.save

	def create_rb(self):
		min_bits = self.get_min_bits()
		max_bits = self.get_max_bits()
		save_file = self.get_save_file()
		rank_arr = list()
		bv = BV.BitVector(bitstring = "11111100011100111")
		count = 0
		prev = math.pow(2, min_bits-1)
		for bits in range(min_bits, (max_bits+1)):
			curr = int(math.pow(2,bits))
			bv = bv.gen_random_bits(int(curr))
			rank_arr.append(Rank(bv))
			bv = bv.gen_random_bits(int(curr + prev))
			rank_arr.append(Rank(bv))
			print(bits)
			#print(rank_arr[-1].get_bit_vector().length())
#			print(len(rank_arr))
			prev = curr
			count += 2
			if(bits < 20):
				if(count % 10 == 0):
					with open(save_file, "wb") as f_write:
						Pi.dump(rank_arr, f_write)
				if(bits == (max_bits)):
#					print(max_bits)
					with open(save_file, "wb") as f_write:
						Pi.dump(rank_arr, f_write)
			else:
				with open(save_file, "wb") as f_write:
					Pi.dump(rank_arr, f_write)
			
		return rank_arr

def main():
	ob = Check(3, 24, "rank.pickle")
	ob.create_rb()

if __name__ == '__main__':
	main()
