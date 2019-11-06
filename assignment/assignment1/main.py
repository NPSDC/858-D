import sys

#sys.path.insert(1, 'Rank')
#sys.path.insert(1, 'Select')
sys.path.insert(1, 'Wavelet')
#sys.path.insert(1, 'Rank')
from Wavelet import Wavelet, gen_rand_string
import _pickle as Pi
#from Rank import Rank

def write_rand_string(T, f_name):
	with open(f_name, 'w') as f:
		f.write(T)

def write_access(T, f_name):
	#print(list(map(str, list(range(len(T))))))
	with open(f_name, 'w') as f:
		f.write('\n'.join(list(map(str, list(range(len(T)))))))

def main():
	# T = gen_rand_string(10,20)
	# write_rand_string(T, "inp_file.txt")
	# write_access(T,"acc_file.txt")
	command = sys.argv[1]
	inp_file = sys.argv[2]
	file_2 = sys.argv[3]

	# print(command, inp_file, out_file)

	if(command == 'build'):
		T = ""
		with open(inp_file, 'r') as f:
			T = f.read()
		wavelet_ob = Wavelet(T)
		with open(file_2, "wb") as f_write:
			Pi.dump(wavelet_ob, f_write)
		print(len(wavelet_ob.get_alphabet()))
		print(len(T))

	elif(command == 'access'):
		with open(inp_file, "rb") as f:
			wavelet_ob = Pi.load(f)
		with open(file_2, "r") as f:
			for line in f.readlines():
				print(wavelet_ob.access(int(line)))

	elif(command == 'rank'):
		with open(inp_file, "rb") as f:
			wavelet_ob = Pi.load(f)
		with open(file_2, "r") as f:
			for line in f.readlines():
				vals = line.split('\t')
				print(wavelet_ob.rank(vals[0], int(vals[1])))

	elif(command == 'select'):
		with open(inp_file, "rb") as f:
			wavelet_ob = Pi.load(f)
		with open(file_2, "r") as f:
			for line in f.readlines():
				vals = line.split('\t')
				print(wavelet_ob.select(vals[0], int(vals[1])))

if __name__ == '__main__':
	main()