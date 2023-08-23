from qiskit.circuit.library.phase_oracle import PhaseOracle
from qiskit.exceptions import MissingOptionalLibraryError
from qiskit import ClassicalRegister, QuantumCircuit, transpile
from qiskit.algorithms import AmplificationProblem
from qiskit.algorithms import Grover
from qiskit.primitives import Sampler
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt
import numpy as np
from qiskit_aer import AerSimulator
import math
from src.gamma import gaussianGamma
from src.oracles import oracles_factory

alpha = 0.2


def g_p(x):
    a = (alpha) ** (0.25)
    return a**x


def g_g(x):
    return np.exp((np.power(x, 2) * np.log(alpha)) / 16)


import random

# bits = [[-1, -1, +1, -1], [-1, -1, +1, +1], [-1, +1, +1, +1]]
# alpha = 16 / 81
# c = []
# a = []
# max_gamma = sum([gaussianGamma(0, i, k=4, a=alpha) for i in range(4)])
# for k, b in enumerate(bits):
#     ci = 0
#     for j, bit in enumerate(b):
#         ci += bit * gaussianGamma(0, j, k=4, a=alpha)
#     print(f"c{k}={ci}")
#     print(f"a{k}={abs(ci)/max_gamma}")
# exit()
# from numpy import sqrt
# from qiskit.quantum_info import Statevector

# diff = "111"
qc = QuantumCircuit(2)
qc.x(0)
qc.h(1)
qc.cz(0, 1)
qc.h(1)
qc.x(0)

qc.draw(output="mpl", filename="test.svg")
# qc.ry(math.pi / 12, 0)
# qc.ry(math.pi / 2, 1)
# qc.ry(math.pi / 2, 2)
# p = AmplificationProblem(
#     oracle=Statevector.from_label(diff),
#     is_good_state=[diff],
# )
# measurement_cr = ClassicalRegister(len(diff))
# qc.add_register(measurement_cr)
# m = [i for i in range(len(diff))]
# qc.measure(m, reversed(m))

# bk = AerSimulator()
# job_sim = bk.run(transpile(qc, bk), shots=4096)
# result_sim = job_sim.result()
# print(result_sim.get_counts())

# plot_histogram(result_sim.get_counts(), filename="graph.png", figsize=(21, 9))
# exit()
# sv = Statevector([1, 0])
# sv.draw(output="bloch", filename="s.png")
# sv = Statevector([0, 1])
# sv.draw(output="bloch", filename="s1.png")
size = 8
x = np.linspace(0, size * 3, 1000)
y = multimodal_fitness(x, size)
plt.figure(figsize=(16, 9))
plt.plot(x, y, color=(0, 0.5, 1, 1))
plt.axvline(x=size, color="r", linestyle="dotted")
plt.xticks(np.arange(0, (size + 1) * 3, step=1))
# plt.legend([r"\TeX\ \gamma", "gaussian"])
plt.savefig(r"C:\Users\matteo\Documents\UniTn\Tesi\assets\multimodal_8.svg")
plt.show()
# qc = QuantumCircuit(2)
# qc.h(0)
# qc.cx(0, 1)
# # qc.h(1)
# # qc.measure_all()
# qc.decompose("cx").draw(
#     filename="h.png",
#     output="mpl",
#     plot_barriers=False,
#     initial_state=False,
# )
