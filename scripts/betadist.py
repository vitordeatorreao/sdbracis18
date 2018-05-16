"""Generates the image for the beta distribution"""

import math
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
import numpy as np
import os
from scipy.special import gamma

from utils import COLORS

plt.style.use('ggplot')

def beta(x, alpha, beta):
    """beta pdf"""
    num = math.pow(x, alpha - 1) * math.pow(1 - x, beta - 1)
    denom = (gamma(alpha) * gamma(beta)) / (gamma(alpha + beta))
    return num / denom

def main():
    """main function"""
    funcs = [(1.0, 1.0), (1.0, 3.0), (1.0, 9.0), (1.0, 27.0), (1.0, 81.0)]
    X = np.arange(0, 1, 0.001, dtype=np.float)
    funci = 0
    for alpha, bet in funcs:
        vfunc = np.vectorize(lambda x: beta(x, alpha, bet))
        Y = vfunc(X)
        plt.plot(X, Y, color=COLORS[funci],
                 label=r"$\alpha$ = " + str(alpha) + r"; $\beta$ = " + str(bet))
        funci += 1
    plt.xlabel(r"$x$")
    plt.ylabel("PDF")
    plt.legend()
    ax = plt.gca()
    ax.set_ylim([0.0, 2.5])
    figpath = os.path.join("images", "beta.pdf")
    plt.savefig(figpath)

if __name__ == "__main__":
    main()
