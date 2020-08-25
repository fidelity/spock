# Define

`spock` manages complex configurations via a class based solution. All parameters are defined in a class or 
multiple classes decorated with `@spock_config`. Parameters are defined with `spock` types that are checked at run time.
Once built, all parameters can be found within an automatically generated namespace object that contains each class 
that can be accessed with the `spock_config` class name.

All examples can be found [here](https://github.com/fidelity/spock/blob/master/examples).

### Supported Parameter Types

`spock` supports the following argument types:

| Python Base Type | `spock` Type | Optional `spock` Type | Description |
|------------------|--------------|-----------------------|-------------|
| bool | BoolArg | N/A | Basic boolean parameter (e.g. True) |
| float | FloatArg | FloatOptArg | Basic float type parameter (e.g. 10.2) |
| int | IntArg | IntOptArg | Basic integer type parameter (e.g. 2) |
| str | StrArg | StrOptArg | Basic string type parameter (e.g. 'foo') |
| list | ListArg | ListOptArg | Basic list type parameter of base types such as int, float, etc. (e.g. [10.0, 2.0]) |
| tuple | TupleArg | TupleOptArg | Basic tuple type parameter of base types such as int, float, etc. (e.g. (10, 2)) |
| N/A | ChoiceArg | N/A | Parameter that must be from a defined set of values of base types such as int, float, etc. |

### Defining A spock Class

Let's start building out an example (a simple neural net in PyTorch) that we will continue to use within the tutorial: 
`tutorial.py`

Here we import the basic units of functionality from `spock`. We define our class using the `@spock_config` 
decorator and define our parameters with supported argument types from `spock.args`. Parameters are defined within 
the class by using the format `parameter: type`.

```python
from spock.args import *
from spock.config import spock_config

@spock_config
class ModelConfig:
    n_features: IntArg
    dropout: ListArg[float]
    hidden_sizes: TupleArg[int]
    activation: ChoiceArg(choice_set=['relu', 'gelu', 'tanh'])
```

### Using spock Parameters: Writing More Code

In another file let's write our simple neural network code: `basic_nn.py`

Notice that even before we've built and linked all of the related `spock` components together we are referencing the 
parameters we have defined in our `spock` class. Below we are passing in the `ModelConfig` class as a parameter 
`model_config` to the `__init__` function where we can then access the parameters with `.` notation. We could have 
also passed in individual parameters instead if that is the preferred syntax.

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
        self.dropout_1 = nn.Dropout(model_config.dropout[0])
        self.dropout_2 = nn.Dropout(model_config.dropout[1])
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
        x = self.dropout_1(x)
        # Layer 2
        # Linear
        x = self.layer_2(x)
        # Activation
        x = self.use_act(x)
        # Dropout
        x = self.dropout_2(x)
        # Layer 3
        # Linear
        x = self.layer_3(x)
        # Softmax
        output = self.softmax(x)
        return output
```
