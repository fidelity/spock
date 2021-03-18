# Define

`spock` manages complex configurations via a class based solution. All parameters are defined in a class or 
multiple classes decorated using the `@spock` decorator. Parameters are defined with base types or those defined within
the `typing` module and are type checked at run time. Once built, all parameters can be found within an automatically 
generated namespace object that contains each class that can be accessed with the given `@spock` class name.

All examples can be found [here](https://github.com/fidelity/spock/blob/master/examples).

### Supported Parameter Types

#### Basic Types
`spock` supports the following basic argument types (note `List`, `Tuple`, and `Optional` are defined in the `typing` 
standard library while `Enum` is within the `enum` standard library):

| Python Base or Typing Type (Required) | Optional Type | Description |
|----------------------------|---------------|-------------|
| bool | Optional[bool] | Basic boolean parameter (e.g. True) |
| float | Optional[float] | Basic float type parameter (e.g. 10.2) |
| int | Optional[int] | Basic integer type parameter (e.g. 2) |
| str | Optional[str] | Basic string type parameter (e.g. 'foo') |
| List[type] | Optional[List[type]] | Basic list type parameter of base types such as int, float, etc. (e.g. [10.0, 2.0]) |
| Tuple[type] | Optional[Tuple[type]] | Basic tuple type parameter of base types such as int, float, etc. (e.g. (10, 2)) |
| Enum | Optional[Enum] | Parameter that must be from a defined set of values of base types such as int, float, etc. |

Parameters that are specified without the `Optional[]` type will be considered **REQUIRED** and therefore will raise an
Exception if not value is specified. 

#### Advanced Types
`spock` supports more than just basic types. More information can be found in 
the [Advanced Types](../advanced_features/Advanced-Types.md) section.

### Defining a spock Class

Let's start building out an example (a simple neural net in PyTorch) that we will continue to use within the tutorial: 
`tutorial.py`

Here we import the basic units of functionality from `spock`. We define our class using the `@spock` 
decorator and define our parameters with supported argument types. Parameters are defined within 
the class by using the format `parameter: type`. Note that to create a parameter that is required to be within a 
specified set one must first define an `Enum` class object with the given options. The `Enum` class is then passed to
your `spock` class just like other types.

```python
from enum import Enum
from spock.config import spock
from typing import List
from typing import Tuple


class Activation(Enum):
    relu = 'relu'
    gelu = 'gelu'
    tanh = 'tanh'


@spock
class ModelConfig:
    n_features: int
    dropout: List[float]
    hidden_sizes: Tuple[int]
    activation: Activation
```

### Adding Help Information

`spock` uses the [Google](https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings) docstring style
format to support adding help information to classes and Enums. `spock` will look for the first contiguous line of text
within the docstring as the class help information. `spock` looks within the `Attributes` section of the docstring
for help information for each parameter. Modifying the above code to include help information:

```python
from enum import Enum
from spock.args import SavePath
from spock.config import spock
from typing import List
from typing import Tuple

class Activation(Enum):
    """Options for activation functions

    Attributes:
        relu: relu activation
        gelu: gelu activation
        tanh: tanh activation
    """
    relu = 'relu'
    gelu = 'gelu'
    tanh = 'tanh'


@spock
class ModelConfig:
    """Main model configuration for a basic neural net

    Attributes:
        save_path: spock special keyword -- path to write out spock config state
        n_features: number of data features
        dropout: dropout rate for each layer
        hidden_sizes: hidden size for each layer
        activation: choice from the Activation enum of the activation function to use
    """
    save_path: SavePath
    n_features: int
    dropout: List[float]
    hidden_sizes: Tuple[int]
    activation: Activation
```

If we run our `tutorial.py` script with the `--help` flag:

```bash
$ python tutorial.py --help
```

We should see the help information we added to the docstring(s):

```
usage: /Users/a635179/Documents/git_repos/open_source/spock/examples/tutorial/basic/tutorial.py -c [--config] config1 [config2, config3, ...]

spock Basic Tutorial

configuration(s):

  ModelConfig (Main model configuration for a basic neural net)
    save_path       Optional[SavePath]    spock special keyword -- path to write out spock config state (default: None)
    n_features      int                   number of data features 
    dropout         List[float]           dropout rate for each layer 
    hidden_sizes    Tuple[int]            hidden size for each layer 
    activation      Activation            choice from the Activation enum of the activation function to use 

  Activation (Options for activation functions)
    relu    str    relu activation 
    gelu    str    gelu activation 
    tanh    str    tanh activation 
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
