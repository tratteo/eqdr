import math
from typing import Callable, Union
from qiskit import QuantumCircuit, ClassicalRegister, execute
import random
from qiskit.quantum_info import Statevector
from qiskit import Aer
from src.eqdr.eqdr_result import EqdrResult
from src.gamma import gaussianGamma, identityGamma, polyGamma
from qiskit.algorithms import AmplificationProblem


class Eqdr:
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
        self.genomeSize = self.problem.oracle.num_qubits

        self.backend = Aer.get_backend("qasm_simulator") if backend is None else backend
        # self.backend.set_options(device="GPU")
        self.verbosity = kwargs.get("verbosity", 1)
        self.lmbd = kwargs.get("lambda", 1.2)
        self.maximize = kwargs.get("maximize", False)
        self.maxIter = kwargs.get("max_iterations", math.inf)

        self.recombinationProb = kwargs.get("recombination", {}).get("prob", 0.1)
        self.mutateFactor = kwargs.get("recombination", {}).get("mutate_factor", None)
        self.recombine = kwargs.get("recombination", {}).get("enabled", True)
        self.mutateProb = kwargs.get("recombination", {}).get("mutate_prob", 0.1)
        self.kOut = kwargs.get("recombination", {}).get("k_out", self.genomeSize // 2)
        self.uniformRecombine = kwargs.get("recombination", {}).get("uniform", False)
        self.increasedRecombinationProb = kwargs.get("recombination", {}).get(
            "increased_prob", 0.75
        )

        self.gamma = self._getGamma(kwargs.get("gamma", {}).get("function", "poly"))
        self.gAlpha = kwargs.get("gamma", {}).get("alpha", 0.5)

        self.fitnessThreshold = kwargs.get("fitness", {}).get("threshold", None)
        self.targetFitness = kwargs.get("fitness", {}).get("target", None)

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

    def is_fitness_better(self, f1: float, f2: float) -> bool:
        if self.maximize:
            return f1 > f2
        else:
            return f1 < f2

    def optimize(self) -> EqdrResult:
        b_out: list[tuple[str, float]] = []
        solutions = []
        recombinations = 0
        iteration = 0
        fitnessCalls = 0
        recombinationIndex = 0
        increaseMutate = False
        m = 1
        while iteration < self.maxIter:
            qc, recombined = self.construct_circuit(
                power=random.randint(1, m),
                b_out=b_out,
                recombineProb=self.increasedRecombinationProb
                if increaseMutate
                else math.tanh(iteration / (self.genomeSize**2))
                * (self.recombinationProb),
            )
            if recombined:
                recombinations += 1 if recombined else 0
                increaseMutate = False

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
                if self.is_fitness_better(fitness, b_out[0][1]):
                    increaseMutate = True
                if len(b_out) > self.kOut:
                    b_out.sort(key=lambda x: x[1], reverse=self.maximize)
                    b_out.pop()
                # self.problem = AmplificationProblem(
                #     oracle=multi_targets_oracle([b[0] for b in b_out], self.genomeSize)
                # )

            solutions.append([measured, fitness])
            solutions.sort(key=lambda x: x[1], reverse=self.maximize)
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

        solutions.sort(key=lambda x: x[1], reverse=self.maximize)
        return EqdrResult(
            solutions=solutions,
            statistics={
                "iterations": iteration,
                "recombinations": recombinations,
                "fitness_calls": fitnessCalls,
            },
        )

    def compute_diffusions_bits(
        self, b: "list[tuple[str, float]]"
    ) -> "tuple[list[str], list[float]]":
        bits = [0] * self.genomeSize
        b.sort(key=lambda x: x[1])
        for i in range(self.genomeSize):
            gc = []
            if self.uniformRecombine:
                rand_index = random.randint(0, len(b) - 1)
                current = b[rand_index]
                bits[i] += -1 if current[0][i] == "0" else 1
            else:
                max_gamma = 0
                for k in range(len(b)):
                    current = b[k]
                    g = self.gamma(
                        current[1],
                        k,
                        a=self.gAlpha,
                        k=len(b),
                    )
                    gc.append(g)
                    bits[i] += (-1 if current[0][i] == "0" else 1) * g
        res = ["0" if a < 0 else "1" for a in bits]
        max_gamma = sum(gc)
        acc = [abs(a) for a in bits]
        acc = [a / max_gamma for a in acc]
        if self.verbosity > 1:
            print("\n", flush=True)
            print("gamma > " + str(gc), flush=True)
            print("b > " + str(b), flush=True)
            print("contributions > " + str(bits), flush=True)
            print("res > " + str(res), flush=True)
        return res, acc

    def construct_circuit(
        self,
        power: int,
        b_out: "list[tuple[str, float]]",
        recombineProb: float,
    ) -> "tuple[QuantumCircuit, bool]":
        shouldRecombine = (
            self.recombine
            and len(b_out) >= self.kOut
            and random.random() < recombineProb
        )

        qubits = self.genomeSize * 2 if shouldRecombine else self.genomeSize
        qc = QuantumCircuit(qubits, name="circuit")
        qc.barrier(label="Grover")
        qc.compose(self.problem.state_preparation, inplace=True)
        qc.compose(self.problem.grover_operator.power(power), inplace=True)
        # qc.decompose(reps=2, gates_to_decompose=["Q"]).draw(
        #     filename="eqdr1.png",
        #     output="mpl",
        #     plot_barriers=False,
        #     vertical_compression="medium",
        # )
        if shouldRecombine:
            qc.barrier(label="Recombination")
            bits, acc = self.compute_diffusions_bits(b=b_out)
            # lab = "".join(bits)
            # p = AmplificationProblem(
            #     oracle=Statevector.from_label(lab),
            #     is_good_state=[lab],
            # )
            # qc.compose(
            #     p.grover_operator.power(math.sqrt(self.genomeSize)),
            #     qubits=p.objective_qubits,
            #     inplace=True,
            # )
            for i, t in enumerate(bits):
                if random.random() < acc[i]:
                    p = AmplificationProblem(
                        oracle=Statevector.from_label("00" if t == "0" else "11"),
                        is_good_state=["00" if t == "0" else "11"],
                        objective_qubits=[i, i + self.genomeSize],
                    )
                    qc.h(i + self.genomeSize)
                    qc.compose(
                        p.grover_operator.power(1),
                        qubits=p.objective_qubits,
                        inplace=True,
                    )
                    # p.grover_operator.power(1).decompose(reps=2).draw(
                    #     filename="eqdrdiff.png",
                    #     output="mpl",
                    #     vertical_compression="medium",
                    # )
        # Insert mutation
        if self.mutateFactor is not None:
            qc.barrier(label="Mutation")

            for i in range(self.genomeSize):
                if random.random() < self.mutateProb:
                    qc.ry(
                        random.uniform(
                            -math.pi * self.mutateFactor,
                            math.pi * self.mutateFactor,
                        ),
                        i,
                    )

        measurement_cr = ClassicalRegister(self.genomeSize)
        qc.add_register(measurement_cr)
        m = [i for i in range(self.genomeSize)]
        qc.measure(m, reversed(m))
        # qc.measure(problem.objective_qubits, measurement_cr)
        # qc.decompose(reps=2, gates_to_decompose=["Q"]).draw(
        #     filename="eqdrtot.png",
        #     fold=64,
        #     output="mpl",
        #     vertical_compression="medium",
        # )
        return [qc, shouldRecombine]

    def _getGamma(self, id: str) -> Callable[[float, int], float]:
        if id == "poly":
            return polyGamma
        if id == "gaussian":
            return gaussianGamma
        return identityGamma
