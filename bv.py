import inspect 
import numpy as np
from qiskit.quantum_info.operators import Operator
from qiskit import Aer, QuantumCircuit, execute
import matplotlib.pyplot as plt
import sys

class BernsteinVazirani(object):

	def __init__(self):
		pass


	def getOracle(self, f, n):

		# create empty oracle U_f
		oracle = np.zeros(shape=(2**(n+1), 2**(n+1)))

		# populate oracle according to f
		# basically,
			# when f(x)=0 apply Identity to ancilla qubit
			# when f(x)=1 apply NOT to ancilla qubit
		for i in range(2**n):
			if f(i) == 0:
				oracle[2*i][2*i] = 1
				oracle[2*i+1][2*i+1] = 1
			else:
				oracle[2*i+1][2*i] = 1
				oracle[2*i][2*i+1] = 1

		return oracle


	def run(self, f, n):
		# execute circuit on smallest possible qc available
		backend = Aer.get_backend('qasm_simulator')
		circ = self.get_circuit(f,n)
		print('got circuit', circ)
		result = self.execute(circ, backend)
		print(result)


	def get_circuit(self, f, n_qubits):

		# construct oracle and define its gate constructor
		# construct oracle and define its gate constructor
		U_f = Operator(self.getOracle(f,n_qubits))
		# make circuit
		circ = QuantumCircuit(n_qubits+1, n_qubits+1)
		# apply the first hadamard to all qubits
		for i in range(n_qubits):
			circ.h(i)

		# NOT ancilla qubit then apply hadamard
		circ.x(n_qubits)
		circ.h(n_qubits)

		# apply oracle to all qubits
		circ.unitary(U_f, range(0,n_qubits+1))

		# apply hadamard to computational qubits
		for i in range(n_qubits):
			circ.h(i)
		circ.measure(range(0,n_qubits+1),range(0,n_qubits+1))
		return circ

		return circ


	def execute(self, circ, backend):
		job = execute(circ, backend)
		result = job.result().get_counts()
		return result
