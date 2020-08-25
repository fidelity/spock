# Defaults

`spock` allows you to set defaults for parameters that are either not set from a configuration file or you no longer
need to set (maybe you've finally settled on a standard or would like to fall back to defaults if the user does not
know the correct/best parameter to choose). This is done in the `spock` class definition.


### Setting Defaults

Say we want defaults for the hidden layer sizes and the activation function as well as add a new parameter with a 
default value.

For basic types (`FloatArg`, `IntArg`, `StrArg`, `BoolArg`) default values are set with the `=` operator. For 
`ListArg` and `TupleArg` types, defaults are set using the `.default()` method. For `ChoiceArg` the default value is set
using the `default` keyword arg.

Let's modify the definition in: `tutorial.py`

```python
from spock.args import *
from spock.config import spock_config

@spock_config
class ModelConfig:
    save_path: SavePathOptArg
    lr: FloatArg = 0.01
    n_features: IntArg
    dropout: ListArg[float]
    hidden_sizes: TupleArg[int] = TupleArg.defaults((32, 32, 32))
    activation: ChoiceArg(choice_set=['relu', 'gelu', 'tanh'], default='relu')
```

We added a new parameter `lr` that has a default value of `0.01`, and set defaults for `hidden_sizes` and `activation`.
These values will be used if no values are specified in the configuration file and prevent `spock` from raising an
exception for required parameters.
