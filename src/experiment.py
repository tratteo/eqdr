import json
from multiprocessing import Process
import os
import random

from src.utils import generate_binary_string
from src.eqiro import eqiro_run


def run_experiment(name: str):
    print("starting experiment " + name)
    if name == "angles":
        angles_experiment()
    if name == "gamma":
        gamma_experiment()
    if name == "fitness":
        fitness_experiment()
    if name == "targets":
        targets_experiment()


def execute_eqiro_experiment(name: str, config: any, workers: "list[any]"):
    root = os.path.join("results", name)
    if not os.path.exists(root):
        os.makedirs(root)

    # with open(os.path.join(root, "config.json"), "w") as outfile:
    #     outfile.write(json.dumps(config, indent="\t"))

    processes = []
    for i, k in enumerate(workers):
        c = json.loads(json.dumps(config))
        c["id"] = i
        c["report"] = os.path.join(root, k["name"] + ".csv")
        c = k["config_factory"](c, root)
        c["prefix"] = name + "_" + k["name"]
        with open(os.path.join(root, k["name"] + "_config.json"), "w") as outfile:
            outfile.write(json.dumps(c, indent="\t"))
        processes.append(Process(target=eqiro_run, args=[c]))

    for p in processes:
        p.start()
    for p in processes:
        p.join()

    print("experiment " + name + " completed")


def targets_experiment():
    config = {
        "size": 6,
        "k_out": 2,
        "g_alpha": 0.75,
        "gamma_mul": 0.15,
        "recombination_module": 6,
        "lambda": 1.2,
        "rescaled_angles": True,
        "oracle": "targets",
        "fitness_function": "targets",
        "gamma": "gaussian",
        "iterations": 50,
    }
    n = config["size"]
    targets = [generate_binary_string(n) for i in range(random.randint(1, n // 2))]
    config["targets"] = targets

    def config_factory(recombine: bool):
        def config(config, root):
            config["recombine"] = recombine
            return config

        return config

    execute_eqiro_experiment(
        "targets",
        config,
        [
            {"name": "recombined", "config_factory": config_factory(True)},
            {"name": "not_recombined", "config_factory": config_factory(False)},
        ],
    )


def gamma_experiment():
    config = {
        "size": 6,
        "k_out": 2,
        "g_alpha": 0.75,
        "gamma_mul": 0.15,
        "recombination_module": 8,
        "lambda": 1.2,
        "oracle": "odd",
        "fitness_function": "sin",
        "rescaled_angles": True,
        "target_fitness": -0.7,
        "fitness_threshold": 0.1,
        "recombine": True,
        "iterations": 50,
    }

    def config_factory(gamma: str):
        def config(config, root):
            config["gamma"] = gamma
            return config

        return config

    execute_eqiro_experiment(
        "gamma",
        config,
        [
            {"name": "gaussian", "config_factory": config_factory("gaussian")},
            {"name": "poly", "config_factory": config_factory("poly")},
        ],
    )


def fitness_experiment():
    config = {
        "size": 5,
        "k_out": 10,
        "g_alpha": 0.5,
        "gamma_mul": 1,
        "lambda": 1.2,
        "recombination_prob": 0.15,
        "oracle": "odd",
        "recombine": True,
        "fitness_function": "square",
        "diffusion_recombine": True,
        "gamma": "gaussian",
        "target_fitness": 0,
        "fitness_threshold": 0.1,
        "mutate_factor": 1 / 8,
        "iterations": 50,
    }

    def config_factory(c: any):
        def config(config, root):
            for key, value in c.items():
                config[key] = value
            return config

        return config

    execute_eqiro_experiment(
        "fitness",
        config,
        [
            {
                "name": "not_recombine",
                "config_factory": config_factory(
                    {
                        "recombine": False,
                        "diffusion_recombine": False,
                    }
                ),
            },
            {
                "name": "diffusion_recombine",
                "config_factory": config_factory(
                    {
                        "recombine": True,
                        "diffusion_recombine": True,
                    }
                ),
            },
        ],
    )


def angles_experiment():
    config = {
        "size": 6,
        "k_out": 2,
        "g_alpha": 0.75,
        "gamma_mul": 0.15,
        "recombination_module": 8,
        "lambda": 1.2,
        "recombine": True,
        "oracle": "odd",
        "target_fitness": -0.7,
        "fitness_threshold": 0.1,
        "fitness_function": "sin",
        "gamma": "gaussian",
        "iterations": 50,
    }

    def config_factory(scaled: bool):
        def config(config, root):
            config["rescaled_angles"] = scaled
            return config

        return config

    execute_eqiro_experiment(
        "angles",
        config,
        [
            {"name": "normal", "config_factory": config_factory(False)},
            {"name": "scaled", "config_factory": config_factory(True)},
        ],
    )
