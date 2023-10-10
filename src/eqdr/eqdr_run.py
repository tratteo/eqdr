import csv
from src.eqdr.eqdr import Eqdr
from src.fitness import fitness_factory
from src.oracles import oracles_factory


class EqdrResult:
    def __init__(
        self,
        solutions: "list[tuple[str, float]]",
        statistics: any,
    ) -> None:
        self.solutions: list[tuple[str, float]] = solutions
        self.statistics = statistics


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
