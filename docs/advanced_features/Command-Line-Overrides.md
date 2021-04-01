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
$ python tutorial.py --config tutorial.yaml --cache_path /tmp/trash
```

Each parameter can be overridden at the global level or the class specific level with the syntax `--name.parameter`. For
instance, our previous example would override any parameters named `cache_path` regardless of what class they are 
defined in. In this case `cache_path` in both `ModelConfig` and `DataConfig`. To override just a class specific value 
we would use the class specific override:

```bash
$ python tutorial.py --config tutorial.yaml --DataConfig.cache_path /tmp/trash
```