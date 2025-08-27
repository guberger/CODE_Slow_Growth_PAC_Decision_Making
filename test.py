from math import log, sqrt
import random
import numpy as np
import matplotlib.pyplot as plt

def sample_con_1(p: float):
    i = np.random.geometric(p) - 1
    j = np.random.geometric(p) - 1
    return (i, j)

def sample_con_2(p: float):
    return np.random.geometric(p) - 1

def sample_constraints(p: float, N: int):
    cons_1 = []
    cons_2 = []
    for _ in range(N):
        b = random.randint(0, 1)
        if b == 0:
            cons_1.append(sample_con_1(p))
        else:
            cons_2.append(sample_con_2(p))
    return cons_1, cons_2

def compute_risk(cons_1: list, cons_2: list, p: float):
    k, l = max((max(con), min(con)) for con in cons_1)
    risk_1 = 0.5 * ((1 - p) ** (k + l)) * (p * p)
    risk_2 = 0.0
    cons_2_set = set(cons_2)
    for i in range(k):
        if i not in cons_2_set:
            risk_2 = risk_2 + 0.5 * ((1 - p) ** i) * p
    return risk_1 + risk_2

def run_experiments(N_list: list, M: int):
    all_results = []
    for N in N_list:
        results = []
        for _ in range(M):
            cons_1, cons_2 = sample_constraints(p, N)
            risk = compute_risk(cons_1, cons_2, p)
            results.append(risk)
        all_results.append(results)
    return all_results

def compute_bound(N: int, delta: float):
    assert N > 0
    return 4 * (3 * log(2) * sqrt(2 * N) + log(2) - log(delta)) / N

p = 0.25
N_list = [10, 32, 100, 316, 1000, 3162, 10000]
M = 50
all_results = run_experiments(N_list, M)
eps_list = [compute_bound(N, 0.05) for N in N_list]

# Create boxplot
plt.boxplot(all_results)
plt.plot(range(1, len(N_list) + 1), eps_list, "--x", c="magenta")
# Add labels for each vector on x-axis
plt.xticks(range(1, len(N_list) + 1), N_list)
plt.xlabel(r"$m$")
plt.ylabel(r"$1-\mu(A(S))$")
plt.title("Boxplot of the value of the risk")
plt.yscale("log")
plt.savefig("boxplot.png", dpi=300, bbox_inches="tight")
plt.show()