## Elite Quantum Diffusion Recombination

Adapting Grover's Quantum Search algorithm to fitness based multimodal optimization problems.

**Document**: [EQDR: an Elite Quantum Diffusion Recombination procedure](https://github.com/tratteo/eqdr/blob/main/eqdr.pdf)

## Execute

### Dependencies
```sh
pip install -r requirements.txt
```

### Run example
```sh
python run.py <id>
```

#### Running custom experiments
```python
# Experiment name
experiment_name = "rastrigin"

# Common parameters
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

# Run experiments, each identified by its instance_name. Results will be saved in > results/<experiment_name>_<instance_name>.csv

# Read the eqdr.pdf thesis file to know the different parameters

execute_eqiro_experiment(
    experiment_name,
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
```