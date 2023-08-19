import sys

from src.experiment import execute_eqiro_experiment


iterations = 200


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
                        "expression": "1*0*0*1",
                    },
                    "recombination": {
                        "enabled": False,
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
                        "expression": "1*0*0*1",
                    },
                    # "gamma": {
                    #     "function": "gaussian",
                    #     "alpha": 0.2,
                    # },
                    "recombination": {
                        "k_out": 7,
                        "prob": 0.65,
                        "enabled": True,
                        "type": "uniform",
                        "args": {"uniform_accuracy": 0.45},
                        "mutate_prob": 0.225,
                        "mutate_factor": 0.2,
                    },
                },
            },
        ],
    )


def square_recombination(id: str):
    execute_eqiro_experiment(
        id,
        [
            {
                "name": "square_contribution",
                "config": {
                    "size": 8,
                    "iterations": 50,
                    "fitness": {
                        "function": "square",
                        "threshold": 0.01,
                        "target": 0,
                    },
                    "oracle": {
                        "operator": "pattern",
                        "expression": "***01***",
                    },
                    "recombination": {
                        "k_out": 14,
                        "prob": 0.65,
                        "enabled": True,
                        "gamma": {
                            "function": "gaussian",
                            "alpha": 0.175,
                        },
                        "type": "contribution",
                        "mutate_prob": 0.5,
                        "mutate_factor": 0.125,
                    },
                },
            },
            {
                "name": "square_uniform",
                "config": {
                    "size": 8,
                    "iterations": 50,
                    "fitness": {
                        "function": "square",
                        "threshold": 0.01,
                        "target": 0,
                    },
                    "oracle": {
                        "operator": "pattern",
                        "expression": "***01***",
                    },
                    "recombination": {
                        "k_out": 14,
                        "prob": 0.65,
                        "type": "uniform",
                        "enabled": True,
                        "uniform_accuracy": 0.5,
                        "mutate_prob": 0.5,
                        "mutate_factor": 0.125,
                    },
                },
            },
            {
                "name": "square_proportional",
                "config": {
                    "size": 8,
                    "iterations": 50,
                    "fitness": {
                        "function": "square",
                        "threshold": 0.01,
                        "target": 0,
                    },
                    "oracle": {
                        "operator": "pattern",
                        "expression": "***01***",
                    },
                    "recombination": {
                        "k_out": 14,
                        "prob": 0.65,
                        "type": "proportional",
                        "enabled": True,
                        "uniform_accuracy": 0.5,
                        "mutate_prob": 0.5,
                        "mutate_factor": 0.125,
                    },
                },
            },
        ],
    )


def multimodal_recombination(id: str):
    execute_eqiro_experiment(
        id,
        [
            {
                "name": "multimodal_contribution",
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
                        "expression": "1*0*0*1",
                    },
                    "recombination": {
                        "k_out": 7,
                        "gamma": {
                            "function": "gaussian",
                            "alpha": 0.15,
                        },
                        "prob": 0.65,
                        "enabled": True,
                        "type": "contribution",
                        "mutate_prob": 0.5,
                        "mutate_factor": 0.125,
                    },
                },
            },
            {
                "name": "multimodal_uniform",
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
                        "expression": "1*0*0*1",
                    },
                    "recombination": {
                        "k_out": 7,
                        "prob": 0.65,
                        "enabled": True,
                        "type": "uniform",
                        "uniform_accuracy": 0.5,
                        "mutate_prob": 0.5,
                        "mutate_factor": 0.125,
                    },
                },
            },
            {
                "name": "multimodal_proportional",
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
                        "expression": "1*0*0*1",
                    },
                    "recombination": {
                        "k_out": 7,
                        "prob": 0.65,
                        "enabled": True,
                        "type": "proportional",
                        "uniform_accuracy": 0.5,
                        "mutate_prob": 0.5,
                        "mutate_factor": 0.125,
                    },
                },
            },
        ],
    )


