from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D
import math
import matplotlib.pyplot as plt
import numpy as np


def rastrigin(*X, **kwargs):
    A = kwargs.get("A", 10)
    return A * len(X) + sum([(x**2 - A * np.cos(2 * math.pi * x)) for x in X])


if __name__ == "__main__":
    X = np.linspace(-6, 6, 500)
    Y = np.linspace(-6, 6, 500)

    X, Y = np.meshgrid(X, Y)

    Z = rastrigin(X, Y, A=10)

    fig = plt.figure(figsize=(16, 12))
    ax = fig.add_subplot(projection="3d")

    ax.plot_surface(
        X, Y, Z, rstride=1, cstride=1, cmap=cm.plasma, linewidth=0, antialiased=True
    )
    # plt.show()
    plt.tight_layout()
    plt.savefig(r"C:\Users\matteo\Documents\UniTn\Tesi\assets\rastrigin.png")
