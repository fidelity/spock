[![Spock](https://raw.githubusercontent.com/fidelity/spock/master/resources/images/logo.png)](https://fidelity.github.io/spock/)
> Managing complex configurations any other way would be highly illogical...

[![License](https://img.shields.io/badge/License-Apache%202.0-9cf)](https://opensource.org/licenses/Apache-2.0)
[![Python](https://img.shields.io/badge/python-3.6+-informational.svg)]()
[![PyPI version](https://badge.fury.io/py/spock-config.svg)](https://badge.fury.io/py/spock-config)
![Tests](https://github.com/fidelity/spock/workflows/pytest/badge.svg)

## About

`spock` is a framework that helps manage complex parameter configurations during research and development of Python 
applications. `spock` let's you focus on the code you need to write instead of re-implementing boilerplate code like 
creating ArgParsers, reading configuration files, implementing traceability etc.

In short, `spock` configurations are defined by simple and familiar class-based structures. This allows `spock` to 
support inheritance, read from multiple markdown formats, and allow hierarchical configuration by composition.

## Quick Install

Supports Python 3.6+

```bash
pip install spock-config
```

## Documentation

Current documentation and more information can be found [here](https://fidelity.github.io/spock/).

Example `spock` usage is located [here](https://github.com/fidelity/spock/blob/master/examples).

## Key Features

* Simple Declaration: Type checked parameters are defined within a `@spock` decorated class. Supports required/optional 
and automatic defaults.
* Easily Managed Parameter Groups: Each class automatically generates its own object within a single namespace.
* Parameter Inheritance: Classes support inheritance allowing for complex configurations derived from a common base 
set of parameters.
* Multiple Configuration File Types: Configurations are specified from YAML, TOML, or JSON files.
* Hierarchical Configuration: Composed from multiple configuration files via simple include statements.
* Command-Line Overrides: Quickly experiment by overriding a value with automatically generated command line arguments
* Immutable: All classes are *frozen* preventing any misuse or accidental overwrites.
* Tractability and Reproducibility: Save currently running parameter configuration with a single chained command. 

#### Main Contributors

[Nicholas Cilfone](https://github.com/ncilfone), [Siddharth Narayanan](https://github.com/sidnarayanan)
___
`spock` is developed and maintained by the **Artificial Intelligence Center of Excellence at Fidelity Investments**.

