from grovertwo import Grover

import time
import sys
from random import seed
from random import randrange
import numpy as np
import matplotlib.pyplot as plt

def main():
	
	groverObject = Grover()
	n = 0
	# randomly decide target value
	target = randrange(0,2**(n+2))
	print('Target value: ' + str(target))

	def f(x):
		return (x == target)

	start = time.perf_counter()
	result = groverObject.run(f, n+2)
	print(result)
	end = time.perf_counter()

	worked = (result == target)
	timing = (end - start)
	print(worked)
	print(timing)



if __name__ == "__main__":
	main()