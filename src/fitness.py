import math
from typing import Callable


def sin_fitness(genome: str, size: int) -> float:
    val = int(genome, 2)
    k = 1.5
    return math.sin(k * val) / math.exp(0.1 * val)


def square_fitness(genome: str, size: int) -> float:
    val = int(genome, 2) - size
    return val * val


def targets_fitness_factory(targets: list[str]) -> Callable[[str, int], float]:
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


def fitness_factory(fitnessId: str, **kwargs):
    if fitnessId.lower() == "sin":
        return sin_fitness
    elif fitnessId.lower() == "targets":
        return targets_fitness_factory(kwargs["targets"])
    elif fitnessId.lower() == "square":
        return square_fitness
