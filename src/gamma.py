import math


def polyGamma(f: float, rank: int, **kwargs):
    alpha = kwargs.get("a", 0.95)
    return math.pow(alpha, rank)


def gaussianGamma(f: float, rank: int, **kwargs):
    k = kwargs.get("k", 1)
    alpha = kwargs.get("a", 0.5)
    return math.exp((rank * rank * math.log(alpha)) / (k * k))


def identityGamma(f: float, rank: int, **kwargs):
    return 1
