import math
from typing import Callable
from qiskit.algorithms import AmplificationProblem
from qiskit.quantum_info import Statevector
from utils import generate_binary_string, loadConfig
from qiskit.algorithms import Grover
from qiskit.primitives import Sampler
from qiskit import QuantumCircuit
from qiskit.visualization import *
import matplotlib.pyplot as plt
import time


def execute_grover(
    oracle: any,
    is_good_state: Callable[[str], bool] | list[int] | list[str] | Statevector | None,
):
    start_time = time.time_ns()
    problem = AmplificationProblem(oracle, is_good_state=is_good_state)
    grover = Grover(sampler=Sampler())
    result = grover.amplify(problem)
    print(
        f"executed grover O({len(problem.objective_qubits)}) in { str((time.time_ns() - start_time) / 1e6) } ms\nresult: {result.assignment}, good state: {'uknown' if is_good_state is None else is_good_state(result.assignment)}"
    )

    return result
