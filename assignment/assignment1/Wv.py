import BitVector as BV
from Rank import Rank
import math
import gc
import string
import numpy as np

def create_substr(bv, i, n, vals):
	if(i == n):
		vals.append(bv.deep_copy())
		return
	bv[i] = 0
	create_substr(bv, i+1, n, vals)
	bv[i] = 1
	create_substr(bv, i+1, n, vals)

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

def create_pos_vec(alpha_len, n):
	pos_vec = list()
	for i in range(alpha_len):
		pos_vec.append(BV.BitVector(size = math.ceil(math.log2(n))+1))
	return pos_vec

def get_prefix(bv, l):
	#print(bv)
	return bv[0:l].int_val()

def gen_bv(str_len, levels):
	bv_list = list()
	for i in range(levels):
		bv_list.append(BV.BitVector(size = str_len))
	return bv_list

def get_count(bv, n):
	count = 0
	for i in range(len(bv)):
		if(bv[i] == n):
			count += 1
	return count

def print_wavelet(bv_list, pos, map_vec):
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
			out.extend([str_ele[i*2]]*get_count(bv[min_pos:max_pos], 0))
			out.extend([str_ele[i*2 + 1]]*get_count(bv[min_pos:max_pos], 1))
			min_pos = max_pos
	max_pos = len(bv)
	#print(min_pos, max_pos,i)
	if(min_pos < len(bv)-1	):
		out.extend([str_ele[i]]*(max_pos - min_pos))
	out = ''.join(out)
	final_out.append(out)
	return('\n'.join(final_out))

def create_alternate(length):
	return [0]*length

def main():
	T = "0167154263"
	T = gen_rand_string(10,1000)
	T = "xbqcgmmbmxxnqwcxwcmxmxwbmnmhqh"
	#print(len(T))
	#print(T)
	#print(set(T))

	#T = "alabar_a_la_alabarda"
	#T = "abcdefghhhijkl"
	alphabet = sorted(list(set(T)))
	len_alpha = len(alphabet)
	#print(len_alpha)
	levels = math.ceil(math.log2(len_alpha))
	int_alp_dict = dict()

	for i in range(len(alphabet)):
		int_alp_dict[alphabet[i]] = i

	T_sub = []
	create_substr(BV.BitVector(size=levels), 0, levels, T_sub)
	
	bv_list = gen_bv(len(T), levels)
	#print(len(bv_list))
	#print(int_alp_dict)

	#bv_list.append(BV.BitVector(size = len(T)))

	#S_pos = create_pos_vec(len_alpha, len(T))
	#print(list(map(str, S_pos)))
	hist = dict()
	l = len(T)
	for i in range(len(T)):
		key = int_alp_dict[T[i]]
		#	print(key)
		if(key in hist.keys()):
			hist[key] += 1
		else:
			hist[key] = 1
		bv_list[0][i] = T_sub[key][0]

	#print(len(hist))
	#print(T_sub)
	#print(list(map(str, S_pos)))
	#print(str(bv_list[0]))
	S_pos_list = list()
	d = []
	#print(sum(hist.values()))
	#print(str(bv_list[2]))
	#print(bv_list)
	#print(len(hist))
	l_hist = len(hist)
	for l in reversed(range(1, levels)):
		S_pos = create_pos_vec(len_alpha, len(T))
		#S_pos2 = create_alternate(len_alpha)
		#print(S_pos2)
		#print(l, "l")

		for i in range(int(math.pow(2,l))):
			#print(i)
			if((2*i + 1) >= l_hist):
				break
			if (2*i+1) < l_hist:
				hist[i] = hist[2*i] + hist[2*i + 1]
		if (l_hist-1) == (2*i):
			hist[i] = hist[2*i]
				# 	print(hist[i])
		# print("shakla")
		#print(len_alpha)
		#print(hist)
		for i in range(1, min(int(math.pow(2,l)), len_alpha)):
		#	print(i)
			S_pos[i] = S_pos[i-1].deep_copy()				
			Rank.add_num(S_pos[i], hist[i-1])

			#print(hist[i-1])
			#print(S_pos[i].int_val())
#			print(S_pos[i].int_val())

			#print(i)
			#print(i, S_pos[i].int_val())
			#S_pos2[i] = S_pos2[i-1] + hist[i-1]
		#print(list(map(str, S_pos)))
#		print('dd')
		for i in range(len(T)):
			#print(T_sub[int_alp_dict[T[i]]])
			#print(get_prefix(T_sub[int_alp_dict[T[i]]], l))
			interval = get_prefix(T_sub[int_alp_dict[T[i]]], l)
			pos = S_pos[interval].int_val()
			Rank.add_num(S_pos[interval], 1)
			#S_pos2[interval] += 1
			#print(bv_list[l][pos])
			#print(int_alp_dict[T[i]],pos)
		#	print(bv_list[l][pos])
			bv_list[l][pos] = T_sub[int_alp_dict[T[i]]][l]

			#print('ho')


		# for i in range(len(T)):
		# 	pos = 
		#print(l, "l")
		#print(list(map(str, S_pos)))
		#print(S_pos2)
		S_pos_list.insert(0, S_pos)
		l_hist = math.ceil(l_hist/2)
		#print(str(bv_list[0]))
		#print(l)
		
		
		#gc.collect()
	#print(str(bv_list[0]))
	#print(str(bv_list[1]))
	#print(str(bv_list[2]))
	#print(len(bv_list))
	#print(bits_alpha-2)
	#print(len(int_alp_dict.keys()))
	
	print(print_wavelet(bv_list, S_pos_list[levels-2], int_alp_dict))

if __name__ == '__main__':
	main()