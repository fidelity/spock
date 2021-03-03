# Quick Start

*Updated for the new and simpler API!*

*New API is 100% backwards compatible with existing code!*

This is a quick and dirty guide to getting up and running with `spock`. Read the 
[Basic Tutorial](basic_tutorial/About.md) as a simple guide and then explore more
[Advanced Features](advanced_features/About.md) for in-depth usage.

All examples can be found [here](https://github.com/fidelity/spock/blob/master/examples).

Legacy documentation for the old API (pre v2.0) can be 
found [here](https://github.com/fidelity/spock/blob/master/docs/legacy)

### TL;DR
1. Import the necessary components from `spock`
2. Create a basic Python class, decorate it with `@spock`
3. Define your parameters in the class (using the typing module if needed)
4. Use the defined parameters in your code 
5. Create a configuration file
6. Run your code with --config /path/to/config

### Simple Example

A basic python script, `simple.py`.

First we import the necessary functionality from `spock`. We define our class using the `@spock` 
decorator and our parameters with supported argument types from `typing`.

```python
from spock.builder import ConfigArgBuilder
from spock.config import spock
from typing import List

@spock
class BasicConfig:
    parameter: bool
    fancy_parameter: float
    fancier_parameter: float
    most_fancy_parameter: List[int]
```

Next let's add two simple function(s) to our script. They both so the same thing but use our parameters in two different
ways.

```python
def add_namespace(config):
    # Lets just do some basic algebra here
    val_sum = sum([(config.fancy_parameter * val) + config.fancier_parameter for val in config.most_fancy_parameter])
    # If the boolean is true let's round
    if config.parameter:
        val_sum = round(val_sum)
    return val_sum

def add_by_parameter(multiply_param, list_vals, add_param, tf_round):
    # Lets just do some basic algebra here
    val_sum = sum([(multiply_param * val) + add_param for val in list_vals])
    # If the boolean is true let's round
    if tf_round:
        val_sum = round(val_sum)
    return val_sum
```

Now, we build out the parameter objects by passing in the `spock` objects (as `*args`) to the `ConfigArgBuilder` 
and chain call the `generate` method. The returned namespace object contains the defined classes named with the given
`spock` class name. We then can pass the whole object to our first function or specific parameters to our
second function.

```python
def main():
    # Chain the generate function to the class call
    config = ConfigArgBuilder(BasicConfig).generate()
    # One can now access the Spock config object by class name with the returned namespace
    print(config.BasicConfig.parameter)
    # And pass the namespace to our first function
    val_sum_namespace = add_namespace(config.BasicConfig)
    print(val_sum_namespace)
    # Or pass by parameter
    val_sum_parameter = add_by_parameter(config.BasicConfig.fancy_parameter, config.BasicConfig.most_fancy_parameter, 
                                         config.BasicConfig.fancier_parameter, config.BasicConfig.parameter)
    print(val_sum_parameter)


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

Finally, we would then pass the path to the configuration file to the command line (-c or --config):

```bash
$ python simple.py -c simple.yaml
```
