import math
from typing import Union
import random
from qiskit_aer import AerSimulator
from qiskit import ClassicalRegister, QuantumCircuit, transpile
from qiskit.primitives import Sampler
from qiskit.quantum_info import Statevector

from qiskit.algorithms import AmplificationProblem, AmplitudeAmplifier


class BBHTResult:
    def __init__(self, iterations: int, resultState: str):
        self.iterations = iterations
        self.resultState = resultState


class BBHT(AmplitudeAmplifier):
    def __init__(
        self, targets: list, oracle: Union[QuantumCircuit, Statevector]
    ) -> None:
        self._targets = targets
        self.geneticPool = []
        self._m = 1
        self._lambda = 4 / 3
        self.sim_bk = AerSimulator()
        self._problem = AmplificationProblem(oracle=oracle)

    def amplify(self) -> BBHTResult:
        count = 1
        while True:
            i = random.randint(1, self._m)
            power = i

            # Run a grover experiment for a given power of the Grover operator.
            qc = self.construct_circuit(self._problem, power, measurement=True)
            # print("running amplitude amplification, m: " + str(self._m))
            result = self.sim_bk.run(transpile(qc, self.sim_bk), shots=1).result()
            measured = list(result.get_counts().keys())[0]
            num_bits = len(self._problem.objective_qubits)
            self.geneticPool.append(measured)
            if measured in self._targets:
                return BBHTResult(iterations=count, resultState=measured)
            else:
                self._m = math.ceil(
                    min(
                        self._lambda * self._m,
                        math.sqrt(math.pow(2, num_bits)),
                    )
                )
            count += 1

        return ""

    def construct_circuit(
        self,
        problem: AmplificationProblem,
        power: int,
        measurement: bool = False,
    ) -> QuantumCircuit:
        qc = QuantumCircuit(problem.oracle.num_qubits, name="Grover circuit")
        qc.compose(problem.state_preparation, inplace=True)
        qc.compose(problem.grover_operator.power(power), inplace=True)
        if measurement:
            measurement_cr = ClassicalRegister(len(problem.objective_qubits))
            qc.add_register(measurement_cr)
            qc.measure(problem.objective_qubits, measurement_cr)

        return qc
