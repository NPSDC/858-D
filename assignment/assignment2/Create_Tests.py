import sys
import os
import string
import numpy as np

class CreateTests(object):
	@staticmethod
	def create_rand_keys(num_keys, max_key_size = 100, check_keys = [], file_write = None, ret = False):
		letters = string.printable
		for num in range(num_keys):
			while(1):
				key_size = np.random.randint(5, max_key_size + 1)
				rand_numbers = np.random.choice(len(letters), key_size, replace = False)
				key = repr(''.join([letters[i] for i in rand_numbers]))
				if not key in check_keys:
					check_keys.append(key)
					break

		if(file_write is not None):
			ret = False
			with open(file_write, 'w') as f:
				for num in range(len(check_keys)):
					if(num < (len(check_keys) - 1)):
						f.write(check_keys[num] + "\n")
					else:
						f.write(check_keys[num])

		if(ret):
			return check_keys

	@staticmethod
	def create_test_query(key_file, type):
		if(os.path.exists(key_file)):
			if not type in [1,2]:
				sys.exit("Invalid type")
			keys = []
			with open(key_file, 'r') as f:
				for key in f.readlines():
					keys.append(key.strip('\n'))

			if(type == 1):
				CreateTests.create_rand_keys(num_keys = len(keys), check_keys = keys, file_write = key_file.split('.')[0] + "_nocomm.txt")		
			else:
				CreateTests.create_rand_keys(num_keys = len(keys)//2, \
					check_keys = [keys[i] for i in list(np.random.choice(len(keys), len(keys)//2, replace = False))], \
				 	file_write  = key_file.split('.')[0] + "_50comm.txt")

	@staticmethod
	def gen_files(n_keys_list, directory):
		if(os.path.exists(directory)):
			for n_keys in n_keys_list:
				key_file = os.path.join(directory, "{}.txt".format(n_keys))
				CreateTests.create_rand_keys(n_keys, file_write = key_file)
				CreateTests.create_test_query(key_file, 1)
				CreateTests.create_test_query(key_file, 2)
		else:
			sys.exit("Invalid directory Path")

def main():
	CreateTests.gen_files([1000,2000], 'test')

if __name__ == '__main__':
	main()