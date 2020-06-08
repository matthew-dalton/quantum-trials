from simontwo import Simon

import time
import sys
from random import seed
from random import randint
from random import randrange
import numpy as np
import matplotlib.pyplot as plt

def main():
	
	simonObject = Simon()

	# constants
	n = 1

	# randomly decide f
	# for ease of construction, the output for each x,y such that x^y=s is min(x,y)
	s = randint(0,2**n - 1)
	print("S: " + "{0:b}".format(s))
	def f(x):
		return x if (x^s > x) else x^s

	start = time.perf_counter()
	result = simonObject.run(f, n)
	end = time.perf_counter()

	print("Result = " + str(result) + (": Worked" if result == s else ": Failed"))
	timing= (end - start)
	print(timing)


if __name__ == "__main__":
	main()
