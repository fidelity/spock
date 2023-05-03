# Quick Start

This is a quick and dirty guide to getting up and running with `spock`. Read the 
[Basic Tutorial](basics/About.md) as a simple guide and then explore more
[Advanced Features](advanced_features/About.md) for in-depth usage.

All examples can be found [here](https://github.com/fidelity/spock/blob/master/examples).

### TL;DR
1. Import the necessary components from `spock`
2. Create a basic Python class, decorate it with `@spock`
3. Define your parameters in the class (using the typing module if needed)
4. Use the defined parameters in your code 
5. Create a configuration file
6. Run your code with --config /path/to/config

### Simple Example

A basic python script, `simple.py`.

First we import the necessary functionality from `spock`. We define our class using the `@spock` decorator and our 
parameters with supported argument types from the `typing` library. Lastly, we write simple Google style 
docstrings to provide command line `--help` information.

```python
from spock import SpockBuilder
from spock import spock
from typing import List

@spock
class BasicConfig:
    """Basic spock configuration for example purposes

    Attributes:
        parameter: simple boolean that flags rounding
        fancy_parameter: parameter that multiplies a value
        fancier_parameter: parameter that gets added to product of val and fancy_parameter
        most_fancy_parameter: values to apply basic algebra to

    """
    parameter: bool
    fancy_parameter: float
    fancier_parameter: float
    most_fancy_parameter: List[int]
```

Next let's add a simple function to our script. The function takes as an argument a `Spockspace` (in this case we type
hint within Python so IDEs can autocomplete), thus we access our defined parameters from the class definition above via 
dot notation (just like `Namespaces` as the output from argparsers).

```python
def add_values(config: BasicConfig):
    # Lets just do some basic algebra here
    val_sum = sum([(config.fancy_parameter * val) + config.fancier_parameter for val in config.most_fancy_parameter])
    # If the boolean is true let's round
    if config.parameter:
        val_sum = round(val_sum)
    return val_sum
```

Now, we build out the parameter objects by passing in the `spock` objects (as `*args`) to the `SpockBuilder` 
and chain call the `generate` method. The returned object contains the defined classes named with the given
`spock` class name which we call a `Spockspace`. We then simply pass `config.BasicConfig` to our function.

```python
def main():
    # Chain the generate function to the class call
    config = SpockBuilder(BasicConfig, desc='Quick start example').generate()
    # One can now access the Spock config object by class name with the returned namespace
    print(config.BasicConfig.parameter)
    # And pass the namespace to our first function
    val_sum_namespace = add_values(config.BasicConfig)
    print(val_sum_namespace)


if __name__ == '__main__':
    main()
```

Next let's create a simple configuration file that sets the values of our parameters. Let's make a YAML file (you can 
also use TOML or JSON), `simple.yaml`:

```yaml
# Parameters
parameter: true
fancy_parameter: 8.8
fancier_parameter: 64.64
most_fancy_parameter: [768, 768, 512, 128]
```

Finally, we would run our script and pass the path to the configuration file to the command line (`-c` or `--config`):

```shell
python simple.py -c simple.yaml
```

To get help for our `spock` class and defined parameters:

```shell
python simple.py --help
```

```shell
usage: ~/Documents/git_repos/open_source/spock/examples/quick-start/simple.py -c [--config] config1 [config2, config3, ...]

Quick start example

configuration(s):

  BasicConfig (Basic spock configuration for example purposes)
    parameter               bool         simple boolean that flags rounding (default: False)
    fancy_parameter         float        parameter that multiplies a value 
    fancier_parameter       float        parameter that gets added to product of val and fancy_parameter 
    most_fancy_parameter    List[int]    values to apply basic algebra to 
```

### Spock As a Drop In Replacement For Argparser

`spock` can easily be used as a drop in replacement for argparser. 
See the docs/example [here](https://fidelity.github.io/spock/ArgParser-Replacement/).
