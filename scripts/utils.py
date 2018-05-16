"""Set of utility function definitions which will power the other scripts in
this folder. The other scripts are just main functions and the real data
processing is done by the functions in this file."""

import csv
import os
import re

import numpy as np

DATASETS = [
    "alon",
    "burczynski",
    "chiaretti",
    "chin",
    "christensen",
    "gravier",
    "nakayama",
    "sun",
    "tian",
    "yeoh"
]

COLORS = [
    "#ff7f00",
    "#377eb8",
    "#984ea3",
    "#000000",
    "#4daf4a",
    "#e41a1c"
]

PROPORTIONS = [
    1, 2, 5, 10, 15, 25, 50, 100
]

def get_names(filename: str):
    """Retrieves the name of the algorithm and dataset from the file name"""
    pattern = re.compile(r"(.+_\d{1,3}p)_(.+).[Cc][Ss][Vv]")
    match = pattern.match(filename)
    if not match:
        return None, None
    return match.group(1), match.group(2)

def convergence_by_alg(algorithm:str, convergences):
    """Retrieves a dictionary with the beta values and their number of
    convergence."""
    betas = dict()
    alg_pattern = re.compile(algorithm)
    beta_pattern = re.compile(r"\_b(\d{1,2}\.\d{1})")
    for alg in convergences:
        if not alg_pattern.search(alg):
            continue
        match = beta_pattern.search(alg)
        if match:
            betas[match.groups()[0]] = convergences[alg]
        else:
            betas[""] = convergences[alg]
    return betas

def get_convergences(proportion:int, algorithms):
    """Retrieves a dictionary with the algorithms as keys and the number
    of times they converged."""
    regex = "_" + str(proportion) + "p"
    convergences = dict()
    zero_pat = re.compile(r"0\.(0+)$")
    metric = "Support"
    for algorithm in algorithms:
        convergence = 0
        for dataset in algorithms[algorithm]:
            if not re.search(regex, dataset):
                continue
            for observation in algorithms[algorithm][dataset]:
                if metric not in observation:
                    continue
                if observation[metric] == "NaN":
                    continue
                elif zero_pat.match(observation[metric]):
                    continue
                else:
                    convergence += 1
        convergences[algorithm] = convergence
    return convergences

def get_all_proportions_sample(metric: str, algorithms):
    """Retrieves a dictionary with the algorithms as keys and the observations
    of the given metric a python list."""
    samples = dict()
    for proportion in PROPORTIONS:
        samps = get_samples(proportion, metric, algorithms)
        for algorithm in samps:
            if algorithm not in samples:
                samples[algorithm] = list()
            samples[algorithm] += samps[algorithm]
    return samples

def get_samples(proportion:int, metric: str, algorithms):
    """Retrieves a dictionary with the algorithms as keys and the observations
    of the given metric as a python list."""
    regex = "_" + str(proportion) + "p"
    samples = dict()
    zero_pat = re.compile(r"0\.0{6,}")
    for algorithm in algorithms:
        observations = list()
        for dataset in algorithms[algorithm]:
            if not re.search(regex, dataset):
                continue
            sum_ = 0.0
            qty = 0.0
            for observation in algorithms[algorithm][dataset]:
                if metric not in observation:
                    continue
                if observation[metric] == "NaN":
                    continue
                elif metric == "WRACC" and zero_pat.match(observation[metric]):
                    continue
                try:
                    sum_ += float(observation[metric])
                    qty += 1.0
                except ValueError:
                    continue
            if qty > 0:
                observations.append(sum_ / qty)
            else:
                observations.append(float("nan"))
        samples[algorithm] = observations
    return samples

def get_nemenyi_table():
    """Reads and retrieves the Nemenyi statistic table"""
    npath = os.path.join("scripts", "nemenyi.csv")
    table = dict()
    with open(npath, "r") as nfile:
        reader = csv.DictReader(nfile)
        for line in reader:
            nmodels = int(line["# models"])
            if nmodels not in table:
                table[nmodels] = dict()
            table[nmodels]["0.01"] = line["Nemenyi 0.01"]
            table[nmodels]["0.05"] = line["Nemenyi 0.05"]
            table[nmodels]["0.10"] = line["Nemenyi 0.10"]
    return table

def get_nemenyi_stat(num_models:int, significance_level:float) -> float:
    """Retrieves the Studentised range statistic for infinite degrees of
    freedom divided by the square root of 2."""
    if num_models > 100:
        raise ValueError("A comparison between more than 100 models is "+
                         "not supported.")
    alpha = "{:.2f}".format(significance_level)
    if alpha != "0.05" and alpha != "0.01" and alpha != "0.10":
        raise ValueError(("The significance value '{0}' is not " +
                          "supported.").format(alpha))
    table = get_nemenyi_table()
    return float(table[num_models][alpha])

def read_all(folder: str):
    """Reads all the information into memory"""
    algorithms = dict()
    datasets = dict()
    for dataset in DATASETS:
        folder_path = os.path.join(folder, dataset)
        file_names = [name for name in os.listdir(folder_path) \
                           if os.path.isfile(os.path.join(folder_path, name))]
        for file_name in file_names:
            dataset, algorithm = get_names(file_name)
            if not algorithm or not dataset:
                continue
            observations = list()
            with open(os.path.join(folder_path, file_name), "r") as file_:
                reader = csv.DictReader(file_)
                for line in reader:
                    observations.append(line)
            if algorithm not in algorithms:
                algorithms[algorithm] = dict()
            if dataset not in datasets:
                datasets[dataset] = dict()
            if algorithm not in datasets[dataset]:
                datasets[dataset][algorithm] = list()
            if dataset not in algorithms[algorithm]:
                algorithms[algorithm][dataset] = list()
            datasets[dataset][algorithm] += observations
            algorithms[algorithm][dataset] += observations
    return algorithms, datasets
