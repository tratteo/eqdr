import sys

from src.experiment import execute_eqiro_experiment


iterations = 100


def knapsack_7(id: str):
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
        "expression": "1*0*0*1",
    }
    lmbd = 1.2
    execute_eqiro_experiment(
        id,
        [
            # {
            #     "name": "not_recombined",
            #     "config": {
            #         "size": size,
            #         "maximize": True,
            #         "lambda": lmbd,
            #         "iterations": iterations,
            #         "fitness": fitness,
            #         "oracle": oracle,
            #         "recombination": {
            #             "enabled": False,
            #         },
            #     },
            # },
            # {
            #     "name": "diffusion_ud",
            #     "config": {
            #         "size": size,
            #         "maximize": True,
            #         "lambda": lmbd,
            #         "iterations": iterations,
            #         "fitness": fitness,
            #         "oracle": oracle,
            #         "recombination": {
            #             "k_out": size,
            #             "prob": 0.8,
            #             "enabled": True,
            #             "type": "uniform",
            #             "uniform_accuracy": 0.35,
            #             "mutate_prob": 0.75,
            #             "mutate_factor": 0.15,
            #         },
            #     },
            # },
            # {
            #     "name": "diffusion_spd",
            #     "config": {
            #         "size": size,
            #         "maximize": True,
            #         "lambda": lmbd,
            #         "iterations": iterations,
            #         "fitness": fitness,
            #         "oracle": oracle,
            #         "recombination": {
            #             "k_out": size,
            #             "prob": 0.8,
            #             "enabled": True,
            #             "type": "proportional",
            #             "uniform_accuracy": 0.35,
            #             "mutate_prob": 0.75,
            #             "mutate_factor": 0.15,
            #         },
            #     },
            # },
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
                        "k_out": 14,
                        "prob": 0.8,
                        "enabled": True,
                        "type": "contribution",
                        "gamma": {
                            "function": "gaussian",
                            "alpha": 0.15,
                        },
                        "mutate_prob": 0.4,
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
                        "k_out": 7,
                        "prob": 0.8,
                        "enabled": True,
                        "type": "proportional",
                        "uniform_accuracy": 0.5,
                        "mutate_prob": 0.4,
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
                        "k_out": 7,
                        "prob": 0.8,
                        "enabled": True,
                        "type": "uniform",
                        "uniform_accuracy": 0.5,
                        "mutate_prob": 0.4,
                        "mutate_factor": 0.15,
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
                    "iterations": iterations,
                    "fitness": {
                        "function": "square",
                        "threshold": 0.01,
                        "target": 0,
                    },
                    "oracle": {
                        "operator": "pattern",
                        "expression": "*****000",
                    },
                    "recombination": {
                        "k_out": 14,
                        "prob": 0.75,
                        "enabled": True,
                        "gamma": {
                            "function": "gaussian",
                            "alpha": 0.1,
                        },
                        "type": "contribution",
                        "mutate_prob": 0.25,
                        "mutate_factor": 0.125,
                    },
                },
            },
            {
                "name": "square_uniform",
                "config": {
                    "size": 8,
                    "iterations": iterations,
                    "fitness": {
                        "function": "square",
                        "threshold": 0.01,
                        "target": 0,
                    },
                    "oracle": {
                        "operator": "pattern",
                        "expression": "*****000",
                    },
                    "recombination": {
                        "k_out": 4,
                        "prob": 0.75,
                        "type": "uniform",
                        "enabled": True,
                        "uniform_accuracy": 0.75,
                        "mutate_prob": 0.25,
                        "mutate_factor": 0.125,
                    },
                },
            },
            {
                "name": "square_proportional",
                "config": {
                    "size": 8,
                    "iterations": iterations,
                    "fitness": {
                        "function": "square",
                        "threshold": 0.01,
                        "target": 0,
                    },
                    "oracle": {
                        "operator": "pattern",
                        "expression": "*****000",
                    },
                    "recombination": {
                        "k_out": 4,
                        "prob": 0.75,
                        "type": "proportional",
                        "enabled": True,
                        "uniform_accuracy": 0.75,
                        "mutate_prob": 0.25,
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
    execute_eqiro_experiment(
        id,
        [
            {
                "name": "bbht",
                "config": {
                    "size": size,
                    "lambda": lmbd,
                    "iterations": iterations,
                    "fitness": fitness,
                    "oracle": oracle,
                    "recombination": {
                        "enabled": False,
                    },
                },
            },
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
                        "k_out": int(size * 1.5),
                        "prob": 0.6,
                        "gamma": {
                            "function": "gaussian",
                            "alpha": 0.2,
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
                        "k_out": size,
                        "prob": 0.6,
                        "type": "proportional",
                        "uniform_accuracy": 0.75,
                        "enabled": True,
                        "mutate_prob": 0.3,
                        "mutate_factor": 0.15,
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
                        "k_out": size,
                        "prob": 0.6,
                        "uniform_accuracy": 0.75,
                        "type": "uniform",
                        "enabled": True,
                        "mutate_prob": 0.3,
                        "mutate_factor": 0.15,
                    },
                },
            },
        ],
    )
    return
    oracle = {
        "operator": "pattern",
        "expression": "**001000",
    }
    execute_eqiro_experiment(
        id + "_high_precision",
        [
            {
                "name": "bbht",
                "config": {
                    "size": size,
                    "lambda": lmbd,
                    "iterations": iterations,
                    "fitness": fitness,
                    "oracle": oracle,
                    "recombination": {
                        "enabled": False,
                    },
                },
            },
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
                            "alpha": 0.2,
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
                        "k_out": 8,
                        "prob": 0.6,
                        "type": "proportional",
                        "uniform_accuracy": 0.75,
                        "enabled": True,
                        "mutate_prob": 0.3,
                        "mutate_factor": 0.15,
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
                        "k_out": 6,
                        "prob": 0.6,
                        "uniform_accuracy": 0.75,
                        "type": "uniform",
                        "enabled": True,
                        "mutate_prob": 0.3,
                        "mutate_factor": 0.15,
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
    knapsack_7(name)
    # square_recombination(name)
    # print("-" * 100)
    # multimodal_recombination(name)
    # alpha(name)
    # rastrigin(name)
