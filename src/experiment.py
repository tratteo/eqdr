import json
from multiprocessing import Process
import os
import random

from src.eqdr.eqdr_run import eqdr_run


def execute_eqiro_experiment(name: str, workers: "list[any]"):
    root = os.path.join("results", name)
    if not os.path.exists(root):
        os.makedirs(root)

    # with open(os.path.join(root, "config.json"), "w") as outfile:
    #     outfile.write(json.dumps(config, indent="\t"))

    processes = []
    for i, k in enumerate(workers):
        c = k["config"]
        c["id"] = i
        c["report"] = os.path.join(root, k["name"] + ".csv")
        # c = k["config_factory"](c, root)
        c["prefix"] = name + "_" + k["name"]
        with open(os.path.join(root, k["name"] + "_config.json"), "w") as outfile:
            outfile.write(json.dumps(c, indent="\t"))
        processes.append(Process(target=eqdr_run, args=[c]))

    for p in processes:
        p.start()
    for p in processes:
        p.join()

    print("experiment " + name + " completed")
