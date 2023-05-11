from multiprocessing import Process
from typing import Callable, Union
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector, random_statevector
from qiskit.circuit.library import *
import math
from eqiro import Eqiro
from qiskit.visualization import *
import csv
import random
import json
from grover import execute_grover
from oracles import multi_targets_oracle

from utils import generate_binary_string, loadConfig


def oracle_factory(
    genome: str, fitness: float, size: int
) -> Union[QuantumCircuit, Statevector]:
    # return Statevector.from_label(genome)
    list = []
    for i in range(2**size):
        list.append("0" if i % 2 == 0 else "1")
    return Statevector(list)


def fitness_function_factory(targets: list[str]) -> Callable[[str, int], float]:
    def fitness_function(genome: str, size: int) -> float:
        min_dist = math.inf
        genome_val = int(genome, 2)
        for t in targets:
            v = int(t, 2)
            d = abs(genome_val - v)
            if d < min_dist:
                min_dist = d
        return min_dist
        # if val % 2 == 0:
        #     return math.inf
        # a = (2**size) / 2
        # if val - a == 0:
        #     return 0
        # return 1 - (math.sin(val - a) / (val - a))

    return fitness_function


def distance(first: str, second: str) -> int:
    if len(first) != len(second):
        print("error")
        return 0
    h = 0
    for i in range(len(first)):
        if first[i] != second[i]:
            h += 1
    return h


def eqiro_run(config: any):
    n = config["size"]
    targets = config["targets"]
    its = config["its"]
    id = config["id"]
    oracle = multi_targets_oracle(targets, n)
    file_name = (
        "eqiro_"
        + ("recombined" if config["enable_recombination"] else "not_recombined")
        + ".csv"
    )
    print(str(id) + " > recombine: " + str(config["enable_recombination"]))
    count = 0
    with open(file_name, "w", newline="") as file:
        csvwriter = csv.writer(file)
        csvwriter.writerow(["n", "avg_iterations", "avg_recombinations"])
    eqiro = Eqiro(
        oracle=oracle,
        fitnessFunction=fitness_function_factory(targets),
        genomeSize=n,
        is_good_state=lambda x: x in targets,
        verbosity=0,
        **config,
    )
    iterations = 0
    recombinations = 0
    for j in range(its):
        res = eqiro.optimize()
        iterations += res.statistics["iterations"]
        recombinations += res.statistics["recombinations"]
        count += 1
        print(str(id) + " > it: " + str(count) + "/" + str(its))
    iterations /= its
    recombinations /= its
    with open(file_name, "a", newline="") as file:
        csvwriter = csv.writer(file)
        csvwriter.writerow([its, iterations, recombinations])


if __name__ == "__main__":
    config = loadConfig("config/std.json")
    n = config["size"]
    targets = [generate_binary_string(n) for i in range(random.randint(1, n // 2))]
    print(targets)
    oracle = multi_targets_oracle(targets, n)

    # if n < 8:
    #     oracle.draw(output="bloch", filename="oracle.png")
    # res = execute_grover(oracle, is_good_state=lambda x: x in targets)
    # if n < 8:
    #     plot_distribution(
    #         res.circuit_results[0],
    #         filename="plot.png",
    #         figsize=(16, 9),
    #         bar_labels=False,
    #     )
    its = 100
    config["targets"] = targets
    config["its"] = its

    c1 = json.loads(json.dumps(config))
    c1["enable_recombination"] = True
    c1["id"] = 0

    c2 = json.loads(json.dumps(config))
    c2["enable_recombination"] = False
    c2["id"] = 1

    t1 = Process(target=eqiro_run, args=[c1])
    t2 = Process(target=eqiro_run, args=[c2])
    t1.start()
    t2.start()
    t1.join()
    t2.join()

    print("_" * 100)
