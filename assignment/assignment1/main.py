import sys

#sys.path.insert(1, 'Rank')
#sys.path.insert(1, 'Select')
sys.path.insert(1, 'Wavelet')
#sys.path.insert(1, 'Rank')
from Wavelet import Wavelet
#from Rank import Rank

def main():
	val = Wavelet("0000111")
	command = sys.argv[1]
	inp_file = sys.argv[2]
	out_file = sys.argv[3]

	print(command, inp_file, out_file)

	if(command == 'build'):
		T = ""
		with open(inp_file, 'r') as f:
			print(f.read())
		print(T)

if __name__ == '__main__':
	main()