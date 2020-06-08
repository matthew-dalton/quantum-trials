import inspect

from qiskit import Aer, QuantumCircuit, execute, assemble, transpile, IBMQ, QuantumCircuit
from qiskit.visualization import plot_histogram
from qiskit.tools.visualization import circuit_drawer
from qiskit.extensions import UnitaryGate

import numpy as np
import sympy

class Simon(object):

	def __init__(self):
		pass


	def getOracle(self, f, n):
		# note that n represents the total number of qubits, computational and ancillary

		# create empty oracle U_f
		oracle = np.zeros(shape=(2**(2*n), 2**(2*n)))

		# properly construct oracle matrix
		for x in range(2**n):
			y = f(x)

			# the output is XOR(f(x), b) for each b
			for i in range(2**n):
				oracle[(x<<n)+i][(x<<n)+(i^y)] = 1

		# print("Peak at Oracle: ")
		# print(oracle)

		return UnitaryGate(oracle)


	def run(self, f, n):
		
		# execute circuit on smallest possible qc available
		# print(circuit_drawer(self.get_circuit(f,n)))
		provider = IBMQ.save_account('2e03c3d444ae65d8dc03d7d18b980161ff9127001b55b2bdc6bc8d1f951bee53309b23628e6fac4984b5dfadb4dadf8add910a424973f9fde6ffd0fa4132b053')
		provider = IBMQ.load_account()
		backend = provider.backends.ibmq_16_melbourne
		return self.execute(self.get_circuit(f, n), backend, f, n)



	def get_circuit(self, f, n):

		# construct simon's circuit
		circuit = QuantumCircuit(2*n, n)
		for i in range(n):
			circuit.h(i+n)
		U_f = self.getOracle(f,n)
		circuit.append(U_f, range(2*n))
		for i in range(n):
			circuit.h(i+n)
		source = []
		dest = []
		for i in range(n):
			source.append(i + n)
			dest.append(i)

		circuit.measure(source, dest)
		
		return circuit


	def execute(self, circuit, backend, f, n):
		
		# print out (latex) of circuit

		# repeat until we get linear independent equations
		i = 1
		while True:
			print('Circuit Trial: ' + str(i))
			i += 1
			
			qobj = assemble(transpile(circuit, backend, optimization_level=3), backend, shots = n-1)
			job = backend.run(qobj)
			delayed_results = backend.retrieve_job(job.job_id()).result()
			counts = delayed_results.get_counts()
			if len(counts) == (n-1):
				m = []
				for y in counts:
					m.append(np.fromstring(' '.join(y), dtype=np.uint8, sep=' '))
				matrix = sympy.Matrix(np.array(m))
				nullspace = matrix.nullspace()
				# print('nullspace: ' + str(nullspace))
				if len(nullspace) == 1:
					print(matrix)
					s_int = nullspace[0].transpose().tolist()[0]
					s_char = [str(abs(bit)) for bit in s_int]
					s_string = ''.join(s_char)
					s = int(s_string, 2)
					print("Potential s value: " + str(s))
					return s if f(s) == f(0) else 0
