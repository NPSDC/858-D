import sys
import os
import string
import numpy as np
import _pickle as Pi
from BloomFilter import BloomFilter as BF
from BlockedBloomFilter import BlockedBloomFilter as BBF
import time
import matplotlib.pyplot as plt
import seaborn as sb
import pandas as pd

class CreateTests(object):
	@staticmethod
	def create_rand_keys(num_keys, max_key_size = 100, check_keys = [], file_write = None, ret = False, all = None):
		orig_keys = check_keys[:]
		#print(len(check_keys), "ssjs")
		letters = string.printable
		for num in range(num_keys):
			while(1):
				key_size = np.random.randint(5, max_key_size + 1)
				rand_numbers = np.random.choice(len(letters), key_size, replace = False)
				key = repr(''.join([letters[i] for i in rand_numbers]))
				if not key in orig_keys:
					orig_keys.append(key)
					break
		#print(len(check_keys))
		if(file_write is not None):
			if(all is None):
				with open(file_write, 'w') as f:
					for num in range(len(orig_keys)):
						if(num < (len(orig_keys) - 1)):
							f.write(orig_keys[num] + "\n")
						else:
							f.write(orig_keys[num])
			else:
				with open(file_write, 'w') as f:
					for num in range(num_keys, len(orig_keys)):
						if(num < (len(orig_keys) - 1)):
							f.write(orig_keys[num] + "\n")
						else:
							f.write(orig_keys[num])

		if(ret):
			return orig_keys

	@staticmethod
	def create_test_query(key_file, type, keys):
		if(os.path.exists(key_file)):
			if not type in [1,2]:
				sys.exit("Invalid type")
			#keys = []
			# with open(key_file, 'r') as f:
			# 	for key in f.readlines():
			# 		keys.append(key.strip('\n'))

			if(type == 1):
				CreateTests.create_rand_keys(num_keys = len(keys), check_keys = keys, file_write = key_file.split('.')[0] + "_nocomm.txt", all = 1)
			else:
				#print(len(keys), 'aaa')
				#print(len([keys[i] for i in list(np.random.choice(len(keys), len(keys)//2, replace = True))]), "asa")
				CreateTests.create_rand_keys(num_keys = len(keys)//2, \
					check_keys = [keys[i] for i in list(np.random.choice(len(keys), len(keys)//2, replace = False))], \
				 	file_write  = key_file.split('.')[0] + "_50comm.txt")

	@staticmethod
	def gen_files(n_keys_list, directory):
		if(os.path.exists(directory)):
			for n_keys in n_keys_list:
				key_file = os.path.join(directory, "{}.txt".format(n_keys))
				keys = CreateTests.create_rand_keys(n_keys, file_write = key_file, check_keys = [], ret = True)
				CreateTests.create_test_query(key_file, 1, keys)
				CreateTests.create_test_query(key_file, 2, keys)
		else:
			sys.exit("Invalid directory Path")

	@staticmethod
	def create_BF(fpr_list, n_keys_list, dir, BF_type):
		bf_list = list()
		for i in range(len(fpr_list)):
			bf_list.append(list())
			for j in range(len(n_keys_list)):
				bf = BF_type(fpr_list[i], n_keys_list[j])
				f_name = os.path.join(dir, "{}.txt".format(n_keys_list[j]))
				bf.insert(f_name)
				bf_list[i].append(bf)

		try:
			module_name = BF_type.__module__
		except Exception:
			sys.exit("Class Name expected")

		if module_name == 'BlockedBloomFilter':
			with open(os.path.join(dir, "bbf_list.pickle"), "wb") as f_write:
				Pi.dump(bf_list, f_write)
		elif module_name == 'BloomFilter':
			with open(os.path.join(dir, "bf_list.pickle"), "wb") as f_write:
				Pi.dump(bf_list, f_write)
		else:
			sys.exit("Invalid class name")
		return(bf_list)

	@staticmethod
	def find_query_time(bf_list, fpr_list, n_keys_list, comm_cont, dir):
		query_times = []
		for i in range(len(fpr_list)):
			query_times.append(list())
			for j in range(len(n_keys_list)):
				file = os.path.join(dir, str(n_keys_list[j]) + comm_cont + ".txt")
				if(not os.path.exists(file)):
					sys.exit("{} file does not exists".format(file))
				cum_time = 0
				with open(file, "rb") as f:
					for q in f.readlines():
						q = q.strip()
						start_time = time.time()
						bf_list[i][j].query(q)
						end_time = time.time()
						req_time = end_time - start_time
						cum_time += req_time
				query_times[i].append(cum_time/n_keys_list[j])
		return query_times

	@staticmethod
	def compute_emp_fpr(bf, q_file, fpr_ded = False):
		if(os.path.exists(q_file)):
			n_pos = 0
			with open(q_file, "r") as f:
				queries = f.readlines()
				for q in queries:
					q = q.strip('\n')
					val = bf.query(q)
					if val:
						n_pos += 1
			if(fpr_ded):
				n_pos -= bf.get_n()/2 
				val = n_pos*2/bf.get_n()
			else:
				val = n_pos/bf.get_n()
			return val

		else:
			sys.exit("{} does not exists".format(q_file))

	@staticmethod
	def compute_fpr_list(bf_list, fpr_list, n_keys_list, dir, fpr_ded):
		emp_fpr_list = list()
		for i in range(len(fpr_list)):
			emp_fpr_list.append(list())
			emp_fpr_list[i] = [0]*len(n_keys_list)
			for j in range(len(n_keys_list)):
				if(fpr_ded):
					file = os.path.join(dir, str(n_keys_list[j]) + "_50comm" + ".txt")
				else:
					file = os.path.join(dir, str(n_keys_list[j]) + "_nocomm" + ".txt")
				if(not os.path.exists(file)):
					sys.exit("{} file does not exists".format(file))
				emp_fpr_list[i][j] = CreateTests.compute_emp_fpr(bf_list[i][j], file, fpr_ded)
		return emp_fpr_list

	@staticmethod
	def plot_query(fpr_pos, nkeys_list, names, *qlist, type, title):

		if not len(names) == len(qlist):
			sys.exit("Lengths not same")
		if not type in ["query", "FPR"]:
			sys.exit("Invalid type")
		ax = plt.subplot(111)
		for i in range(len(qlist)):
			if(type == 'query'):
				ax.plot(nkeys_list, np.array(qlist[i][fpr_pos])*1e6, label = names[i])
			else:
				ax.plot(nkeys_list, np.array(qlist[i][fpr_pos]), label = names[i])
		ax.set_title(title, fontsize = 12, fontweight = 'bold')
		ax.set_xlabel("Key Size", fontsize = 12)
		if(type == 'query'):
			ax.set_ylabel("Time in microseconds", fontsize = 12)
		else:
			ax.set_ylabel("FPR", fontsize = 12)
		ax.legend()
		plt.show()

	@staticmethod
	def create_heatmap(fpr_comp_list, fpr_list, n_keys_list, title):
		df = pd.DataFrame(fpr_comp_list, columns = n_keys_list, index = fpr_list)
		ax = plt.axes()
		sb.heatmap(df, ax = ax)
		ax.set_title(title, fontsize = 12, fontweight = 'bold')
		ax.set_xlabel("Key Size", fontsize = 12)
		ax.set_ylabel("FPR", fontsize = 12)
		plt.show()

def main():
	nkeys_list = list(range(1000, int(1e5), 5000))
	nkeys_list.extend(list(range(int(1e5), int(1e6), 50000)))
	nkeys_list.extend(list(range(int(1e6), int(1e7), 500000)))
	fpr_list = np.array(range(1,26))/100
	#nkeys_list = nkeys_list[10:20]
	CreateTests.gen_files(nkeys_list, 'test2')
	bf_list = CreateTests.create_BF(fpr_list, [1000,2000], 'test')
	#q_time = CreateTests.find_query_time(bf_list, fpr_list, [1000,2000], '_nocomm', 'test')
	#q_time = CreateTests.find_query_time(bf_list, fpr_list, [1000,2000], '_nocomm', 'test')

if __name__ == '__main__':
	main()