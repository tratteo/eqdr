import math


def polyGamma(f: float, rank: int, **kwargs):
    alpha = kwargs.get("alpha")
    return math.pow(alpha, rank)


def gaussianGamma(f: float, rank: int, **kwargs):
    k = kwargs.get("k", 1)
    return math.exp((rank * rank * math.log(f)) / (k * k))


def identityGamma(f: float, rank: int, **kwargs):
    return 1
