# Evolve

`spock` provides evolve functionality similar to the underlying attrs library 
([attrs.evolve](https://www.attrs.org/en/stable/api.html#attrs.evolve). `evolve()` creates a new 
`Spockspace` instance based on differences between the underlying declared state and any passed in instantiated 
`@spock` decorated classes.

### Using Evolve

The `evolve()` method is available form the `SpockBuilder` object. `evolve()` takes as input a variable number of 
instantiated `@spock` decorated classes, evolves the underlying `attrs` objects to incorporate the changes between
the instantiated classes and the underlying classes, and returns the new `Spockspace` object.

For instance:

```python

from enum import Enum
from spock import spock
from spock import SpockBuilder


class Choices(Enum):
    choice1 = 1
    choice2 = 2


@spock
class Configs4OneThing:
    the_choice: Choices = Choices.choice1
    param: int = 10


def main():
    evolve_class = Configs4OneThing(param=20)
    evolved_configs = SpockBuilder(Configs4OneThing, desc='Evolve Example').evolve(evolve_class)
    print(evolved_configs)
    
if __name__ == '__main__':
    main()
```

This would evolve the value of `param` to be 20 instead of the default value of 10. The print output would be:

```shell
Configs4OneThing: !!python/object:spock.backend.config.Configs4OneThing
  param: 20
  the_choice: 1
```

### Maintaining CLI and Python API Configuration Parity

`evolve` is quite useful when writing python code/libraries/packages that maintain both a CLI and a Python API. With
`spock` it is simple to maintain parity between the CLI and the Python API by leveraging the `evolve` functionality.

For instance, let's say we have two different `@spock` decorated configs we want to use for both the CLI and the Python
API:

```python
# config.py

from enum import Enum
from spock import spock
from typing import List


class Choices(Enum):
    choice1 = 1
    choice2 = 2


@spock
class Configs4OneThing:
    the_choice: Choices = Choices.choice1
    param: int = 10


@spock
class Configs4AnotherThing:
    some_list: List[float] = [10.0, 20.0]
    flag: bool = False

    
# List of all configs
ALL_CONFIGS = [
    Configs4OneThing,
    Configs4AnotherThing
]

```

With these `@spock` decorated classes it's easy to write a parent class that contains shared functionality (i.e. run a 
model, do some work, etc.) and two child classes that handle the slightly different syntax needed for the underlying 
`SpockBuilder` for the CLI and for the Python API. 

For the CLI, we use the common `spock` syntax that has been shown in previous examples/tutorial. Call the builder 
object and pass in all `@spock` decorated classes. Keep the `no_cmd_line` flag set to `False` which will automatically 
generate a command line argument for each defined parameter and provide support for the `--config` argument to pass
in values via a markdown file(s). We then call `generate` on the builder to return the `Spockspace`.

For the Python API, we modify the `spock` syntax slightly. We still pass in all `@spock` decorated classes but set 
the `no_cmd_line` flag to `True` to prevent command line arguments (and markdown configuration). We then call `evolve`
and pass in any user instantiated `@spock` decorated classes to evolve the underlying object and return a new
`Spockspace` object that has been evolved based on the differences between the values within instantiated classes and
the values in the underlying object.

Example code is given below:

```python
# code.py
from abc import ABC
from spock import SpockBuilder
from config import ALL_CONFIGS


class Base(ABC):
    def run(self):
        # do something with self.configs
        ...

    
class OurAPI(Base):
    def __init__(self,
                 config_4_one_thing: Configs4OneThing = Configs4OneThing(), 
                 config_4_another_thing: Configs4AnotherThing = Configs4AnotherThing()
                 ):
        # Call the SpockBuilder with the no_cmd_line flag set to True 
        # This will prevent command-line arguments from being generated
        # Additionally call evolve on the builder with the custom/default Configs4OneThing & Configs4AnotherThing
        # objects
        self.configs = SpockBuilder(*ALL_CONFIGS, no_cmd_line=True, configs=[]).evolve(
            config_4_one_thing, config_4_another_thing
        )


class OurCLI(Base):
    def __init__(self):
        # Call the SpockBuilder with the no_cmd_line flag set to False (default value)
        # This will automatically provide command-line arguments for all of the @spock decorated
        # config classes
        self.configs = SpockBuilder(*ALL_CONFIGS).generate()
    

def cli_shim():
    """Shim function for setup.py entry_points

    Returns:
        None
    """
    cli_runner = OurCLI().run()
```
