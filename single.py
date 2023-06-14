import math
from qiskit.algorithms import Grover, AmplificationProblem
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram
from qiskit import QuantumCircuit, ClassicalRegister, transpile
from qiskit.circuit.library import GroverOperator
from qiskit.quantum_info import Statevector, random_statevector
from qiskit.primitives import Sampler
from src.eqiro import Eqiro
import random
from src.fitness import fitness_factory, sin_fitness
from src.gamma import polyGamma
from src.oracles import multi_targets_oracle, odd_oracle, oracles_factory


def calculate_target_bits(genomeSize, b: "list[tuple[str, float]]") -> "list[float]":
    angles = [0] * genomeSize
    b.sort(key=lambda x: x[1])
    for i in range(genomeSize):
        gc = []
        for k in range(len(b)):
            current = b[k]
            g = polyGamma(
                current[1],
                k,
                a=0.75,
                k=len(b),
            )
            gc.append(g)
            angles[i] += (-1 if current[0][i] == "0" else 1) * g
    print(b, flush=True)
    print(gc, flush=True)
    print(angles, flush=True)
    res = [0 if a < 0 else 1 for a in angles]
    print(res, flush=True)
    return res


if __name__ == "__main__":
    # config = {
    #     "size": 4,
    #     "k_out": 3,
    #     "g_alpha": 0.75,
    #     "gamma_mul": 1,
    #     "recombination_module": 3,
    #     "lambda": 1.2,
    #     "oracle": "odd",
    #     "recombine": True,
    #     "fitness_function": "square",
    #     "diffusion_recombine": True,
    #     "gamma": "gaussian",
    #     "target_fitness": 0,
    #     "fitness_threshold": 0.1,
    #     "mutate_factor": 1 / 6,
    #     "iterations": 50,
    # }
    # # targets = calculate_target_bits(3, [["100", 0], ["000", 1], ["000", 2], ["000", 3]])
    # # exit()
    # fitness_function = fitness_factory(config["fitness_function"], **config)
    # oracle = oracles_factory(config["oracle"], **config)
    # eq = Eqiro(
    #     fitnessFunctionImp=fitness_function,
    #     oracleImp=oracle,
    #     verbosity=1,
    #     **config,
    # )
    # qc, _ = eq.construct_circuit(
    #     2, [["0000", 0], ["0000", 1], ["0000", 2], ["0000", 3]], 30
    # )
    # qc.decompose(reps=3).draw(
    #     filename="recombination_3.png",
    #     output="mpl",
    #     vertical_compression="high",
    # )
    # exit()
    # res = eq.optimize()
    # print(res)
    # exit()
    n = 1
    targets = calculate_target_bits(n, [["00", 0]])
    qc = QuantumCircuit(n * 2)
    # qc.h(0)
    # qc.h(1)
    # qc.h(2)
    # qc.h(3)
    qc.ry(math.pi / 3, 0)
    # qc.rx(random.uniform(-math.pi / 3, math.pi / 3), 1)
    # qc.rx(random.uniform(-math.pi / 3, math.pi / 3), 2)
    # qc.rx(random.uniform(-math.pi / 3, math.pi / 3), 3)
    for i, t in enumerate(targets):
        # print("i: " + str(i) + ", t: " + str(t))
        p = AmplificationProblem(
            oracle=Statevector.from_label("00" if t == 0 else "11"),
            is_good_state=["00" if t == 0 else "11"],
            objective_qubits=[i, i + n],
        )

        qc.h(i + n)
        qc.compose(p.grover_operator.power(1), qubits=p.objective_qubits, inplace=True)
        # for i in range(n):
        #     qc.rx(
        #         random.uniform(
        #             -math.pi * (1 / 4),
        #             math.pi * (1 / 4),
        #         ),
        #         i,
        #     )

    meas = ClassicalRegister(n * 2)
    qc.add_register(meas)
    m = [i for i in range(n * 2)]
    qc.measure(m, reversed(m))
    qc.decompose(reps=3).draw(filename="qc.png", output="mpl")

    bk = AerSimulator()
    job_sim = bk.run(transpile(qc, bk), shots=4096)
    result_sim = job_sim.result()
    print(result_sim.get_counts())

    plot_histogram(result_sim.get_counts(), filename="graph.png", figsize=(21, 9))
