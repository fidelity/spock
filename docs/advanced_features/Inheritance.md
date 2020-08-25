# Inheritance

`spock` supports class inheritance between different defined `spock` classes. This allows you to build complex 
configurations derived from a common base class or classes.

### Defining an Inherited spock Class

Back to our example. We have implemented two different optimizers to train our neural network. In its current state
we have overlooked the fact that the two different optimizers share a set of common parameters but each also has a 
set of specific parameters. Instead of defining redundant parameter definitions let's use `spock` inheritance.

We create a new `spock` class that inherits from another `spock` class. This functions just like traditional inheritance
where the child will inherit the parameter definitions from the parent class.

Editing our definition in: `tutorial.py`

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
    hidden_sizes: Tuple[int] = (32, 32, 32)
    activation: Activation = 'relu'
    optimizer: Optimizer


@spock
class DataConfig:
    batch_size: int = 2
    n_samples: int = 8


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

Editing our configuration file: `tutorial.yaml`

```yaml
################
# tutorial.yaml
################
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

### Using an Inherited spock Class

Let's use our inherited class to use the SGD optimizer with the defined parameter on our basic neural network: 
`tutorial.py`

```python
import torch
from .basic_nn import BasicNet


def train(x_data, y_data, model, model_config, data_config, optimizer_config):
    if model_config.optimizer == 'SGD':
        optimizer = torch.optim.SGD(model.parameters(), lr=optimizer_config.lr, momentum=optimizer_config.momentum,
                                    nesterov=optimizer_config.nesterov)
    elif model_config.optimizer == 'Adam':
        optimizer = torch.optim.Adam(model.parameters(), lr=optimizer_config.lr)
    else:
        raise ValueError(f'Optimizer choice {optimizer_config.optimizer} not available')
    n_steps_per_epoch = data_config.n_samples % data_config.batch_size
    for epoch in range(optimizer_config.n_epochs):
        for i in range(n_steps_per_epoch):
            # Ugly data slicing for simplicity
            x_batch = x_data[i * n_steps_per_epoch:(i + 1) * n_steps_per_epoch, ]
            y_batch = y_data[i * n_steps_per_epoch:(i + 1) * n_steps_per_epoch, ]
            optimizer.zero_grad()
            output = model(x_batch)
            loss = torch.nn.CrossEntropyLoss(output, y_batch)
            loss.backward()
            if optimizer_config.grad_clip:
                torch.nn.utils.clip_grad_value(model.parameters(), optimizer_config.grad_clip)
            optimizer.step()
        print(f'Finished Epoch {epoch+1}')


def main():
    # A simple description
    description = 'spock Advanced Tutorial'
    # Build out the parser by passing in Spock config objects as *args after description
    config = ConfigArgBuilder(ModelConfig, DataConfig, SGDConfig, desc=description).generate()
    # Instantiate our neural net using
    basic_nn = BasicNet(model_config=config.ModelConfig)
    # Make some random data (BxH): H has dim of features in
    x_data = torch.rand(config.DataConfig.n_samples, config.ModelConfig.n_features)
    y_data = torch.randint(0, 3, (config.DataConfig.n_samples,))
    # Run some training
    train(x_data, y_data, basic_nn, config.ModelConfig, config.DataConfig, config.SGDConfig)
```