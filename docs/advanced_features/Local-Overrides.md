# Local Overrides

The class based solution within `spock` provides the ability to override a global parameter value within a local
class context.

### Overriding a Global Value

Let's define two new parameters with the same name but in two different classes that represent where some stuff is 
going to be cached. One for the model and one for some data.

Editing our definition in: `tutorial.py`

```python
from spock.args import *
from spock.config import spock_config


@spock_config
class ModelConfig:
    save_path: SavePathOptArg
    n_features: IntArg
    dropout: ListOptArg[float]
    hidden_sizes: TupleArg[int] = TupleArg.defaults((32, 32, 32))
    activation: ChoiceArg(choice_set=['relu', 'gelu', 'tanh'], default='relu')
    optimizer = ChoiceArg(choice_set=['SGD', 'Adam'])
    cache_path: StrOptArg


@spock_config
class DataConfig:
    batch_size: IntArg = 2
    n_samples: IntArg = 8
    cache_path: StrOptArg


@spock_config
class OptimizerConfig:
    lr: FloatArg = 0.01
    n_epochs: IntArg = 2
    grad_clip: FloatOptArg
    

@spock_config
class SGDConfig(OptimizerConfig):
    weight_decay: FloatArg
    momentum: FloatArg
    nesterov: BoolArg

```

Now, if we edit our configuration file: `tutorial.yaml`

```yaml
################
# tutorial.yaml
################
# Global
cache_path: /tmp/cache/
# Special Key
save_path: /tmp
# ModelConfig
n_features: 64
dropout: [0.2, 0.1]
hidden_sizes: [32, 32, 16]
activation: relu
optimizer: SGD
# DataConfig
batch_size: 2
n_samples: 8
# OptimizerConfig
lr: 0.01
n_epochs: 2
grad_clip: 5.0
# SGD Config
weight_decay: 1E-5
momentum: 0.9
nesterov: true
```

This configuration file would set both parameters to use the `/tmp/cache/` value (i.e. it would set the parameter value 
globally). But what if we want to the data cache to be a different path? We can override the global parameter value with
a local parameter value.

Editing our configuration file: `tutorial.yaml`

```yaml
################
# tutorial.yaml
################
# Global
cache_path: /tmp/cache/
# Special Key
save_path: /tmp
# ModelConfig
n_features: 64
dropout: [0.2, 0.1]
n_hidden: [32, 32, 16]
activation: relu
optimizer: SGD
# DataConfig
batch_size: 2
n_samples: 8
DataConfig:
  cache_path: /home/user/cache/
# OptimizerConfig
lr: 0.01
n_epochs: 2
grad_clip: 5.0
# SGD Config
weight_decay: 1E-5
momentum: 0.9
nesterov: true
```