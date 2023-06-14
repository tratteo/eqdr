from multiprocessing import Process
import sys

from src.experiment import run_experiment

if __name__ == "__main__":
    processes = []
    sequential = "--sequential" in sys.argv
    arguments = sys.argv.copy()

    arguments.pop(0)
    if sequential:
        arguments.remove("--sequential")
    for a in arguments:
        if sequential:
            run_experiment(a)
        else:
            processes.append(Process(target=run_experiment, args=[a]))
    if not sequential:
        for p in processes:
            p.start()
        for p in processes:
            p.join()
