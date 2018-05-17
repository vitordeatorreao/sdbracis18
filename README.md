# Effects of Population Initialization on Evolutionary Techniques for Subgroup Discovery in High Dimensional Datasets

In this repository you will find the support material for the paper entitled
"Effects of Population Initialization on Evolutionary Techniques for Subgroup
Discovery in High Dimensional Datasets" which was submitted to the BRACIS 2018
conference. As such, this material is not designed to be understood on its own:
it should be read along side a copy of paper.

## Files in this repository

An explanation of the files found in this repository follows:

The `data` folder contains all the data about the algorithms' performance
collected for the study in the different datasets tested. Inside, each folder is
named after one of the studied datasets. As such, the contents of these folders
is the results of each algorithm's execution in different versions of the
dataset. Since each algorithm was executed in each dataset 30 times, any given
CSV file in this folder will contain 31 lines (1 for the header). The files'
names indicate the context of the results, and they follow the rule:

```
<DATASET_NAME>-pn-<DISCRETIZATION_METHOD>_<PROPORTION_OF_FEATURES>p_<ALGORITHM_NAME>[_a<ALPHA_VALUE>_b<BETA_VALUE>].CSV
```

The `images` folder contains a superset of the images included in the paper. It
also contains images for the final ranking of algorithms in the experiments on
which each algorithm is compared to its modified versions using different values
of alpha and beta. These images are generated using the Python scripts in the
`scripts` folder.

The `scripts` folder contains Python 3.6 scripts which run the statistical tests
explained in the paper, display their results as well as plot the images which
are shown in the paper. To execute the scripts, follow the instructions in the
section down below.

## Images

The following images are not present in the paper:

* `images/mesdif_Support.pdf`: this shows the final average ranks, calculated
using the Nemenyi critical distance, for the MESDIF algorithm when compared to
its modified versions using different values of alpha and beta, and using the
Support of a rule as quality metric;
* `images/mesdif_WRACC.pdf`: the same as the previous item, but using the WRACC
quality metric instead;
* `images/nmefsd_Support.pdf`: this shows the final average ranks, calculated
using the Nemenyi critical distance, for the NMEEF-SD algorithm when compared to
its modified versions using different values of alpha and beta, and using the
Support of a rule as quality metric;
* `images/nmefsd_WRACC.pdf`: the same as the previous item, but using the WRACC
quality metric instead;
* `images/ssdp_Support.pdf`: this shows the final average ranks, calculated
using the Nemenyi critical distance, for the SSDP algorithm when compared to
its modified versions using different values of alpha and beta, and using the
Support of a rule as quality metric;
* `images/ssdp_WRACC.pdf`: the same as the previous item, but using the WRACC
quality metric instead;

These pictures show that, except for the SSDP algorithm, the modified versions
of the algorithms using `alpha = 1.0` and `beta = 81.0` provide the best quality
rules in the resulting population (after the entire evolutionary algorithm has
been executed).

## Running the Python scripts

In order to run the Python scripts in the `scripts` folder, you must have a
Python 3.6 distribution installed with the necessary packages. Every package
this project depends on is available in the
[Python Package Index](https://pypi.org/) and can be installed through the
[Python Package Manager](https://docs.python.org/3/installing/).

To do so, run the following commands in your command prompt or shell. First, you
must change directory to this project's root directory (that would probably be
the one called `bracis2018`.)

```sh
$ pip install -r requirements.txt
```

The above will install every Python package needed. After that, you must run
the scripts which generate the images. Like so (again, you must be in this
project's root directory):

```sh
$ python scripts/convergence.py # generates the images related to convergence
$ python scripts/stat_tests.py # generates the images with the nemenyi tests
$ python scripts/betadist.py # generates the images with the different beta distributions
```
