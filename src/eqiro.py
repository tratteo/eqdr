import csv
import math
from typing import Callable, Union
from qiskit import QuantumCircuit, ClassicalRegister, execute
import random
from qiskit.quantum_info import Statevector
from qiskit import Aer
from src.fitness import fitness_factory
from src.oracles import multi_targets_oracle, oracles_factory
from src.gamma import gaussianGamma, identityGamma, polyGamma
from qiskit.algorithms import AmplificationProblem


def eqiro_run(config: any):
    n = config["size"]
    targets = config.get("targets", None)
    fitness_function = fitness_factory(config["fitness_function"], **config)
    oracle = oracles_factory(config["oracle"], **config)
    its = config["iterations"]
    id = config["id"]
    prefix = config.get("prefix", None)
    if prefix is None:
        prefix = ""
    else:
        prefix += " - "
    reportFileName = config["report"]
    # print(str(id) + " > targets: " + str(targets))
    # oracle = odd_oracle(n=n)

    backend = Aer.get_backend("qasm_simulator")
    count = 0
    with open(reportFileName, "w", newline="") as file:
        csvwriter = csv.writer(file)
        csvwriter.writerow(
            ["n", "avg_iterations", "avg_recombinations", "avg_fitness_calls"]
        )
    eqiro = Eqiro(
        oracleImp=oracle,
        fitnessFunctionImp=fitness_function,
        isGoodState=lambda x: x in targets if targets is not None else None,
        verbosity=0,
        **config,
    )
    iterations = 0
    recombinations = 0
    fitnessCalls = 0
    for j in range(its):
        res = eqiro.optimize()
        iterations += res.statistics["iterations"]
        recombinations += res.statistics["recombinations"]
        fitnessCalls += res.statistics["fitness_calls"]
        count += 1
        print(
            prefix
            + str(id)
            + " > it: "
            + str(count)
            + "/"
            + str(its)
            + " - "
            + str({"avg_it": iterations / (j + 1), "avg_rec": recombinations / (j + 1)})
        )
    iterations /= its
    fitnessCalls /= its
    recombinations /= its
    with open(reportFileName, "a", newline="") as file:
        csvwriter = csv.writer(file)
        csvwriter.writerow([its, iterations, recombinations, fitnessCalls])


class EqiroResult:
    def __init__(
        self,
        solutions: "list[tuple[str, float]]",
        statistics: any,
    ) -> None:
        self.solutions: list[tuple[str, float]] = solutions
        self.statistics = statistics


