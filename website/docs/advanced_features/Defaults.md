# Defaults

`spock` allows you to set defaults for parameters that are either not set from a configuration file or you no longer
need to set (maybe you've finally settled on a standard or would like to fall back to defaults if the user does not
know the correct/best parameter to choose). This is done in the `spock` class definition.


### Setting Defaults

Say we want defaults for the hidden layer sizes and the activation function as well as add a new parameter with a 
default value.

Default values are simply set with the `=` operator

Let's modify the definition in: `tutorial.py`

```python
from enum import Enum
from spock import spock
from typing import List
from typing import Optional
from typing import Tuple

class Activation(Enum):
    relu = 'relu'
    gelu = 'gelu'
    tanh = 'tanh'


@spock
class ModelConfig:
    lr: float = 0.01
    n_features: int
    dropout: List[float]
    hidden_sizes: Tuple[int, int, int] = (32, 32, 32)
    activation: Activation = 'relu'
```

We added a new parameter `lr` that has a default value of `0.01`, and set defaults for `hidden_sizes` and `activation`.
These values will be used if no values are specified in the configuration file and prevent `spock` from raising an
Exception for required parameters.
