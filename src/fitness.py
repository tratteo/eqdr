import math
from typing import Callable


def sin_fitness(genome: str, size: int) -> float:
    val = int(genome, 2)
    k = 1.5
    return math.sin(k * val) / math.exp(0.1 * val)


def multimodal_fitness(genome: str, size: int) -> float:
    val = int(genome, 2)
    k = size
    numerator = k * math.tanh(((val - k) ** 2) / (2**k))
    denominator = math.cos(k * (val - k)) + 2
    return numerator / denominator


def binary_knapsack_fitness_factory(
    weights: "list[float]", max_weight: float, prices: "list[float]"
):
    def binary_knapsack_fitness(
        genome: str,
        size: int,
    ) -> float:
        w = 0
        p = 0
        f = 0
        for i, b in enumerate(genome):
            p += int(b) * prices[i]
            w += int(b) * weights[i]

        if w > max_weight:
            f = 0
        else:
            f = p
        # print(genome + ": " + str(max_weight) + ", " + str(w) + ", f: " + str(f))
        return f

    return binary_knapsack_fitness


def square_fitness(genome: str, size: int) -> float:
    val = int(genome, 2) - size
    return val * val


def targets_fitness_factory(targets: "list[str]") -> Callable[[str, int], float]:
    def fitness_function(genome: str, size: int) -> float:
        min_dist = math.inf
        genome_val = int(genome, 2)
        for t in targets:
            v = int(t, 2)
            d = abs(genome_val - v)
            if d < min_dist:
                min_dist = d
        return min_dist

    return fitness_function


def fitness_factory(**kwargs):
    fitnessId = kwargs["function"].lower()
    if fitnessId == "sin":
        return sin_fitness
    elif fitnessId == "multimodal":
        return multimodal_fitness
    elif fitnessId == "targets":
        return targets_fitness_factory(kwargs["targets"])
    elif fitnessId == "square":
        return square_fitness
    elif fitnessId == "binary_knapsack":
        return binary_knapsack_fitness_factory(
            kwargs["weights"], kwargs["max_weight"], kwargs["prices"]
        )
