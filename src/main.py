import json
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
from qiskit.algorithms import AmplificationProblem
from bbht import BBHT, BBHTResult
from qiskit.primitives import Sampler
from qiskit.circuit.library.phase_oracle import PhaseOracle
from qiskit.visualization import plot_distribution
import math
from random import choice
from tqdm import tqdm
import multiprocessing as mp


def generate_binary_string(n):
    return "".join(choice("01") for _ in range(n))


def loadConfig(path: str):
    f = open(path)
    data = json.load(f)
    return data


def iteration(config):
    pass


if __name__ == "__main__":
    config = loadConfig("config/std.json")

    n = 6

    its = 0
    sampleIts = 10
    print("Calculating average iterations")
    pbar = tqdm(range(sampleIts))
    for i in pbar:
        target = generate_binary_string(n)
        oracle = Statevector.from_label(target)
        targets = [target]
        bbht = BBHT(targets=targets, oracle=oracle)
        result = bbht.amplify()
        its += result.iterations
        pbar.set_description(
            "BBHT found "
            + result.resultState
            + " in "
            + str(result.iterations)
            + " iterations"
        )
    print("N: " + str(n) + ", " + str(int(math.pow(2, n))) + " possible states")
    print(
        "Theoretical upper bound iterations: "
        + str(math.ceil(math.sqrt(math.pow(2, n) / len([1]))))
    )
    print("Empirical average iterations: " + str(its / sampleIts))
