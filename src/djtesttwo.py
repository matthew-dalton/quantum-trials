from djnew import DeutschJozsa
import djnew as dj
import time
import sys
from random import seed
from random import randint
import numpy as np
import matplotlib.pyplot as plt
import numpy as np
from qiskit import *


def main():
	
	djObject = DeutschJozsa()

	# constants
	n = 1


	# randomly decide f
	const_val = randint(0,1)
	def f_constant(_):
		return const_val
	def f_balanced(x):
		return x%2

	constant = randint(0,1)
	f = f_constant if constant else f_balanced
	print(constant)
	oracle = dj.dj_oracle(constant, n+2)
	start = time.perf_counter()
	result = djObject.run(f,oracle, n+2)
	end = time.perf_counter()

	# print('worked' if result == constant else 'failed')
	timing = (end - start)
	print(timing)


if __name__ == "__main__":
	main()