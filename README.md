[![Spock](https://raw.githubusercontent.com/fidelity/spock/master/resources/images/logo.png)](https://fidelity.github.io/spock/)
> Managing complex configurations any other way would be highly illogical...

[![License](https://img.shields.io/badge/License-Apache%202.0-9cf)](https://opensource.org/licenses/Apache-2.0)
[![Python](https://img.shields.io/badge/python-3.6+-informational.svg)](https://www.python.org/)
[![Style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![PyPI version](https://badge.fury.io/py/spock-config.svg)](https://badge.fury.io/py/spock-config)
[![Coverage Status](https://coveralls.io/repos/github/fidelity/spock/badge.svg?branch=master)](https://coveralls.io/github/fidelity/spock?branch=master)
![Tests](https://github.com/fidelity/spock/workflows/pytest/badge.svg?branch=master)
![Docs](https://github.com/fidelity/spock/workflows/docs/badge.svg)

## About

`spock` is a framework that helps manage complex parameter configurations during research and development of Python 
applications. `spock` lets you focus on the code you need to write instead of re-implementing boilerplate code like 
creating ArgParsers, reading configuration files, implementing traceability etc.

In short, `spock` configurations are defined by simple and familiar class-based structures. This allows `spock` to 
support inheritance, read from multiple markdown formats, automatically generate cmd-line arguments, and allow 
hierarchical configuration by composition.

## Key Features

* [Simple Declaration](https://fidelity.github.io/spock/docs/basic_tutorial/Define/): Type checked parameters are 
  defined within a `@spock` decorated class. Supports required/optional and automatic defaults.
* Easily Managed Parameter Groups: Each class automatically generates its own object within a single namespace.
* [Parameter Inheritance](https://fidelity.github.io/spock/docs/advanced_features/Inheritance/): Classes support 
  inheritance (w/ lazy evaluation of inheritance/dependencies) allowing for complex configurations derived from 
  a common base set of parameters.
* [Complex Types](https://fidelity.github.io/spock/docs/advanced_features/Advanced-Types/): Nested Lists/Tuples, 
  List/Tuples of Enum of `@spock` classes, List of repeated `@spock` classes
* Multiple Configuration File Types: Configurations are specified from YAML, TOML, or JSON files.
* [Hierarchical Configuration](https://fidelity.github.io/spock/docs/advanced_features/Composition/): Compose from 
  multiple configuration files via simple include statements.
* [Command-Line Overrides](https://fidelity.github.io/spock/docs/advanced_features/Command-Line-Overrides/): Quickly 
  experiment by overriding a value with automatically generated command line arguments.
* Immutable: All classes are *frozen* preventing any misuse or accidental overwrites (to the extent they can be in 
  Python).
* [Tractability and Reproducibility](https://fidelity.github.io/spock/docs/basic_tutorial/Saving/): Save runtime 
  parameter configuration to YAML, TOML, or JSON with a single chained command (with extra runtime info such as Git info, 
  Python version, machine FQDN, etc). The saved markdown file can be used as the configuration input to reproduce 
  prior runtime configurations.
* [Hyper-Parameter Tuner Addon](https://fidelity.github.io/spock/docs/addons/tuner/About): Provides a unified
  interface for defining hyper-parameters (via `@spockTuner` decorator) that supports various tuning/algorithm 
  backends (currently: Optuna, Ax)
* [S3 Addon](https://fidelity.github.io/spock/docs/addons/S3/): Automatically detects `s3://` URI(s) and handles loading 
  and saving `spock` configuration files when an active `boto3.Session` is passed in (plus any additional 
  `S3Transfer` configurations)

## Quick Install

The basic install and `[s3]` extension require Python 3.6+ while the `[tune]` extension requires Python 3.7+

| Base | w/ S3 Extension | w/ Hyper-Parameter Tuner |
|------|-----------------|--------------------------|
| `pip install spock-config` | `pip install spock-config[s3]` | `pip install spock-config[tune]` |

## Quick Start & Documentation

Refer to the quick-start guide [here](https://fidelity.github.io/spock/docs/Quick-Start/).

Current documentation and more information can be found [here](https://fidelity.github.io/spock/).

Example `spock` usage is located [here](https://github.com/fidelity/spock/blob/master/examples).

## News/Releases

See [Releases](https://github.com/fidelity/spock/releases) for more information.

#### January 18th, 2022
* Support for lazy evaluation: (1) inherited classes do not need to be `@spock` decorated, (2) dependencies/references 
between `spock` classes can be lazily handled thus preventing the need for every `@spock` decorated classes to be 
passed into `*args` within the main `SpockBuilder` API
* Updated main API interface for better top-level imports (backwards compatible): `ConfigArgBuilder`->`spockBuilder`
* Added stubs to the underlying decorator that should help with type hinting in VSCode (pylance/pyright)

#### December 14, 2021
* Refactored the backend to better handle nested dependencies (and for clarity)
* Refactored the docs to use Docusaurus

#### August 17, 2021
* Added hyper-parameter tuning backend support for Ax via Service API

## Original Implementation

[Nicholas Cilfone](https://github.com/ncilfone), [Siddharth Narayanan](https://github.com/sidnarayanan)
___
`spock` was originally developed by the **Artificial Intelligence Center of Excellence at Fidelity Investments**.

