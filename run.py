import sys
from src.experiment import execute_eqdr_experiment


iterations = 100


def knapsack(id: str):
    size = 7
    fitness = {
        "function": "binary_knapsack",
        "threshold": 0,
        "target": 107,
        "prices": [70, 20, 39, 37, 7, 5, 10],
        "weights": [31, 10, 20, 19, 4, 3, 6],
        "max_weight": 50,
    }
    oracle = {
        "operator": "pattern",
        "expression": "1****00",
    }
    lmbd = 1.2
    execute_eqdr_experiment(
        id,
        [
            {
                "name": "rcd",
                "config": {
                    "size": size,
                    "maximize": True,
                    "lambda": lmbd,
                    "iterations": iterations,
                    "fitness": fitness,
                    "oracle": oracle,
                    "recombination": {
                        "k_out": 12,
                        "prob": 0.8,
                        "enabled": True,
                        "type": "contribution",
                        "gamma": {
                            "function": "poly",
                            "alpha": 0.7,
                        },
                        "mutate_prob": 0.3,
                        "mutate_factor": 0.15,
                    },
                },
            },
            {
                "name": "spd",
                "config": {
                    "size": size,
                    "maximize": True,
                    "lambda": lmbd,
                    "iterations": iterations,
                    "fitness": fitness,
                    "oracle": oracle,
                    "recombination": {
                        "k_out": 12,
                        "prob": 0.8,
                        "enabled": True,
                        "type": "proportional",
                        "uniform_accuracy": 0.25,
                        "mutate_prob": 0.3,
                        "mutate_factor": 0.15,
                    },
                },
            },
            {
                "name": "ud",
                "config": {
                    "size": size,
                    "maximize": True,
                    "lambda": lmbd,
                    "iterations": iterations,
                    "fitness": fitness,
                    "oracle": oracle,
                    "recombination": {
                        "k_out": 12,
                        "prob": 0.8,
                        "enabled": True,
                        "type": "uniform",
                        "uniform_accuracy": 0.25,
                        "mutate_prob": 0.3,
                        "mutate_factor": 0.15,
                    },
                },
            },
        ],
    )


def rastrigin(id: str):
    size = 8
    fitness = {
        "function": "rastrigin",
        "threshold": 1e-3,
        "target": 0,
    }
    oracle = {
        "operator": "pattern",
        "expression": "**001000",
    }
    lmbd = 1.2
    execute_eqdr_experiment(
        id,
        [
            {
                "name": "eqdr_rcd",
                "config": {
                    "size": size,
                    "lambda": lmbd,
                    "iterations": iterations,
                    "fitness": fitness,
                    "oracle": oracle,
                    "recombination": {
                        "enabled": True,
                        "k_out": 12,
                        "prob": 0.6,
                        "gamma": {
                            "function": "gaussian",
                            "alpha": 0.5,
                        },
                        "type": "contribution",
                        "mutate_prob": 0.3,
                        "mutate_factor": 0.2,
                    },
                },
            },
            {
                "name": "eqdr_spd",
                "config": {
                    "size": size,
                    "lambda": lmbd,
                    "iterations": iterations,
                    "fitness": fitness,
                    "oracle": oracle,
                    "recombination": {
                        "k_out": 12,
                        "prob": 0.6,
                        "type": "proportional",
                        "uniform_accuracy": 0.75,
                        "enabled": True,
                        "mutate_prob": 0.3,
                        "mutate_factor": 0.2,
                    },
                },
            },
            {
                "name": "eqdr_ud",
                "config": {
                    "size": size,
                    "lambda": lmbd,
                    "iterations": iterations,
                    "fitness": fitness,
                    "oracle": oracle,
                    "recombination": {
                        "k_out": 12,
                        "prob": 0.6,
                        "uniform_accuracy": 0.75,
                        "type": "uniform",
                        "enabled": True,
                        "mutate_prob": 0.3,
                        "mutate_factor": 0.2,
                    },
                },
            },
        ],
    )


if __name__ == "__main__":
    arguments = sys.argv.copy()
    arguments.pop(0)
    if len(arguments) < 1:
        exit(1)
    name = arguments[0]

    # Run Rastrigin experiment with the provided name
    rastrigin(name)

    # Run Knapsack experiment with the provided name
    knapsack(name)
