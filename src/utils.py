import json
from random import choice


def loadConfig(path: str = None):
    if path is None:
        path = "config/std.json"
    f = open(path)
    data = json.load(f)
    return data


def generate_binary_string(n):
    return "".join(choice("01") for _ in range(n))