def parameters_variations(id: str):
    execute_eqiro_experiment(
        id,
        [
            {
                "name": "high_mutation",
                "lambda": 1.2,
                "config": {
                    "size": 8,
                    "iterations": iterations,
                    "fitness": {
                        "function": "multimodal",
                        "threshold": 1e-3,
                        "target": 0,
                    },
                    "oracle": {
                        "operator": "pattern",
                        "expression": "*****000",
                    },
                    "recombination": {
                        "k_out": 14,
                        "prob": 0.4,
                        "type": "contribution",
                        "enabled": True,
                        "mutate_prob": 0.75,
                        "mutate_factor": 0.125,
                    },
                },
            },
            {
                "name": "low_mutation",
                "lambda": 1.2,
                "config": {
                    "size": 8,
                    "iterations": iterations,
                    "fitness": {
                        "function": "multimodal",
                        "threshold": 1e-3,
                        "target": 0,
                    },
                    "oracle": {
                        "operator": "pattern",
                        "expression": "*****000",
                    },
                    "recombination": {
                        "k_out": 14,
                        "prob": 0.4,
                        "gamma": {
                            "function": "gaussian",
                            "alpha": 0.1,
                        },
                        "type": "contribution",
                        "enabled": True,
                        "mutate_prob": 0.15,
                        "mutate_factor": 0.125,
                    },
                },
            },
            {
                "name": "high_recombination",
                "lambda": 1.2,
                "config": {
                    "size": 8,
                    "iterations": iterations,
                    "fitness": {
                        "function": "multimodal",
                        "threshold": 1e-3,
                        "target": 0,
                    },
                    "oracle": {
                        "operator": "pattern",
                        "expression": "00**1000",
                    },
                    "recombination": {
                        "k_out": 14,
                        "prob": 0.85,
                        "type": "contribution",
                        "enabled": True,
                        "mutate_prob": 0.5,
                        "mutate_factor": 0.125,
                    },
                },
            },
            {
                "name": "low_recombination",
                "lambda": 1.2,
                "config": {
                    "size": 8,
                    "iterations": iterations,
                    "fitness": {
                        "function": "multimodal",
                        "threshold": 1e-3,
                        "target": 0,
                    },
                    "oracle": {
                        "operator": "pattern",
                        "expression": "00**1000",
                    },
                    "recombination": {
                        "k_out": 14,
                        "prob": 0.15,
                        "gamma": {
                            "function": "gaussian",
                            "alpha": 0.175,
                        },
                        "type": "contribution",
                        "enabled": True,
                        "mutate_prob": 0.5,
                        "mutate_factor": 0.125,
                    },
                },
            },
            {
                "name": "high_kout",
                "lambda": 1.2,
                "config": {
                    "size": 8,
                    "iterations": iterations,
                    "fitness": {
                        "function": "multimodal",
                        "threshold": 1e-3,
                        "target": 0,
                    },
                    "oracle": {
                        "operator": "pattern",
                        "expression": "00**1000",
                    },
                    "recombination": {
                        "k_out": 24,
                        "prob": 0.4,
                        "gamma": {
                            "function": "gaussian",
                            "alpha": 0.175,
                        },
                        "type": "contribution",
                        "enabled": True,
                        "mutate_prob": 0.5,
                        "mutate_factor": 0.125,
                    },
                },
            },
            {
                "name": "low_kout",
                "lambda": 1.2,
                "config": {
                    "size": 8,
                    "iterations": iterations,
                    "fitness": {
                        "function": "multimodal",
                        "threshold": 1e-3,
                        "target": 0,
                    },
                    "oracle": {
                        "operator": "pattern",
                        "expression": "00**1000",
                    },
                    "recombination": {
                        "k_out": 4,
                        "prob": 0.4,
                        "gamma": {
                            "function": "gaussian",
                            "alpha": 0.175,
                        },
                        "type": "contribution",
                        "enabled": True,
                        "mutate_prob": 0.5,
                        "mutate_factor": 0.125,
                    },
                },
            },
        ],
    )


def multimodal(id: str):
    execute_eqiro_experiment(
        id,
        [
            {
                "name": "not_recombined",
                "lambda": 1.2,
                "config": {
                    "size": 8,
                    "iterations": iterations,
                    "fitness": {
                        "function": "multimodal",
                        "threshold": 1e-3,
                        "target": 0,
                    },
                    "oracle": {
                        "operator": "pattern",
                        "expression": "****10**",
                    },
                    "recombination": {
                        "enabled": False,
                    },
                },
            },
            {
                "name": "recombined",
                "lambda": 1.2,
                "config": {
                    "size": 8,
                    "iterations": iterations,
                    "fitness": {
                        "function": "multimodal",
                        "threshold": 1e-3,
                        "target": 0,
                    },
                    "oracle": {
                        "operator": "pattern",
                        "expression": "****10**",
                    },
                    "recombination": {
                        "k_out": 16,
                        "prob": 0.55,
                        "gamma": {
                            "function": "gaussian",
                            "alpha": 0.175,
                        },
                        "type": "contribution",
                        "enabled": True,
                        "mutate_prob": 0.3,
                        "mutate_factor": 0.125,
                    },
                },
            },
            # {
            #     "name": "not_recombined_betteroracle",
            #     "lambda": 1.2,
            #     "config": {
            #         "size": 8,
            #         "iterations": iterations,
            #         "fitness": {
            #             "function": "multimodal",
            #             "threshold": 1e-3,
            #             "target": 0,
            #         },
            #         "oracle": {
            #             "operator": "pattern",
            #             "expression": "00**1000",
            #         },
            #         "recombination": {
            #             "enabled": False,
            #         },
            #     },
            # },
            # {
            #     "name": "recombined_betteroracle",
            #     "lambda": 1.2,
            #     "config": {
            #         "size": 8,
            #         "iterations": iterations,
            #         "fitness": {
            #             "function": "multimodal",
            #             "threshold": 1e-3,
            #             "target": 0,
            #         },
            #         "oracle": {
            #             "operator": "pattern",
            #             "expression": "00**1000",
            #         },
            #         "gamma": {
            #             "function": "gaussian",
            #             "alpha": 0.175,
            #         },
            #         "recombination": {
            #             "k_out": 8,
            #             "prob": 0.5,
            #             "enabled": True,
            #             "type": "contribution",
            #             "args": {"uniform_accuracy": 0.75},
            #             "mutate_prob": 0.25,
            #             "mutate_factor": 0.175,
            #         },
            #     },
            # },
        ],
    )


if __name__ == "__main__":
    processes = []
    arguments = sys.argv.copy()

    arguments.pop(0)
    if len(arguments) < 1:
        exit(1)
    name = arguments[0]
    # knapsack(name)
    square_recombination(name)
    print("-" * 100)
    multimodal_recombination(name)
