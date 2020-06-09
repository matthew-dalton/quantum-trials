import inspect 
import numpy as np
from qiskit.quantum_info.operators import Operator
from qiskit import Aer, QuantumCircuit, execute, assemble, transpile, IBMQ, QuantumCircuit
import matplotlib.pyplot as plt
import sys


def bv_oracle(s, n):
	oracle_qc = QuantumCircuit(n)
	q = 0

	for char in s:
		if char == "1":
			oracle_qc.cx(q,n-1)
		q += 1
	oracle_gate = oracle_qc.to_gate()
	return oracle_gate
class BernsteinVazirani(object):

	def __init__(self):
		pass



	def run(self, U_f, n):
		# execute circuit on smallest possible qc available
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


	def get_circuit(self, U_f, n_qubits):

		# construct oracle and define its gate constructor
		# construct oracle and define its gate constructor
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

		# apply hadamard to computational qubits
		for i in range(n_qubits):
			circ.h(i)
		circ.measure(range(0,n_qubits+1),range(0,n_qubits+1))
		return circ

		return circ

