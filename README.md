[![Spock](https://raw.githubusercontent.com/fidelity/spock/master/resources/images/logo.png)](https://fidelity.github.io/spock/)
> Managing complex configurations any other way would be highly illogical...

[![License](https://img.shields.io/badge/License-Apache%202.0-9cf)](https://opensource.org/licenses/Apache-2.0)
[![Python](https://img.shields.io/badge/python-3.6+-informational.svg)]()
[![PyPI version](https://badge.fury.io/py/spock-config.svg)](https://badge.fury.io/py/spock-config)
![Tests](https://github.com/fidelity/spock/workflows/pytest/badge.svg)
![Docs](https://github.com/fidelity/spock/workflows/docs/badge.svg)

## About

`spock` is a framework that helps manage complex parameter configurations during research and development of Python 
applications. `spock` lets you focus on the code you need to write instead of re-implementing boilerplate code like 
creating ArgParsers, reading configuration files, implementing traceability etc.

In short, `spock` configurations are defined by simple and familiar class-based structures. This allows `spock` to 
support inheritance, read from multiple markdown formats, and allow hierarchical configuration by composition.

## Quick Install

Requires Python 3.6+

```bash
pip install spock-config
```

## Version(s)

All prior versions are available on PyPi. If legacy API and backend support is needed please install a pre v2.0.0+ 
version. We recommend refactoring your code to the new API and backend instead as legacy versions will be missing 
recent features, bugfixes, and hotfixes.

* v2.0.0+: Dropped support for legacy backend and API semantics
* v1.1.0-v1.2.1: New API with support for legacy backend and legacy API semantics
* v1.0.0: Legacy API and backend 

## News

See [Releases](https://github.com/fidelity/spock/releases) for more information.

#### March  18th, 2021

* Support for Google docstring style annotation of `spock` class (and Enums) and attributes
* Added in ability to print docstring annotated help information to command line with `--help` argument

#### March 1st, 2021

* Removed legacy backend and API (dataclasses and custom typed interface)
* Updated markdown save call to support advanced types so that saved configurations are now valid `spock` config 
  input files
* Changed tuples to support length restrictions

## Documentation

Current documentation and more information can be found [here](https://fidelity.github.io/spock/).

Example `spock` usage is located [here](https://github.com/fidelity/spock/blob/master/examples).

## Key Features

* Simple Declaration: Type checked parameters are defined within a `@spock` decorated class. Supports required/optional 
and automatic defaults.
* Easily Managed Parameter Groups: Each class automatically generates its own object within a single namespace.
* Parameter Inheritance: Classes support inheritance allowing for complex configurations derived from a common base 
set of parameters.
* Complex Types: Nested Lists/Tuples, List/Tuples of Enum of `@spock` classes, List of repeated `@spock` classes
* Multiple Configuration File Types: Configurations are specified from YAML, TOML, or JSON files.
* Hierarchical Configuration: Compose from multiple configuration files via simple include statements.
* Command-Line Overrides: Quickly experiment by overriding a value with automatically generated command line arguments.
* Immutable: All classes are *frozen* preventing any misuse or accidental overwrites.
* Tractability and Reproducibility: Save runtime parameter configuration to YAML, TOML, or JSON with a single chained 
  command (with extra runtime info such as Git info, Python version, machine FQDN, etc). The saved markdown file can be
  used as the configuration input to reproduce prior runtime configurations.

#### Main Contributors

[Nicholas Cilfone](https://github.com/ncilfone), [Siddharth Narayanan](https://github.com/sidnarayanan)
___
`spock` is developed and maintained by the **Artificial Intelligence Center of Excellence at Fidelity Investments**.

