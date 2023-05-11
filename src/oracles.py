import math
from qiskit.quantum_info import Statevector
from qiskit import QuantumCircuit
from qiskit.visualization import *


def multi_targets_oracle(targets: list[str], n: int) -> Statevector:
    encoding = []
    for i in range(2**n):
        bit_str = "{0:b}".format(i).zfill(n)
        encoding.append("1" if bit_str in targets else "0")
    return Statevector(encoding)
