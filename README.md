<html>
<h1 align="center">
    <a href="https://fidelity.github.io/spock/"><img src="https://raw.githubusercontent.com/fidelity/spock/master/resources/images/logo.png"/></a>
    <h6 align="center">Managing complex configurations any other way would be highly illogical...</h6>
</h1>

<p align="center">
  <a href="https://opensource.org/licenses/Apache-2.0"><img src="https://img.shields.io/badge/License-Apache%202.0-9cf"/></a>
  <a href="https://bestpractices.coreinfrastructure.org/projects/5551"><img src="https://bestpractices.coreinfrastructure.org/projects/5551/badge"/></a>
  <a><img src="https://github.com/fidelity/spock/workflows/pytest/badge.svg?branch=master"/></a>
<a href="https://coveralls.io/github/fidelity/spock?branch=master"><img src="https://coveralls.io/repos/github/fidelity/spock/badge.svg?branch=master"/></a>
  <a><img src="https://github.com/fidelity/spock/workflows/docs/badge.svg"/></a>
</p>

<p align="center">
  <a><img src="https://img.shields.io/badge/python-3.6+-informational.svg"/></a>
  <a href="https://github.com/psf/black"><img src="https://img.shields.io/badge/code%20style-black-000000.svg"/></a>
  <a href="https://badge.fury.io/py/spock-config"><img src="https://badge.fury.io/py/spock-config.svg"/></a>
  <a href="https://pepy.tech/badge/spock-config"><img src="https://static.pepy.tech/personalized-badge/spock-config?period=total&units=international_system&left_color=grey&right_color=orange&left_text=Downloads"/></a>
</p>
  
<h3 align="center">
  <a href="https://fidelity.github.io/spock/Quick-Start">Quick Start</a>
  <span> · </span>
  <a href="https://fidelity.github.io/spock/">Documentation</a>
  <span> · </span>
  <a href="https://github.com/fidelity/spock/blob/master/examples">Examples</a>
  <span> · </span>
  <a href="https://github.com/fidelity/spock/releases">Releases</a>
</h3>
  
</html>

## About

`spock` is a framework that helps users easily define, manage, and use complex parameter configurations within Python 
applications. It lets you focus on the code you need to write instead of re-implementing boilerplate code such as
creating ArgParsers, reading configuration files, handling dependencies, implementing type validation, 
maintaining traceability, etc.

`spock` configurations are normal python classes that are decorated with `@spock`. It supports 
inheritance, dynamic class dependencies, loading/saving configurations from/to multiple markdown formats, automatically 
generating CLI arguments, and hierarchical configuration by composition.

## 💥 Why You Should Use Spock 💥 

* Simple organized parameter definitions (i.e. a single line)
* Type checked (static-eqsue) & frozen parameters (i.e. fail early during long ML training runs)
* Complex parameter dependencies made simple (i.e. `@spock` class with a parameter that is an Enum of other 
`@spock` classes)
* Fully serializable parameter state(s) (i.e. exactly reproduce prior runtime parameter configurations)
* Automatic type checked CLI generation w/o argparser boilerplate (i.e click and/or typer for free!)
* Easily maintain parity between CLIs and Python APIs (i.e. single line changes between CLI and Python API definitions)
* Unified hyper-parameter definitions and interface (i.e. don't write different definitions for Ax or Optuna)

## Key Features

* [Simple Declaration](https://fidelity.github.io/spock/basics/Define): Type checked parameters are 
  defined within a `@spock` decorated class. Supports required/optional and automatic defaults.
* Easily Managed Parameter Groups: Each class automatically generates its own object within a single namespace.
* [Parameter Inheritance](https://fidelity.github.io/spock/advanced_features/Inheritance): Classes support 
  inheritance (w/ lazy evaluation of inheritance/dependencies) allowing for complex configurations derived from 
  a common base set of parameters.
* [Complex Types](https://fidelity.github.io/spock/advanced_features/Advanced-Types/): Nested Lists/Tuples, 
  List/Tuples of Enum of `@spock` classes, List of repeated `@spock` classes
* Multiple Configuration File Types: Configurations are specified from YAML, TOML, or JSON files.
* [Hierarchical Configuration](https://fidelity.github.io/spock/advanced_features/Composition/): Compose from 
  multiple configuration files via simple include statements.
* [Command-Line Overrides](https://fidelity.github.io/spock/advanced_features/Command-Line-Overrides/): Quickly 
  experiment by overriding a value with automatically generated command line arguments.
* Immutable: All classes are *frozen* preventing any misuse or accidental overwrites (to the extent they can be in 
  Python).
* [Tractability and Reproducibility](https://fidelity.github.io/spock/basics/Saving): Save runtime 
  parameter configuration to YAML, TOML, or JSON with a single chained command (with extra runtime info such as Git info, 
  Python version, machine FQDN, etc). The saved markdown file can be used as the configuration input to reproduce 
  prior runtime configurations.
* [Hyper-Parameter Tuner Addon](https://fidelity.github.io/spock/addons/tuner/About): Provides a unified
  interface for defining hyper-parameters (via `@spockTuner` decorator) that supports various tuning/algorithm 
  backends (currently: Optuna, Ax)
* [S3 Addon](https://fidelity.github.io/spock/addons/S3): Automatically detects `s3://` URI(s) and handles loading 
  and saving `spock` configuration files when an active `boto3.Session` is passed in (plus any additional 
  `S3Transfer` configurations)

## Quick Install

The basic install and `[s3]` extension require Python 3.6+ while the `[tune]` extension requires Python 3.7+

| Base | w/ S3 Extension | w/ Hyper-Parameter Tuner |
|------|-----------------|--------------------------|
| `pip install spock-config` | `pip install spock-config[s3]` | `pip install spock-config[tune]` |

## News/Releases

See [Releases](https://github.com/fidelity/spock/releases) for more information.

<html>
<h2 id="features"> 
  Recent Changes
</h2>
</html>

<details>

#### March 11th, 2022
* Added support for simple `typing.Callable` types (WIP: advanced versions)
* Added support for post init hooks that allow for validation on parameters defined within `@spock` decorated classes. 
Additionally, added some common validation check to utils (within, greater than, less than, etc.)
* Updated unit tests to support Python 3.10

#### January 26th, 2022
* Added `evolve` support to the underlying `SpockBuilder` class. This provides functionality similar to the underlying
attrs library ([attrs.evolve](https://www.attrs.org/en/stable/api.html#attrs.evolve)). `evolve()` creates a new 
`Spockspace` instance based on differences between the underlying declared state and any passed in instantiated 
`@spock` decorated classes.

#### January 18th, 2022
* Support for lazy evaluation: (1) inherited classes do not need to be `@spock` decorated, (2) dependencies/references 
between `spock` classes can be lazily handled thus preventing the need for every `@spock` decorated classes to be 
passed into `*args` within the main `SpockBuilder` API
* Updated main API interface for better top-level imports (backwards compatible): `ConfigArgBuilder`->`SpockBuilder`
* Added stubs to the underlying decorator that should help with type hinting in VSCode (pylance/pyright)

</details>

## Original Implementation

`spock` was originally developed by the **Artificial Intelligence Center of Excellence at Fidelity Investments** by [Nicholas Cilfone](https://github.com/ncilfone) and [Siddharth Narayanan](https://github.com/sidnarayanan)


