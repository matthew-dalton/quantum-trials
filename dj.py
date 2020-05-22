import inspect 
import numpy as np
from qiskit.quantum_info.operators import Operator
from qiskit import Aer, QuantumCircuit, execute
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
		# First generate a random number that tells us which CNOTs to
		# wrap in X-gates:
		b = np.random.randint(1,2**n)
		# Next, format 'b' as a binary string of length 'n', padded with zeros:
		b_str = format(b, '0'+str(n)+'b')
		# Next, we place the first X-gates. Each digit in our binary string 
		# corresponds to a qubit, if the digit is 0, we do nothing, if it's 1
		# we apply an X-gate to that qubit:
		for qubit in range(len(b_str)):
			if b_str[qubit] == '1':
				oracle_qc.x(qubit)
		# Do the controlled-NOT gates for each qubit, using the output qubit 
		# as the target:
		for qubit in range(n):
			oracle_qc.cx(qubit, n)
		# Next, place the final X-gates
		for qubit in range(len(b_str)):
			if b_str[qubit] == '1':
				oracle_qc.x(qubit)

	# Case in which oracle is constant
	if case == "constant":
		# First decide what the fixed output of the oracle will be
		# (either always 0 or always 1)
		output = np.random.randint(2)
		if output == 1:
			oracle_qc.x(n)
	
	oracle_gate = oracle_qc.to_gate()
	oracle_gate.name = "Oracle" # To show when we display the circuit
	return oracle_gate

class DeutschJozsa(object):
	"""
	Object that is solely used to construct DJ circuits for different oracles f.
	"""

	def __init__(self):
		pass


	def getOracle(self,f, n):
		"""Constructs the quantum oracle U_f from classical oracle f.

		Parameters
		----------
		f : f : {0,1}^n -> {0,1}
			Takes an n-bit array and outputs 1 bit.
			Either constant or balanced.

		Returns
		-------
		2^(n+1) by 2^(n+1) numpy matrix containing the oracle U_f
		"""

		# create empty oracle U_f
		# We need to make a QuantumCircuit object to return
		# This circuit has n+1 qubits: the size of the input,
		# plus one output qubit


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
		print(oracle)

		# populate oracle according to f
		# basically,
			# when f(x)=0 apply Identity to ancilla qubit
			# when f(x)=1 apply NOT to ancilla qubit
		b = np.random.randint(1,2**n)
		b_str = format(b, '0'+str(n)+'b')
		oracle_qc = QuantumCircuit(n+1)
		for i in range(len(b_str)):
			if b_str[i] == '1':
				oracle_qc.x(i)
		for j in range(n):
			oracle_qc.cx(j,n)
		for k in range(len(b_str)):
			if b_str[k] == '1':
				oracle_qc.x(k)
		print(oracle_qc)
		oracle_gate = oracle_qc.to_gate()
		oracle_gate.name = "Oracle" # To show when we display the circuit
		return oracle_gate


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
		np.set_printoptions(threshold=sys.maxsize)
		backend = Aer.get_backend('qasm_simulator')
		circ = self.get_circuit(U_f,n)
		print('got circuit', circ)
		result = self.execute(circ, backend)
		print(result)




	def execute(self, circ, backend):
		job = execute(circ, backend)
		result = job.result().get_counts()
		return result
		
