# Utilizing Command Line Overrides

`spock` supports overriding parameter values set from configuration files via the command line. This can be useful for
exploration of parameter values, quick-and-dirty value overrides, or to parse other command-line arguments that would
normally require use of another argparser.

### Automatic Command-Line Argument Generation

`spock` will automatically generate command line arguments for each parameter, unless the `no_cmd_line=True` flag is 
passed to the `ConfigArgBuilder`. Let's look at two of the `@spock` decorated classes from the `tutorial.py` file to 
illustrate how this works in practice:

```python
from enum import Enum
from spock.args import SavePath
from spock.config import spock
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
from spock.args import SavePath
from spock.config import spock
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
    save_path: SavePath
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

### Overriding List/Tuple of Repeated `@spock` Classes 

For `List` of Repeated `@spock` Classes the syntax is slightly different to allow for the repeated nature of the type.
Given the below example code:

```python
from spock.config import spock
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