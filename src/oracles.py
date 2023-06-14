import math
from qiskit.quantum_info import Statevector
from qiskit import QuantumCircuit
from qiskit.visualization import *


def oracles_factory(oracleId: str, **kwargs):
    n = kwargs["size"]
    if oracleId.lower() == "odd":
        return odd_oracle(n)
    elif oracleId.lower() == "even":
        return even_oracle(n)
    elif oracleId.lower() == "targets":
        targets = kwargs["targets"]
        return multi_targets_oracle(targets, n)


def multi_targets_oracle(targets: "list[str]", n: int) -> Statevector:
    encoding = []
    for i in range(2**n):
        bit_str = "{0:b}".format(i).zfill(n)
        encoding.append("1" if bit_str in targets else "0")
    return Statevector(encoding)


def odd_oracle(n: int) -> Statevector:
    encoding = []
    for i in range(2**n):
        encoding.append("1" if i % 2 != 0 else "0")
    return Statevector(encoding)


def even_oracle(n: int) -> Statevector:
    encoding = []
    for i in range(2**n):
        encoding.append("1" if i % 2 == 0 else "0")
    return Statevector(encoding)
