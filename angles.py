import math


def computeFinalState(coefficients, angles):
    cos1 = math.cos(angles[0] / 2)
    sin1 = math.sin(angles[0] / 2)
    cos2 = math.cos(angles[1] / 2)
    sin2 = math.sin(angles[1] / 2)
    a, b, c, d = coefficients[0], coefficients[1], coefficients[2], coefficients[3]
    oo = (cos1 * (a * cos2 - b * sin2)) - (sin1 * (c * cos2 - d * sin2))
    oi = (cos1 * (a * sin2 + b * cos2)) - (sin1 * (c * sin2 + d * cos2))
    io = (sin1 * (a * cos2 - b * sin2)) + (cos1 * (c * cos2 - d * sin2))
    ii = (sin1 * (a * sin2 + b * cos2)) + (cos1 * (c * sin2 + d * cos2))
    return [oo, oi, io, ii]


if __name__ == "__main__":
    coefficients = [math.sqrt(0.4), math.sqrt(0.025), math.sqrt(0.4), math.sqrt(0.175)]
    coefficients = [math.sqrt(0.25), math.sqrt(0.25), math.sqrt(0.25), math.sqrt(0.25)]
    probabilities = [x**2 for x in coefficients]
    if sum(probabilities) < 1 or sum(probabilities) > 1:
        print("invalid initial coefficients")
        exit(1)
    angles = [0, 2 * math.pi / 3]
    state = computeFinalState(coefficients, angles)
    print("INITIAL STATE")
    print("coefficients")
    print([("{0:02b}".format(i), x) for i, x in enumerate(coefficients)])
    print("probabilities")
    print([("{0:02b}".format(i), x) for i, x in enumerate(probabilities)])
    print()
    print("FINAL STATE")
    print("coefficients")
    print([("{0:02b}".format(i), x) for i, x in enumerate(state)])
    print("probabilities")
    print([("{0:02b}".format(i), x**2) for i, x in enumerate(state)])
