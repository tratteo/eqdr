import numpy as np
from qiskit import QuantumCircuit
from qiskit.circuit.library import *
from qiskit.quantum_info import partial_trace
from qiskit_aer import AerSimulator, StatevectorSimulator
from src.hodl_qiskit import *

n = 4
q = QuantumRegister(n * 2, "q")
c = ClassicalRegister(1, "c")

circuit = QuantumCircuit(q)

a = 13

comparator = IntegerComparator(num_state_qubits=n, value=a, geq=True)
comparator.decompose().draw(output="mpl", filename="comparator.png")

# circuit.x(q[0])
# circuit.x(q[1])
circuit.x(q[2])
circuit.x(q[3])
circuit.x(q[n])
circuit.h(q[n])
circuit = circuit.compose(comparator)

circuit.h(q[n])
circuit.x(q[n])
sim = AerSimulator()
sm = StatevectorSimulator()
print(circuit)
result = sm.run(transpile(circuit, sm), shots=1).result()
sv = result.get_statevector(circuit)
partial_density_matrix = partial_trace(sv, [0, 1, 2, 3, 5, 6, 7])

# extract the statevector out of the density matrix
partial_statevector = np.diagonal(partial_density_matrix)
print(partial_statevector)
