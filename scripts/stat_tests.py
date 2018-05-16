"""Performs the statiscal tests to evaluate the best approach"""

import math
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
import numpy as np
import Orange
import os

from scipy.stats import friedmanchisquare
from nemenyi import NemenyiTestPostHoc
from utils import get_all_proportions_sample, read_all, get_nemenyi_stat

plt.style.use('ggplot')

SIGNIFICANCE_LEVEL = 0.05

MESDIF_COMP = [
    "mesdif",
    "mesdif_a1.0_b1.0",
    "mesdif_a1.0_b3.0",
    "mesdif_a1.0_b9.0",
    "mesdif_a1.0_b27.0",
    "mesdif_a1.0_b81.0"
]

NMEEF_COMP = [
    "nmefsd",
    "nmefsd_a1.0_b1.0",
    "nmefsd_a1.0_b3.0",
    "nmefsd_a1.0_b9.0",
    "nmefsd_a1.0_b27.0",
    "nmefsd_a1.0_b81.0"
]

SSDP_COMP = [
    "ssdp",
    "ssdp_a1.0_b1.0",
    "ssdp_a1.0_b3.0",
    "ssdp_a1.0_b9.0",
    "ssdp_a1.0_b27.0",
    "ssdp_a1.0_b81.0"
]

COMPETITIONS = {
    "mesdif": MESDIF_COMP,
    "nmefsd": NMEEF_COMP,
    "ssdp": SSDP_COMP,
    "all": [
        "ssdp",
        "mesdif_a1.0_b81.0",
        "nmefsd_a1.0_b81.0",
        "ssdp_a1.0_b81.0",
        "mesdif",
        "nmefsd"
    ]
}

def format_float(val: float) -> str:
    """Formats the float number to be better visualized"""
    if val < 0.0001:
        return "{:.2e}".format(val)
    else:
        return "{:.4f}".format(val)

def fmt(competitor_name: str) -> str:
    """Formats the competitor's name"""
    name = competitor_name.replace("_a", r" $\alpha$ ")
    name = name.replace("_b", r" $\beta$ ")
    return name

def compete(algorithms, metric:str):
    """Makes the statiscal tests for all competitions using the given metric"""
    samples = get_all_proportions_sample(metric, algorithms)
    for competition_name in COMPETITIONS:
        competitors = list()
        for competitor in COMPETITIONS[competition_name]:
            competitors.append(samples[competitor])
        _, pvalue = friedmanchisquare(*competitors)
        print(metric + ", " + competition_name + ": pvalue = " +
              format_float(pvalue))
        if pvalue < SIGNIFICANCE_LEVEL:
            # Invert the measures, because Nemeyi expects ordering to be from
            # lowest to highest
            measures = list()
            for competitor in COMPETITIONS[competition_name]:
                if metric == "WRACC":
                    measures.append([0.25 - s for s in samples[competitor]])
                elif metric == "Support":
                    measures.append([1 - s for s in samples[competitor]])
                else:
                    raise ValueError("Unknown metric '{0}'".format(metric))
            nemenyi = NemenyiTestPostHoc(np.asarray(measures))
            mean_ranks, _ = nemenyi.do()
            ncompetitors = len(competitors)
            nemenyistat = get_nemenyi_stat(ncompetitors, SIGNIFICANCE_LEVEL)
            cdiff = nemenyistat * math.sqrt((ncompetitors * (ncompetitors + 1))\
                                            / (6 * len(measures[0])))
            Orange.evaluation.graph_ranks(mean_ranks,
                list(map(fmt, COMPETITIONS[competition_name])),
                cd=cdiff, textspace=1.6)
            imgpath = os.path.join("images",
                                   competition_name + "_" + metric + ".pdf")
            ax = plt.gca()
            ax.text(0.1, 0.9, metric, horizontalalignment="center",
                    verticalalignment="center", transform=ax.transAxes)
            plt.savefig(imgpath)

def main():
    """Main function"""
    algorithms, _ = read_all("data")
    compete(algorithms, "WRACC")
    compete(algorithms, "Support")

if __name__ == "__main__":
    main()
