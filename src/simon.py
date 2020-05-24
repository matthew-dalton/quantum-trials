import inspect

from qiskit import QuantumCircuit, execute, Aer
from qiskit.visualization import plot_histogram
import numpy as np

class Simon(object):

	def __init__(self):
		pass


	def getOracle(self, f, n):

		# create empty oracle U_f
		oracle = np.zeros(shape=(2**(n+1), 2**(n+1)))

		# properly construct oracle matrix

		return oracle


	def run(self, f, n):
		
		# execute circuit on smallest possible qc available
		simulator = Aer.get_backend('qasm_simulator')
		return self.execute(self.get_circuit(f, n), simulator, f)


	def get_circuit(self, f, n_qubits):

		# construct simon's circuit
		circuit = QuantumCircuit(n, n/2)
		for i in range(n):
			circuit.h(i)
		# custom U_f gate
		for i in range(n):
			circuit.h(i)
		source = []
		dest = []
		for i in range(n/2):
			quantum.append(i + n/2)
			classical.append(n/2)

		circuit.measure(source, dest)
		
		return circuit


	def execute(self, circuit, simulator, f):
		
		# print out (latex) of circuit

		# repeat until we get linear independent equations
		while True:
			job = execute(circuit, simulator, shots=1)
			result = job.result()
			counts = result.get_counts(circuit)
			# if this y is dependent on any of the others, discard it

		# solve the linearly independent equations for s'
		# if f(0^n) = s', then return s'
		# if f(0^n) +\= s', then return 0^n
		
