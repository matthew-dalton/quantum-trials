from qiskit import assemble, transpile, IBMQ, QuantumCircuit

circuit = QuantumCircuit(2,2)
circuit.h(0)
circuit.cx(0,1)
circuit.measure([0,1],[0,1])
num_shots = 10

provider = IBMQ.save_account('2e03c3d444ae65d8dc03d7d18b980161ff9127001b55b2bdc6bc8d1f951bee53309b23628e6fac4984b5dfadb4dadf8add910a424973f9fde6ffd0fa4132b053')
provider = IBMQ.load_account()
backend = provider.backends.ibmq_vigo
qobj = assemble(transpile(circuit, backend), backend, shots = num_shots)
job = backend.run(qobj)
result = job.result()
counts = result.get_counts()
print(job.job_id())
print(counts)
delayed_results = backend.retrieve_job(job.job_id()).result()
delayed_counts = delayed_results.get_counts()
print(delayed_counts)