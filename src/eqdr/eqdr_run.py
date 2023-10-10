import csv
import json
from multiprocessing import Process
import os
from src.eqdr.eqdr import Eqdr
from src.fitness import fitness_factory
from src.oracles import oracles_factory


def execute_eqdr_experiment(name: str, workers: "list[any]"):
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


def eqdr_run(config: any):
    n = config["size"]
    targets = config.get("targets", None)
    fitness_function = fitness_factory(**config["fitness"])
    oracle = oracles_factory(config["size"], **config["oracle"])
    its = config["iterations"]
    id = config["id"]
    prefix = config.get("prefix", None)
    if prefix is None:
        prefix = ""
    else:
        prefix += " - "
    reportFileName = config["report"]
    # print(str(id) + " > targets: " + str(targets))
    # oracle = odd_oracle(n=n)

    count = 0
    with open(reportFileName, "w", newline="") as file:
        csvwriter = csv.writer(file)
        csvwriter.writerow(
            [
                "n",
                "iterations",
                "recombinations",
                "avg_iterations",
                "avg_recombinations",
            ]
        )
    eqdr = Eqdr(
        oracleImp=oracle,
        fitnessFunctionImp=fitness_function,
        isGoodState=lambda x: x in targets if targets is not None else None,
        **config,
    )
    iterations = 0
    recombinations = 0
    for j in range(its):
        res = eqdr.optimize()
        iterations += res.statistics["iterations"]
        recombinations += res.statistics["recombinations"]
        count += 1
        print(
            prefix
            + str(id)
            + " > it: "
            + str(count)
            + "/"
            + str(its)
            + " - "
            + str({"avg_it": iterations / (j + 1), "avg_rec": recombinations / (j + 1)})
        )
        with open(reportFileName, "a", newline="") as file:
            csvwriter = csv.writer(file)
            csvwriter.writerow(
                [
                    j,
                    res.statistics["iterations"],
                    res.statistics["recombinations"],
                    iterations / (j + 1),
                    recombinations / (j + 1),
                ]
            )
