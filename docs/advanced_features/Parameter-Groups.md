# Parameter Groups

Since `spock` manages complex configurations via a class based solution we can define and decorate multiple classes 
with `@spock_config`. Each class gets created as a separate class object within the `spock` namespace object.

### Building spock Parameter Groups

Let's go back to our example. Say we need to add a few more parameters to our code. We could just keep adding them to 
the single defined class, but this would lead to a *'mega'* class that has parameters for many different parts of your 
code. Instead, we will define two new `spock` classes for our new parameters and begin to organize them by 
functionality.

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


@spock_config
class DataConfig:
    batch_size: IntArg = 2
    n_samples: IntArg = 8


@spock_config
class OptimizerConfig:
    lr: FloatArg = 0.01
    n_epochs: IntArg = 2
    grad_clip: FloatOptArg
```

Now we have three separate `spock` classes that we need to generate the namespace object from. Simply add the new 
classes to `*args` in the `ConfigArgBuilder`. Editing `tutorial.py`:

```python
from spock.builder import ConfigArgBuilder

def main():
    # A simple description
    description = 'spock Advanced Tutorial'
    # Build out the parser by passing in Spock config objects as *args after description
    config = ConfigArgBuilder(ModelConfig, DataConfig, OptimizerConfig, desc=description).generate()
    # One can now access the Spock config object by class name with the returned namespace
    # For instance...
    print(config.ModelConfig)
    print(config.OptimizerConfig)
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
```

### Adding More Code

Let's add a bit more functionality to our code that uses our new parameters by running a 'basic training loop' (this is 
kept very simple for illustrative purposes, hence the simple data slicing) on our basic neural network: `tutorial.py` 

```python
import torch
from .basic_nn import BasicNet


def train(x_data, y_data, model, model_config, data_config, optimizer_config):
    if model_config.optimizer == 'SGD':
        optimizer = torch.optim.SGD(model.parameters(), lr=optimizer_config.lr)
    elif model_config.optimizer == 'Adam':
        optimizer = torch.optim.Adam(model.parameters(), lr=optimizer_config.lr)
    else:
        raise ValueError(f'Optimizer choice {optimizer_config.optimizer} not available')
    n_steps_per_epoch = data_config.n_samples % data_config.batch_size
    for epoch in range(optimizer_config.n_epochs):
        for i in range(n_steps_per_epoch):
            # Ugly data slicing for simplicity
            x_batch = x_data[i*n_steps_per_epoch:(i+1)*n_steps_per_epoch,]
            y_batch = y_data[i*n_steps_per_epoch:(i+1)*n_steps_per_epoch,]
            optimizer.zero_grad()
            output = model(x_batch)
            loss = torch.nn.CrossEntropyLoss(output, y_batch)
            loss.backward()
            if optimizer_config.grad_clip:
                torch.nn.utils.clip_grad_value(model.parameters(), optimizer_config.grad_clip)
            optimizer.step()
                

def main():
    # A simple description
    description = 'spock Advanced Tutorial'
    # Build out the parser by passing in Spock config objects as *args after description
    config = ConfigArgBuilder(ModelConfig, DataConfig, OptimizerConfig, desc=description).generate()
    # Instantiate our neural net using
    basic_nn = BasicNet(model_config=config.ModelConfig)
    # Make some random data (BxH): H has dim of features in
    x_data = torch.rand(config.DataConfig.n_samples, config.ModelConfig.n_features)
    y_data = torch.randint(0, 3, (config.DataConig.n_samples,))
    # Run some training
    train(x_data, y_data, basic_nn, config.ModelConfig, config.DataConfig, config.OptimizerConfig) 
```