class Eqiro:
    def __init__(
        self,
        oracleImp: Union[QuantumCircuit, Statevector],
        fitnessFunctionImp: Callable[[str, int], float],
        backend: any = None,
        isGoodState: Callable[[str], bool] = None,
        **kwargs,
    ) -> None:
        self.problem = AmplificationProblem(oracle=oracleImp)
        self.fitnessFunction = fitnessFunctionImp
        self.isGoodState = isGoodState
        self.backend = Aer.get_backend("qasm_simulator") if backend is None else backend
        self.verbosity = kwargs.get("verbosity", 1)
        self.gamma = self._getGamma(kwargs.get("gamma", "gaussian"))
        self.lmbd = kwargs.get("lambda", 4 / 3)
        self.recombinationProb = kwargs.get("recombination_prob", 0.4)
        self.genomeSize = self.problem.oracle.num_qubits
        self.gammaMul = kwargs.get("gamma_mul", 1)
        self.maxIter = kwargs.get("max_iterations", math.inf)
        self.diffusionRecombine = kwargs.get("diffusion_recombine", True)
        self.fitnessThreshold = kwargs.get("fitness_threshold", None)
        self.targetFitness = kwargs.get("target_fitness", None)
        self.mutateFactor = kwargs.get("mutate_factor", None)
        self.recombine = kwargs.get("recombine", True)
        self.kOut = kwargs.get("k_out", self.genomeSize // 2)
        self.gAlpha = kwargs.get("g_alpha", 0.5)

        if self.fitnessThreshold is not None and self.targetFitness is None:
            raise AssertionError(
                "target fitness must be specified if a fitness threshold is specified",
            )
        if self.fitnessFunction is None and self.recombine:
            raise AssertionError(
                "cannot apply recombination algorithm without a fitness function",
            )

    def _generate_binary_string(self, n):
        return "".join(random.choice("01") for _ in range(n))

    def optimize(self) -> EqiroResult:
        b_out: list[tuple[str, float]] = []
        solutions = []
        recombinations = 0
        iteration = 0
        fitnessCalls = 0
        recombinationIndex = 0
        m = 1
        while iteration < self.maxIter:
            qc, recombined = self.construct_circuit(
                power=random.randint(1, m),
                b_out=b_out,
                iteration=iteration,
            )
            if recombined:
                recombinations += 1 if recombined else 0

            result = execute(qc, self.backend, shots=1).result()
            # print(result.get_counts())
            measured = list(result.get_counts().keys())[0]

            if self.verbosity > 1:
                print(
                    "amplitude amplification, m: "
                    + str(m)
                    + ", measured: "
                    + str(measured)
                )
            if self.fitnessFunction is not None:
                fitness = self.fitnessFunction(measured, self.genomeSize)
                fitnessCalls += 1
            else:
                fitness = 0

            if self.verbosity > 0:
                print("iteration " + str(iteration))
                print("measured " + str(measured))
                print("fitness " + str(fitness))

            if next(filter(lambda x: x[0] == measured, b_out), None) is None:
                b_out.append([measured, fitness])
                if len(b_out) > self.kOut:
                    b_out.sort(key=lambda x: x[1])
                    b_out.pop()
                # self.problem = AmplificationProblem(
                #     oracle=multi_targets_oracle([b[0] for b in b_out], self.genomeSize)
                # )

            solutions.append([measured, fitness])
            solutions.sort(key=lambda x: x[1])
            if len(solutions) > 10:
                solutions.pop()

            iteration += 1
            recombinationIndex += 1
            if self.isGoodState is not None:
                if self.isGoodState(measured):
                    break
            if (
                self.targetFitness is not None
                and abs(fitness - self.targetFitness) <= self.fitnessThreshold
            ):
                break
            m = math.ceil(
                min(
                    self.lmbd * m,
                    math.sqrt(math.pow(2, self.genomeSize)),
                )
            )

        solutions.sort(key=lambda x: x[1])
        return EqiroResult(
            solutions=solutions,
            statistics={
                "iterations": iteration,
                "recombinations": recombinations,
                "fitness_calls": fitnessCalls,
            },
        )

    def calculate_angles(self, b: "list[tuple[str, float]]") -> "list[float]":
        angles = [0] * self.genomeSize
        c = math.pi / len(b)
        b.sort(key=lambda x: x[1])
        for i in range(self.genomeSize):
            theta = 0
            for k in range(len(b)):
                current = b[k]
                gamma = self.gamma(
                    current[1],
                    k,
                    a=self.gAlpha,
                    k=len(b),
                )
                if self.verbosity > 1:
                    print("computed gamma " + str(gamma))
                theta += int(current[0][i]) * gamma * self.gammaMul
            angles[i] = theta * c
        return angles

    def compute_diffusions_bits(self, b: "list[tuple[str, float]]") -> "list[float]":
        angles = [0] * self.genomeSize
        b.sort(key=lambda x: x[1])
        for i in range(self.genomeSize):
            gc = []
            for k in range(len(b)):
                current = b[k]
                g = self.gamma(
                    current[1],
                    k,
                    a=self.gAlpha,
                    k=len(b),
                )
                gc.append(g)
                angles[i] += (-1 if current[0][i] == "0" else 1) * g
        low = min(angles)
        high = max(angles)

        angles = [
            1 - 0 if high - low == 0 else ((a - low) / (high - low)) for a in angles
        ]
        res = [0 if a < 0.5 else 1 for a in angles]
        if self.verbosity > 1:
            print("\n", flush=True)
            print(gc, flush=True)
            print(b, flush=True)
            print(angles, flush=True)
            print(res, flush=True)
        return res

    def construct_circuit(
        self,
        power: int,
        b_out: "list[tuple[str, float]]",
        iteration: int,
    ) -> tuple[QuantumCircuit, bool]:
        shouldRecombine = (
            self.recombine
            and len(b_out) >= self.kOut
            and random.random()
            < math.tanh(iteration / (self.genomeSize**2)) * (self.recombinationProb)
        )

        qubits = (
            self.genomeSize * 2
            if shouldRecombine and self.diffusionRecombine
            else self.genomeSize
        )
        qc = QuantumCircuit(qubits, name="circuit")
        qc.compose(self.problem.state_preparation, inplace=True)
        qc.compose(self.problem.grover_operator.power(power), inplace=True)

        if shouldRecombine:
            qc.barrier(label="recombination")
            if self.diffusionRecombine:
                targets = self.compute_diffusions_bits(b=b_out)
                for i, t in enumerate(targets):
                    p = AmplificationProblem(
                        oracle=Statevector.from_label("00" if t == 0 else "11"),
                        is_good_state=["00" if t == 0 else "11"],
                        objective_qubits=[i, i + self.genomeSize],
                    )
                    qc.h(i + self.genomeSize)
                    qc.compose(
                        p.grover_operator.power(2),
                        qubits=p.objective_qubits,
                        inplace=True,
                    )
                # Insert mutation
                if self.mutateFactor is not None:
                    qc.barrier(label="mutation")
                    for i in range(self.genomeSize):
                        qc.rx(
                            random.uniform(
                                -math.pi * self.mutateFactor,
                                math.pi * self.mutateFactor,
                            ),
                            i,
                        )
            else:
                angles = [0] * self.genomeSize
                if len(b_out) >= self.kOut:
                    angles = [sum(x) for x in zip(angles, self.calculate_angles(b_out))]
                    if self.verbosity >= 1:
                        print("b_out array " + str(b_out))
                        print("applying b_out angles " + str(angles))

                for a in range(len(angles)):
                    if angles[a] != 0:
                        qc.ry(angles[a], a)

        measurement_cr = ClassicalRegister(self.genomeSize)
        qc.add_register(measurement_cr)
        m = [i for i in range(self.genomeSize)]
        qc.measure(m, reversed(m))
        # qc.measure(problem.objective_qubits, measurement_cr)
        return [qc, shouldRecombine]

    def _getGamma(self, id: str) -> Callable[[float, int], float]:
        if id == "poly":
            return polyGamma
        if id == "gaussian":
            return gaussianGamma
        return identityGamma
