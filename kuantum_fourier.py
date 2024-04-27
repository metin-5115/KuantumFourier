import numpy as np
from numpy import pi
from qiskit import QuantumCircuit, transpile, assemble, Aer, IBMQ
from qiskit.visualization import plot_histogram, plot_bloch_multivector

def qft_olustur(circuit, n):
    if n == 0:
        return circuit
    n -= 1
    circuit.h(n)
    for qubit in range(n):
        circuit.cp(pi/2**(n-qubit), qubit, n)
    qft_olustur(circuit, n)
    return circuit

    
n=4
qc = QuantumCircuit(n)
qft_olustur(qc,n)

for qubit in range(n//2):
    qc.swap(qubit, n-qubit-1) 
    
qc.draw()

qc = QuantumCircuit(3)

# 5 = binary 101. Bu nedenle 1. ve 3. kubitlere X uygulanir.
qc.x(0)
qc.x(2)

# QFT eklenir.
qft_olustur(qc,3)
qc.draw()

sim = Aer.get_backend("aer_simulator")
qc_init = qc.copy()
qc_init.save_statevector()
statevector = sim.run(qc_init).result().get_statevector()
plot_bloch_multivector(statevector)

def inverse_qft(circuit, n):
    qft_circ = qft_olustur(QuantumCircuit(n), n)
    invqft_circ = qft_circ.inverse()
    invqft_circ.draw()
    circuit.append(invqft_circ, circuit.qubits[:n])
    return circuit.decompose()
    
n=4
qc = QuantumCircuit(n, n)
qc = inverse_qft(qc, n)
qc.draw()


n=3
qc = QuantumCircuit(n)

# 5 = binary 101. Bu nedenle 1. ve 3. kubitlere X uygulanir.
qc.x(0)
qc.x(2)

# QFT eklenir.
qc = qft_olustur(qc, n)
qc.barrier()
inverse_qft(qc, n)
qc.measure_all()
qc.draw()


from qiskit.providers.aer import QasmSimulator
sim = QasmSimulator()
qc = transpile(qc, sim)
counts = sim.run(qc).result().get_counts()
plot_histogram(counts)






