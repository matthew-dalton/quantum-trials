import inspect

from qiskit import QuantumCircuit, execute, Aer
from qiskit.visualization import plot_histogram
from qiskit.tools.visualization import circuit_drawer
from qiskit.extensions import UnitaryGate
import numpy as np

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
		simulator = Aer.get_backend('qasm_simulator')
		print(circuit_drawer(self.get_circuit(f,n)))
		return self.execute(self.get_circuit(f, n), simulator, f)


	def get_circuit(self, f, n):

		# construct simon's circuit
		circuit = QuantumCircuit(2*n, n)
		print(f'n: {n}')
		for i in range(n):
			circuit.h(i+n)
		U_f = self.getOracle(f,n)
		print("Successfully received oracle")
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


	def execute(self, circuit, simulator, f):
		
		# print out (latex) of circuit

		# repeat until we get linear independent equations
		job = execute(circuit, simulator, shots=1)
		result = job.result()
		counts = result.get_counts(circuit)
		print(counts)
		# while True:
		# 	job = execute(circuit, simulator, shots=1)
		# 	result = job.result()
		# 	counts = result.get_counts(circuit)
			# if this y is dependent on any of the others, discard it

		# solve the linearly independent equations for s'
		# if f(0^n) = s', then return s'
		# if f(0^n) +\= s', then return 0^n
		
