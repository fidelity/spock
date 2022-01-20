# Utilizing Command Line Overrides

`spock` supports overriding parameter values set from configuration files via the command line. This can be useful for
exploration of parameter values, quick-and-dirty value overrides, or to parse other command-line arguments that would
normally require use of another argparser.

### Automatic Command-Line Argument Generation

`spock` will automatically generate command line arguments for each parameter, unless the `no_cmd_line=True` flag is 
passed to the `SpockBuilder`. Let's look at two of the `@spock` decorated classes from the `tutorial.py` file to 
illustrate how this works in practice:

```python
from enum import Enum
from spock import spock
from typing import List
from typing import Optional
from typing import Tuple

@spock
class DataConfig:
    batch_size: int = 2
    n_samples: int = 8
    cache_path: Optional[str]
    
@spock
class OptimizerConfig:
    lr: float = 0.01
    n_epochs: int = 2
    grad_clip: Optional[float]
```

Given these definitions, `spock` will automatically generate a command-line argument (via an internally maintained 
argparser) for each parameter within each `@spock` decorated class. The syntax follows simple dot notation 
of `--classname.parameter`. Thus, for our sample classes above, `spock` will automatically generate the following 
valid command-line arguments:

```shell
--DataConfig.batch_size *value*
--DataConfig.n_samples *value*
--DataConfig.cache_path *value*
--OptimizerConfig.lr *value*
--OptimizerConfig.n_epochs *value*
--OptimizerConfig.grad_clip *value*
```

None of these command-line arguments are required (i.e. sets `required=False` within the argparser), but a value must
be set via one of the three core mechanisms: (1) a default value (set withing the `@spock` decorated class), (2) the 
configuration file (passed in with the `--config` argument), or (3) the command-line argument (this takes precedence 
over all other methods).

### Overriding Configuration File Values

Using the automatically generated command-line arguments, let's override a few values from our example in `tutorial.py`:

```python
from enum import Enum
from spock import spock
from typing import List
from typing import Optional
from typing import Tuple


class Activation(Enum):
    relu = 'relu'
    gelu = 'gelu'
    tanh = 'tanh'


class Optimizer(Enum):
    sgd = 'SGD'
    adam = 'Adam'


@spock
class ModelConfig:
    n_features: int
    dropout: Optional[List[float]]
    hidden_sizes: Tuple[int, int, int] = (32, 32, 32)
    activation: Activation = 'relu'
    optimizer: Optimizer
    cache_path: Optional[str]


@spock
class DataConfig:
    batch_size: int = 2
    n_samples: int = 8
    cache_path: Optional[str]


@spock
class OptimizerConfig:
    lr: float = 0.01
    n_epochs: int = 2
    grad_clip: Optional[float]


@spock
class SGDConfig(OptimizerConfig):
    weight_decay: float
    momentum: float
    nesterov: bool

```

To run `tutorial.py` we would normally pass just the path to the configuration file as a command line argument:

```bash
$ python tutorial.py --config tutorial.yaml
```

But with command line overrides we can also pass parameter arguments to override their value within the configuration
file:

```bash
$ python tutorial.py --config tutorial.yaml --DataConfig.cache_path /tmp/trash
```

Each parameter can be overridden **ONLY** at the class specific level with the syntax `--classname.parameter`. For
instance, our previous example would only override the `DataConfig.cache_path` and not the `ModelConfig.cache_path` even
though they have the same parameter name (due to the different class names).

```bash
$ python tutorial.py --config tutorial.yaml --DataConfig.cache_path /tmp/trash
```

### Overriding Nested `@spock` Classes

When `@spock` decorated classes are nested within other `@spock` classes they can be overridden still **ONLY** at the 
class specific level. `spock` will internally handle mapping of definitions within a class to nested classes.

For instance, let's create a complex set of nested classes and Enums:

```python
@spock
class BaseDoubleNestedConfig:
    param_base: int = 1


@spock
class FirstDoubleNestedConfig(BaseDoubleNestedConfig):
    h_factor: float = 0.95
    v_factor: float = 0.95


@spock
class SecondDoubleNestedConfig(BaseDoubleNestedConfig):
    morph_param: float = 0.1


class DoubleNestedEnum(Enum):
    first = FirstDoubleNestedConfig
    second = SecondDoubleNestedConfig


@spock
class SingleNestedConfig:
    double_nested_config: DoubleNestedEnum = SecondDoubleNestedConfig()

```

To override the `morph_param` of the `SecondDoubleNestedConfig` class we would use the following argument at the 
command line, `--SecondDoubleNestedConfig.morph_param MY_VALUE`, even though the use of the `SecondDoubleNestedConfig` 
class is nested within another `@spock` decorated class, `SingleNestedConfig`. `spock` knows how to map these nested 
classes and handles all of that internally. Another example, we want to change `double_nested_config` within the 
`SingleNestedConfig` class and then override the `h_factor` parameter within the `FirstDoubleNestedConfig` class. Here,
we would use `--SingleNestedConfig.double_nested_config FirstDoubleNestedConfig` and 
`FirstDoubleNestedConfig.h_factor MY_VALUE`. Notice how you don't need to reference the nesting of the classes, as this
could get very verbose, but simply reference the value within the class only.


### Overriding List/Tuple of Repeated `@spock` Classes 

For `List` of Repeated `@spock` Classes the syntax is slightly different to allow for the repeated nature of the type.
Given the below example code:

```python
from spock import spock
from typing import List


@spock
class NestedListStuff:
    one: int
    two: str

@spock
class TypeConfig:
    nested_list: List[NestedListStuff] # To Set Default Value append '= NestedListStuff'
```

With YAML definitions:

```yaml
# Nested List configuration
nested_list: NestedListStuff
NestedListStuff:
    - one: 10
      two: hello
    - one: 20
      two: bye
```

We could override the parameters like so (note that the len must match the defined length from the YAML):

```bash
$ python tutorial.py --config tutorial.yaml --TypeConfig.nested_list.NestedListStuff.one [1,2] \
--TypeConfig.nested_list.NestedListStuff.two ['ciao','ciao']
```

### Spock As a Drop In Replacement For Argparser

`spock` can easily be used as a drop in replacement for argparser. This means that all parameter definitions as 
required to come in from the command line or from setting defaults within the `@spock` decorated classes. Simply do not 
pass a `-c` or`--config` argument at the command line and instead pass in values to all of the automatically generated 
cmd-line arguments. See more information [here](https://fidelity.github.io/spock/docs/ArgParser-Replacement/).