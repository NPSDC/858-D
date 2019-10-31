import BitVector as BV
from Rank import Rank
import math
import gc

def create_substr(bv, i, n, vals):
	if(i == n):
		vals.append(bv.deep_copy())
		return
	bv[i] = 0
	create_substr(bv, i+1, n, vals)
	bv[i] = 1
	create_substr(bv, i+1, n, vals)

def create_pos_vec(alpha_len, n):
	return [BV.BitVector(size = math.ceil(math.log2(n)))]*alpha_len

def get_prefix(bv, l):
	#print(bv)
	return bv[0:l].int_val()

def get_count(bv, n):
	count = 0
	for i in range(len(bv)):
		if(bv[i] == n):
			count += 1
	return count

def print_wavelet(bv_list, pos, map_vec):
	final_out = list()
	for i in bv_list:
		final_out.append(str(i))
	#print(final_out)
	out = list()
	min_pos = 0
	str_ele = list(map_vec.keys())
	bv = i
	for i in range(math.ceil(len(map_vec)/2)):
		#print(str_ele[i])
		max_pos = pos[i].int_val()
		out.extend([str_ele[i*2]]*get_count(bv[min_pos:max_pos], 0))
		out.extend([str_ele[i*2 + 1]]*get_count(bv[min_pos:max_pos], 1))
		min_pos = max_pos
	out = ''.join(out)
	final_out.append(out)
	print('\n'.join(final_out))

def main():
	#T = "0167154263"
	T = "alabar_a_la_alabarda"
	#T = "abcdefghhhijkl"
	alphabet = sorted(list(set(T)))
	len_alpha = len(alphabet)
	#print(len_alpha)
	bits_alpha = math.ceil(math.log2(len_alpha))
	int_alp_dict = dict()

	for i in range(len(alphabet)):
		int_alp_dict[alphabet[i]] = i

	T_sub = []
	create_substr(BV.BitVector(size=bits_alpha), 0, bits_alpha, T_sub)
	
	bv_list = [BV.BitVector(size = len(T))]*bits_alpha
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
	#print(str(bv_list[2]))
	for l in reversed(range(1, bits_alpha)):
		S_pos = create_pos_vec(len_alpha, len(T))
		for i in range(int(math.pow(2,l))):
			if (2*i+1) < len(hist):
				hist[i] = hist[2*i] + hist[2*i + 1]
		for i in range(1, int(math.pow(2,l))):
			S_pos[i] = S_pos[i-1].deep_copy()
			Rank.add_num(S_pos[i], hist[i-1])
		#print(list(map(str, S_pos)))
		for i in range(len(T)):
			#print(T_sub[int_alp_dict[T[i]]])
			#print(get_prefix(T_sub[int_alp_dict[T[i]]], l))
			
			pos = S_pos[get_prefix(T_sub[int_alp_dict[T[i]]], l)].int_val()

			Rank.add_num(S_pos[get_prefix(T_sub[int_alp_dict[T[i]]], l)], 1)
			#print(bv_list[l][pos])
			#print(int_alp_dict[T[i]],pos)
		#	print(bv_list[l][pos])
			bv_list[l][pos] = T_sub[int_alp_dict[T[i]]][l]

			#print('ho')


		# for i in range(len(T)):
		# 	pos = 
		#print(l, "l")
		#print(list(map(str, S_pos)))
		S_pos_list.insert(0, S_pos)
		print(str(bv_list[0]))
		#print(l)
		
		
		#gc.collect()
	#print(str(bv_list[2]))
	#print(len(bv_list))
	#print(bits_alpha-2)
	#print(len(int_alp_dict.keys()))
	#print_wavelet(bv_list, S_pos_list[bits_alpha-1], int_alp_dict)

if __name__ == '__main__':
	main()