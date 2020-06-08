from bvnew import BernsteinVazirani

import time
import sys
from random import seed
from random import randint
from random import randrange
import numpy as np
import matplotlib.pyplot as plt
import bv

def main():
	
	bvObject = BernsteinVazirani()

	# constants
	n = 1
	ITERATIONS = 1



	print('Testing out Bernstein-Vazirani alorithm...')

	seed(3245234)
	# randomly decide f
	a = randrange(0,2**(n+1))
	b = randint(0,1)
	hstr = ""
	for i in range(n+2):
		hstr+=str(randint(0,1))
	print(hstr[::-1])
	oracle = bv.bv_oracle(hstr,n+3)
	start = time.perf_counter()
	bvObject.run(oracle, n+2)
	end = time.perf_counter()

	timing = (end - start)

	print(timing)
	average_runtimes = []

if __name__ == "__main__":
	main()
