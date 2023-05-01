from typing import Callable
from qiskit import QuantumCircuit
from random import choice
import random
from gamma import gaussianGamma, identityGamma, polyGamma


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
        oracleFactory: Callable[[str, float], QuantumCircuit],
        fitnessFunction: Callable[[str], float],
        genomeSize: int,
        **kwargs
    ) -> None:
        self._oracleFactory = oracleFactory
        self._fitnessFunction = fitnessFunction
        self._weightingGamma = kwargs.get("gamma", "identity")
        self._genomeSize = genomeSize
        self._generations = kwargs.get("generations", 16)
        self._hoyerIterations = kwargs.get("n_h", 2)

    def _generate_binary_string(self, n):
        return "".join(choice("01") for _ in range(n))

    def optimize(self) -> EqiroResult:
        b_out = []
        individuals = []
        for i in range(self._generations):
            solution = self._amplify(b_out=b_out)
            b_out.append(solution)
            individuals.append(solution)

        return EqiroResult(solutions=individuals)

    def _amplify(self, b_out: list[tuple[str, float]]) -> tuple[str, float]:
        y = self._generate_binary_string(self._genomeSize)
        fy = self._fitnessFunction(y)
        oracle = self._oracleFactory(y, fy)
        for m in range(self._hoyerIterations):
            # TODO
            # * DH(oracle, y, fy, b_out)
            # Run modified Durr-Hoyer and retrieve the measured individual and also all measured kets with relative fitness functions
            y1 = ""  # <- TODO
            fy1 = self._fitnessFunction(y1)
            if fy1 < fy:
                y = y1
                oracle = self._oracleFactory(y1, fy1)
        return [y, fy]

    def _getGamma(self, id: str) -> Callable[[float, int], float]:
        if id == "poly":
            return polyGamma
        if id == "gaussian":
            return gaussianGamma
        return identityGamma
