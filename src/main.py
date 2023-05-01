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
from scipy.spatial.distance import hamming

import multiprocessing as mp

from eqiro import Eqiro


def generate_binary_string(n):
    return "".join(choice("01") for _ in range(n))


def loadConfig(path: str):
    f = open(path)
    data = json.load(f)
    return data


def oracle_factory(genome: str, fitness: float) -> QuantumCircuit | Statevector:
    return Statevector.from_label(target)


def fitness_function(genome: str) -> float:
    return 0 if genome == target else 1


def distance(first: str, second: str) -> int:
    if len(first) != len(second):
        print("error")
        return 0
    h = 0
    for i in range(len(first)):
        if first[i] != second[i]:
            h += 1
    return h


if __name__ == "__main__":
    config = loadConfig("config/std.json")
    n = config["size"]
    target = generate_binary_string(n)
    print("configuration " + json.dumps(config))
    h = 0
    its = 10
    correct = 0
    for i in range(its):
        eqiro = Eqiro(
            oracleFactory=oracle_factory,
            fitnessFunction=fitness_function,
            genomeSize=n,
            **config,
            verbosity=0
        )
        res = eqiro.optimize()
        print("-" * 50)
        print("\ntarget: " + target)
        print("proposed solution: " + res.solutions[0][0])
        d = distance(target, res.solutions[0][0])
        h += d
        if d <= 0:
            correct += 1
    h /= its
    print("_" * 100)
    print(
        "average hamming distance "
        + str(h)
        + ", success rate "
        + str(100 * correct / its)
        + "%"
    )
    # n = 6

    # its = 0
    # sampleIts = 10
    # print("Calculating average iterations")
    # pbar = tqdm(range(sampleIts))
    # for i in pbar:
    #     target = generate_binary_string(n)
    #     oracle = Statevector.from_label(target)
    #     targets = [target]
    #     bbht = BBHT(targets=targets, oracle=oracle)
    #     result = bbht.amplify()
    #     its += result.iterations
    #     pbar.set_description(
    #         "BBHT found "
    #         + result.resultState
    #         + " in "
    #         + str(result.iterations)
    #         + " iterations"
    #     )
    # print("N: " + str(n) + ", " + str(int(math.pow(2, n))) + " possible states")
    # print(
    #     "Theoretical upper bound iterations: "
    #     + str(math.ceil(math.sqrt(math.pow(2, n) / len([1]))))
    # )
    # print("Empirical average iterations: " + str(its / sampleIts))
