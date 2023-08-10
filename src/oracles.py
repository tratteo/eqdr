import math
from qiskit.quantum_info import Statevector
from qiskit import QuantumCircuit
from qiskit.circuit.library.phase_oracle import PhaseOracle
from qiskit.visualization import *


def oracles_factory(n: int, **kwargs):
    oracleId = kwargs["operator"].lower()
    if oracleId == "odd":
        return odd_oracle(n)
    elif oracleId == "even":
        return even_oracle(n)
    elif oracleId == "distance":
        return distance_oracle(n)
    elif oracleId == "targets":
        targets = kwargs["targets"]
        return multi_targets_oracle(targets, n)
    elif oracleId == "pattern":
        return pattern_oracle(kwargs["expression"], n)
    elif oracleId == "phase":
        return PhaseOracle(kwargs["expression"])


def distance_oracle(n: int) -> Statevector:
    encoding = []
    for i in range(2**n):
        encoding.append("1" if abs(i - n) < n else "0")
    return Statevector(encoding)


def pattern_oracle(pattern: str, n: int) -> Statevector:
    encoding = []
    for i in range(2**n):
        bit_str = "{0:b}".format(i).zfill(n)
        valid = True
        for i, c in enumerate(pattern):
            if c != "*" and bit_str[i] != c:
                valid = False
                break
        encoding.append("1" if valid else "0")

    return Statevector(encoding)


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
