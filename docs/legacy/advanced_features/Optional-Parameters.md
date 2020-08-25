# Optional Parameters

`spock` allows for parameters to be defined as optional. This means that if the parameter value is not set from either 
a configuration file or a default value it will be assigned the `None` value. Optional `spock` parameters are defined
using the optional version of the base type: `FloatOptArg`, `IntOptArg`, `StrOptArg`, `ListOptArg`,`TupleOptArg`.

### Defining Optional spock Parameters

Optional parameters commonly occur in applications with complex behavior (like neural networks). For instance, what if
you want to execute a specific behavior with some parameter(s) if the parameter is defined and if the parameter is not
defined either skip the behavior or so something different. Normally this would require a combination of boolean logic
and parameter definition (which might be useless...). `spock` remedies this with optional parameters.

As an example, let's assume we want to make dropout within our basic neural network optional. Let's modify the 
definition in: `tutorial.py`

```python
@spock_config
class ModelConfig:
    save_path: SavePathOptArg
    lr: FloatArg = 0.01
    n_features: IntArg
    dropout: ListOptArg[float]
    hidden_sizes: TupleArg[int] = TupleArg.defaults((32, 32, 32))
    activation: ChoiceArg(choice_set=['relu', 'gelu', 'tanh'], default='relu')
```

Notice that all we did was change the type from `ListArg` to `ListOptAg`.

Now let's edit our simple neural network code to reflect that dropout is now optional. We have to change the code a bit
to be more modular (but still ugly for demonstration): `basic_nn.py`

```python
import torch.nn as nn

class BasicNet(nn.Module):
    def __init__(self, model_config):
        super(BasicNet, self).__init__()
        # Make a dictionary of activation functions to select from
        self.act_fncs = {'relu': nn.ReLU, 'gelu': nn.GELU, 'tanh': nn.Tanh}
        self.use_act = self.act_fncs.get(model_config.activation)()
        # Define the layers manually (avoiding list comprehension for clarity)
        self.layer_1 = nn.Linear(model_config.n_features, model_config.hidden_sizes[0])
        self.layer_2 = nn.Linear(model_config.hidden_sizes[0], model_config.hidden_sizes[1])
        self.layer_3 = nn.Linear(model_config.hidden_sizes[1], model_config.hidden_sizes[2])
        # Define some dropout layers
        self.dropout = []
        if model_config.dropout is not None:
            self.dropout = [nn.Dropout(val) for val in model_config.dropout]
        # Define the output layer
        self.softmax = nn.Softmax(dim=1)

    def forward(self, x):
        # x is the data input
        # Layer 1
        # Linear
        x = self.layer_1(x)
        # Activation
        x = self.use_act(x)
        # Dropout
        if len(self.dropout) != 0:
            x = self.dropout[0](x)
        # Layer 2
        # Linear
        x = self.layer_2(x)
        # Activation
        x = self.use_act(x)
        # Dropout
        if len(self.dropout) != 0:
            x = self.dropout[1](x)
        # Layer 3
        # Linear
        x = self.layer_3(x)
        # Softmax
        output = self.softmax(x)
        return output
```

### Code Behavior

If we use the same configuration file defined in: `tutorial.yaml`

```yaml
################
# tutorial.yaml
################
# ModelConfig
n_features: 64
dropout: [0.2, 0.1]
hidden_sizes: [32, 32, 16]
activation: relu
```

With this configuration file, the parameter `dropout` is assigned the specified value. Thus our basic neural network 
will have dropout layers between Layer 1, Layer 2, and Layer 3.

However, if we use the following configuration file: `tutorial_no_dropout.yaml`

```yaml
################
# tutorial.yaml
################
# ModelConfig
n_features: 64
hidden_sizes: [32, 32, 16]
activation: relu
```

With this configuration file, the parameter `dropout` is assigned `None`. Thus our based on the logic in our code our 
basic neural network will not have dropout between layers.

This simple example demonstrates the power of `spock` optional parameters. Flow through code can easily be modified by 
simply changing the configuration file.