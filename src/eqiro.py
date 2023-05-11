import math
from typing import Callable, Union
from qiskit import QuantumCircuit, ClassicalRegister, transpile
import random
import numpy as np
from qiskit.quantum_info import Statevector
from qiskit_aer import AerSimulator
from gamma import gaussianGamma, identityGamma, polyGamma
from qiskit.algorithms import AmplificationProblem


class EqiroResult:
    def __init__(
        self,
        solutions: "list[tuple[str, float]]",
        statistics: any,
    ) -> None:
        self.solutions: list[tuple[str, float]] = solutions
        self.statistics = statistics


class Eqiro:
    """
    * `oracleFactory`: function that given a solution and its fitness `(y, fy)`, constructs an oracle that is able to invert the amplitudes of all states `y1` such that `fy1 < fy`
    * `fitnessFunction`: classical implementation of the target fitness function
    * `genomeSize`: the size of the genome, that is the number of qubits used
    """

    def __init__(
        self,
        oracle: Union[QuantumCircuit, Statevector],
        fitnessFunction: Callable[[str, int], float],
        genomeSize: int,
        is_good_state=Callable[[str], bool],
        **kwargs,
    ) -> None:
        self._problem = AmplificationProblem(oracle=oracle)
        self._fitnessFunction = fitnessFunction
        self._aerSim = AerSimulator()
        self._is_good_state = is_good_state
        self._verbosity = kwargs.get("verbosity", 1)
        self._gamma = self._getGamma(kwargs.get("gamma", "identity"))
        self._lambda = kwargs.get("lambda", 4 / 3)
        self._genomeSize = genomeSize
        self._gamma_mul = kwargs.get("gamma_mul", 1)
        self._recombination_module = kwargs.get("recombination_module", 1)
        self._max_iter = kwargs.get("max_iterations", math.inf)
        self._recombine = kwargs.get("enable_recombination", True)
        self._k_out = kwargs.get("k_out", 4)
        self._g_alpha = kwargs.get("g_alpha", 0.5)

    def _generate_binary_string(self, n):
        return "".join(random.choice("01") for _ in range(n))

    def optimize(self) -> EqiroResult:
        b_out: list[tuple[str, float]] = []
        solutions = []
        recombinations = 0
        count = 0
        m = 1
        while count < self._max_iter:
            power = random.randint(1, m)

            should_recombine = (
                self._recombine
                and len(b_out) >= self._k_out
                and (count - self._k_out) % self._recombination_module == 0
            )
            recombinations += 1 if should_recombine else 0

            # Run a grover experiment for a given power of the Grover operator.
            qc = self.construct_circuit(
                self._problem,
                power,
                b_out=b_out,
                should_recombine=should_recombine,
                measurement=True,
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
            fitness = self._fitnessFunction(measured, self._genomeSize)

            if self._verbosity > 0:
                print("\niteration " + str(count))
                print("measured " + str(measured))
                print("fitness " + str(fitness))

            b_out.append([measured, fitness])
            if len(b_out) > self._k_out:
                b_out.sort(key=lambda x: x[1])
                b_out.pop()

            solutions.append([measured, fitness])
            solutions.sort(key=lambda x: x[1])
            if len(solutions) > 10:
                solutions.pop()

            count += 1
            if self._is_good_state is not None and self._is_good_state(measured):
                break

            m = math.ceil(
                min(
                    self._lambda * m,
                    math.sqrt(math.pow(2, len(self._problem.objective_qubits))),
                )
            )

        solutions.sort(key=lambda x: x[1])
        return EqiroResult(
            solutions=solutions,
            statistics={"iterations": count, "recombinations": recombinations},
        )

    def calculate_angles(self, b: "list[tuple[str, float]]") -> "list[float]":
        angles = [0] * self._genomeSize
        c = math.pi / len(b)
        b.sort(key=lambda x: x[1])
        for i in range(self._genomeSize):
            theta = 0
            for k in range(len(b)):
                current = b[k][0]
                gamma = self._gamma(
                    self._fitnessFunction(current, self._genomeSize),
                    k,
                    a=self._g_alpha,
                    k=len(b),
                )
                if self._verbosity > 1:
                    print("computed gamma " + str(gamma))
                theta += int(current[i]) * gamma * self._gamma_mul
            angles[i] = theta * c
        return angles

    def construct_circuit(
        self,
        problem: AmplificationProblem,
        power: int,
        b_out: "list[tuple[str, float]]",
        should_recombine: bool,
        measurement: bool = False,
    ) -> QuantumCircuit:
        qc = QuantumCircuit(problem.oracle.num_qubits, name="Grover circuit")
        qc.compose(problem.state_preparation, inplace=True)
        qc.compose(problem.grover_operator.power(power), inplace=True)

        if should_recombine:
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

    def _getGamma(self, id: str) -> Callable[[float, int], float]:
        if id == "poly":
            return polyGamma
        if id == "gaussian":
            return gaussianGamma
        return identityGamma
