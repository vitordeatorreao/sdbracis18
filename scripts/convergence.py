"""Creates a plot of the convergence numbers for each algorithm"""

import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
import numpy as np

from utils import COLORS, convergence_by_alg, get_convergences, read_all

plt.style.use('ggplot')
X = np.zeros((8,6))

def main():
    """Main function"""
    algorithms, _ = read_all("data")
    proportions = np.asarray([1, 2, 5, 10, 15, 25, 50, 100])
    proportioni = [i for i in range(0, len(proportions))]
    betas = { "1.0": 1, "3.0": 2, "9.0": 3, "27.0": 4, "81.0": 5, "": 0 }
    algorithm_names = ["mesdif", "nmefsd", "ssdp"]
    convergences = dict()
    for proportion in proportions:
        convergences[proportion] = get_convergences(proportion, algorithms)
    plt.rc("font", size=14)
    fig, axes = plt.subplots(1, 3, sharex="col")
    alg_i = 0
    lines = [None] * len(betas)
    line_names = [str()] * len(betas)
    for alg_name in algorithm_names:
        i = 0
        for proportion in proportions:
            convs = convergence_by_alg(alg_name, convergences[proportion])
            for beta in betas:
                X[i, betas[beta]] = convs[beta]
            i += 1
        bi = 0
        for beta in betas:
            name = "base" if not beta else r"$\beta:$ " + beta
            lines[bi], = axes[alg_i].plot(proportioni, X[:, betas[beta]],
                marker='o', label=name, color=COLORS[bi])
            line_names[bi] = name
            bi += 1
        axes[alg_i].set_xlabel("proportion of features (%)")
        axes[alg_i].set_ylabel("number of convergences")
        axes[alg_i].set_title(
            "Convergence by Initialization - " + alg_name.upper())
        axes[alg_i].set_xticks(proportioni)
        axes[alg_i].set_xticklabels(proportions)
        alg_i += 1
    fig.legend(lines, line_names, loc="lower center", ncol=len(lines))
    fig.set_size_inches(39.29112, 9.82278)
    fig.set_dpi(200)
    fig.savefig("images/convergence.pdf", bbox_inches="tight")

if __name__ == "__main__":
    main()
