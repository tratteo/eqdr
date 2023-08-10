import sys

from src.experiment import execute_eqiro_experiment


def knapsack(id: str):
    execute_eqiro_experiment(
        id,
        [
            {
                "name": "not_recombined",
                "config": {
                    "size": 7,
                    "maximize": True,
                    "iterations": 50,
                    "fitness": {
                        "function": "binary_knapsack",
                        "threshold": 0,
                        "target": 107,
                        "prices": [70, 20, 39, 37, 7, 5, 10],
                        "weights": [31, 10, 20, 19, 4, 3, 6],
                        "max_weight": 50,
                    },
                    "oracle": {
                        "operator": "pattern",
                        "expression": "***1**1",
                    },
                    "gamma": {
                        "function": "poly",
                        "alpha": 0.65,
                    },
                    "recombination": {
                        "k_out": 7,
                        "prob": 0.8,
                        "increased_prob": 0.8,
                        "enabled": False,
                        "mutate_factor": 1 / 12,
                    },
                },
            },
            {
                "name": "diffusion_recombined_poly",
                "config": {
                    "size": 7,
                    "maximize": True,
                    "iterations": 50,
                    "fitness": {
                        "function": "binary_knapsack",
                        "threshold": 0,
                        "target": 107,
                        "prices": [70, 20, 39, 37, 7, 5, 10],
                        "weights": [31, 10, 20, 19, 4, 3, 6],
                        "max_weight": 50,
                    },
                    "oracle": {
                        "operator": "pattern",
                        "expression": "1*1*0",
                    },
                    "gamma": {
                        "function": "poly",
                        "alpha": 0.7,
                    },
                    "recombination": {
                        "k_out": 7,
                        "prob": 0.1,
                        "increased_prob": 0.75,
                        "enabled": True,
                        "mutate_factor": 1 / 10,
                    },
                },
            },
        ],
    )


def square(id: str):
    execute_eqiro_experiment(
        id,
        [
            {
                "name": "not_recombined",
                "config": {
                    "size": 6,
                    "iterations": 50,
                    "fitness": {
                        "function": "square",
                        "threshold": 0.01,
                        "target": 0,
                    },
                    "oracle": {
                        "operator": "pattern",
                        "expression": "**1*0",
                    },
                    "recombination": {
                        "enabled": False,
                    },
                },
            },
            {
                "name": "diffusion_recombined_poly",
                "config": {
                    "size": 6,
                    "iterations": 50,
                    "fitness": {
                        "function": "square",
                        "threshold": 0.01,
                        "target": 0,
                    },
                    "oracle": {
                        "operator": "pattern",
                        "expression": "**1*0",
                    },
                    "gamma": {
                        "function": "poly",
                        "alpha": 0.8,
                    },
                    "recombination": {
                        "k_out": 10,
                        "prob": 0.85,
                        "increased_prob": 0.85,
                        "enabled": True,
                        "uniform": False,
                        "mutate_prob": 0.75,
                        "mutate_factor": 0.075,
                    },
                },
            },
        ],
    )


if __name__ == "__main__":
    processes = []
    arguments = sys.argv.copy()

    arguments.pop(0)
    if len(arguments) < 1:
        exit(1)
    name = arguments[0]
    square(name)
