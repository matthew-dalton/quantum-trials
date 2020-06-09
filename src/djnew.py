import inspect 
import numpy as np
from qiskit.quantum_info.operators import Operator
from qiskit import Aer, QuantumCircuit, execute, assemble, transpile, IBMQ, QuantumCircuit
import matplotlib.pyplot as plt
import sys


def dj_oracle(case, n):
	# We need to make a QuantumCircuit object to return
	# This circuit has n+1 qubits: the size of the input,
	# plus one output qubit
	oracle_qc = QuantumCircuit(n+1)
	if case == 1:
		case = 'constant'
	else:
		case = 'balanced'
	# First, let's deal with the case in which oracle is balanced
	if case == "balanced":
		for qubit in range(n):
			oracle_qc.cx(qubit, n)

	if case == "constant":
		# First decide what the fixed output of the oracle will be
		# (either always 0 or always 1)
		output = np.random.randint(2)
		if output == 1:
			oracle_qc.x(n)
	oracle_gate = oracle_qc.to_gate()
	oracle_gate.name = "Oracle" # To show when we display the circuit
	return oracle_gate

	
	oracle_gate = oracle_qc.to_gate()
	oracle_gate.name = "Oracle" # To show when we display the circuit
	return oracle_gate

class DeutschJozsa(object):
	"""
	Object that is solely used to construct DJ circuits for different oracles f.
	"""

	def __init__(self):
		pass


	def get_circuit(self, U_f, n_qubits):
		"""Creates the DJ circuit for this function f.

		Parameters
		----------
		f : f : {0,1}^n -> {0,1}
			Takes an n-bit array and outputs 1 bit.
			Either constant or balanced.

		Returns
		-------
		1 if f is constant
		0 if f is balanced
		"""

		# make circuit
		circ = QuantumCircuit(n_qubits+1, n_qubits+1)
		# apply the first hadamard to all qubits
		for i in range(n_qubits):
			circ.h(i)

		# NOT ancilla qubit then apply hadamard
		circ.x(n_qubits)
		circ.h(n_qubits)

		# apply oracle to all qubits
		circ.append(U_f, range(n_qubits+1))

		#Put cx and etc gates on

		# apply hadamard to computational qubits
		for i in range(n_qubits):
			circ.h(i)
		circ.measure(range(0,n_qubits),range(0,n_qubits))
		return circ

	def run(self, f, U_f, n):
		num_shots = 10
		provider = IBMQ.load_account()
		backend = provider.backends.ibmq_16_melbourne
		circuit = self.get_circuit(U_f,n)
		qobj = assemble(transpile(circuit, backend), backend, shots = num_shots)
		job = backend.run(qobj)
		result = job.result()
		counts = result.get_counts()
		print(job.job_id())
		print(counts)
		delayed_results = backend.retrieve_job(job.job_id()).result()
		delayed_counts = delayed_results.get_counts()
		print(delayed_counts)



		
