# Utilizing Command Line Overrides

`spock` supports overriding parameter values set from configuration files via the command line. This can be useful for
exploration of parameter values or for things like hyperparameter optimization.

### Overriding Configuration File Values

 Let's override a few values from our example in: `tutorial.py`

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
--TypeConfig.nested_list.NestedListStuff.two [ciao,ciao]
```