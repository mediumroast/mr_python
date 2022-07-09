# Introduction
This is the Python Software Development Kit (SDK) for the mediumroast.io.  Internal tooling from Mediumroast, Inc. uses this SDK, so it will always be a first class citizen. Specifically, we build tools requiring ETL (Extract, Transform and Load), Machine Learning and Natural Language Processing (NLP) with this SDK. As appropriate examples illustrating various capabilities of the SDK can be found in the `examples/` directory of this package.  

# Installation and Configuration Steps for Developers
The following steps are important if you are developing or extending the Python SDK.  If you're not a developer these steps aren't as important to you and you should pay attention to section entitled *Installation for Early Adopters and Testers*.

## Cloning the repository for Developers
Assuming `git` is installed and your credentials are set up to talk to the mediumroast.io set of repositories it should be possible to do the following as a user on the system:
1. `mkdir ~/dev;cd ~/dev`
2. `git clone git@github.com:mediumroast/mediumroast_py.git`
This will create an `mediumroast_py` directory in `~/dev/` and allow you to proceed to the following steps for installation.

## Installation
For developers of the package the `setup.py` file is available to enable a local software distribution that can be improved upon.  As inspired by [this article](https://python-packaging-tutorial.readthedocs.io/en/latest/setup_py.html) the best current way to perform the installation of a developer version after cloning is to assuming you've cloned into `~/dev`:
1. `cd ~/dev/mr_sdk/python`
2. `sudo pip install -e ./`
With this accomplished tools that you've written which depend upon this package should operate.  If there are issues encountered then please open an [issue](https://github.com/mediumroast/mr_python/issues).

## Structure of the repository
The following structure is available for the Python SDK, as new SDK implementations are created additional top level directories will be created.
```
mr_python/
      examples/
      mediumroast_py/
            api/
            extractors/
            transformers/
            helpers.py
      project.toml
      README.md
      LICENSE
```

# The Examples
To illustrate how to interact programmatically with the mediumroast.io application several examples have been created to make it easier for developers to interact with the system.  The scope of the examples, over time, will include all aspects of the SDK to speed up 3rd party development processes.  This means that over time examples for all apsects of the SDK will be produced and made available under the Apache Software License.  As with anything in the SDK if you run into problems please make sure that you raise an [issue](https://github.com/mediumroast/mediumroast_py/issues) in the repository.  More detail on the examples can be found within the [examples directory](https://github.com/mediumroast/mediumroast_py/examples) of this repository.