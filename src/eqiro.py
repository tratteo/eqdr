import math
from typing import Callable
from qiskit import QuantumCircuit, ClassicalRegister, transpile
import random
import numpy as np
from qiskit.quantum_info import Statevector
from qiskit_aer import AerSimulator
from gamma import gaussianGamma, identityGamma, polyGamma
from qiskit.algorithms import AmplificationProblem


class EqiroResult:
    def __init__(self, solutions: list[tuple[str, float]]) -> None:
        self.solutions: list[tuple[str, float]] = solutions


class Eqiro:
    """
    * `oracleFactory`: function that given a solution and its fitness `(y, fy)`, constructs an oracle that is able to invert the amplitudes of all states `y1` such that `fy1 < fy`
    * `fitnessFunction`: classical implementation of the target fitness function
    * `genomeSize`: the size of the genome, that is the number of qubits used
    """

    def __init__(
        self,
        oracleFactory: Callable[[str, float], QuantumCircuit | Statevector],
        fitnessFunction: Callable[[str], float],
        genomeSize: int,
        **kwargs
    ) -> None:
        self._oracleFactory = oracleFactory
        self._fitnessFunction = fitnessFunction
        self._aerSim = AerSimulator()
        self._verbosity = kwargs.get("verbosity", 1)
        self._gamma = self._getGamma(kwargs.get("gamma", "identity"))
        self._lambda = kwargs.get("lambda", 4 / 3)
        self._genomeSize = genomeSize
        self._generations = kwargs.get("generations", 16)
        self._k_in = kwargs.get("k_in", 4)
        self._k_out = kwargs.get("k_out", 4)
        self._g_alpha = kwargs.get("g_alpha", 0.5)
        self._hoyerIterations = kwargs.get("n_h", 2)

    def _generate_binary_string(self, n):
        return "".join(random.choice("01") for _ in range(n))

    def optimize(self) -> EqiroResult:
        b_out: list[tuple[str, float]] = []
        generationsSolutions = []
        for g in range(self._generations):
            solution = self._amplify(b_out=b_out)
            if self._verbosity > 1:
                print("\ngeneration " + str(g))
                print("solution: " + str(solution))
            if len(b_out) >= self._k_out:
                b_out.sort(key=lambda x: x[1])
                b_out.pop()
            b_out.append(solution)
            generationsSolutions.append(solution)

        generationsSolutions.sort(key=lambda x: x[1])
        return EqiroResult(solutions=generationsSolutions)

    def calculate_angles(self, b: list[tuple[str, float]]) -> list[float]:
        angles = [0] * self._genomeSize
        c = math.pi / len(b)
        b.sort(key=lambda x: x[1])
        for i in range(self._genomeSize):
            theta = 0
            for k in range(len(b)):
                current = b[k][0]
                gamma = self._gamma(
                    self._fitnessFunction(current), k, a=self._g_alpha, k=len(b)
                )
                if self._verbosity > 1:
                    print("computed gamma " + str(gamma))
                theta += int(current[i]) * gamma
            angles[i] = theta * c
        return angles

    def construct_circuit(
        self,
        problem: AmplificationProblem,
        power: int,
        b_in: list[tuple[str, float]],
        b_out: list[tuple[str, float]],
        measurement: bool = False,
    ) -> QuantumCircuit:
        qc = QuantumCircuit(problem.oracle.num_qubits, name="Grover circuit")
        qc.compose(problem.state_preparation, inplace=True)
        qc.compose(problem.grover_operator.power(power), inplace=True)

        angles = [0] * self._genomeSize
        # if len(b_in) >= self._k_in:
        #     angles = [sum(x) for x in zip(angles, self.calculate_angles(b_in))]
        #     # print("b_in: " + str(b_in))
        #     # print("applying b_in angles " + str(angles))
        #     b_in.clear()

        if len(b_out) >= self._k_out:
            angles = [sum(x) for x in zip(angles, self.calculate_angles(b_out))]
            if self._verbosity >= 1:
                print("b_out array " + str(b_out))
                print("applying b_out angles " + str(angles))

        for a in range(len(angles)):
            if angles[a] != 0:
                qc.ry(angles[a], a)

        if measurement:
            measurement_cr = ClassicalRegister(len(problem.objective_qubits))
            qc.add_register(measurement_cr)
            qc.measure(problem.objective_qubits, measurement_cr)
        # qc.draw(output="mpl", filename="circuit.png")
        return qc

    def _amplify(self, b_out: list[tuple[str, float]]) -> tuple[str, float]:
        y = self._generate_binary_string(self._genomeSize)
        fy = self._fitnessFunction(y)
        oracle = self._oracleFactory(y, fy)
        problem = AmplificationProblem(oracle=oracle)
        m = 1
        for _ in range(self._hoyerIterations):
            b_in = []
            i = random.randint(1, m)
            power = i
            # Run a grover experiment for a given power of the Grover operator.
            qc = self.construct_circuit(
                problem, power, b_in=b_in, b_out=b_out, measurement=True
            )

            result = self._aerSim.run(transpile(qc, self._aerSim), shots=1).result()
            measured = list(result.get_counts().keys())[0]
            if self._verbosity > 1:
                print(
                    "amplitude amplification, m: "
                    + str(m)
                    + ", measured: "
                    + str(measured)
                )
            fitness = self._fitnessFunction(measured)
            b_in.append([measured, fitness])

            if fitness < fy:
                y = measured
                if self._verbosity >= 1:
                    print("better solution found: " + measured)
                fy = fitness
                oracle = self._oracleFactory(y, fy)
                problem = AmplificationProblem(oracle=oracle)
                break
            m = math.ceil(
                min(
                    self._lambda * m,
                    math.sqrt(math.pow(2, len(problem.objective_qubits))),
                )
            )

        return [y, fy]

    def _getGamma(self, id: str) -> Callable[[float, int], float]:
        if id == "poly":
            return polyGamma
        if id == "gaussian":
            return gaussianGamma
        return identityGamma
