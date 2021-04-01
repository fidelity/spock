# Build

Once all of the parameters we need have been defined in our `spock` class and we've written some code to use those 
parameters we need to generate the namespace object. 

The namespace object is the heart of `spock` and is how one accesses all of the defined parameters. The generation of 
the namespace should happen at the highest level of code, preferably in the `main` guard protected call or `main` 
function call. This allows the namespace object, the `spock` classes, or the individual parameters to be passed to
lower level functionality.

### Generate the spock Namespace Object

So let's continue in: `tutorial.py`

Recall that we defined our `spock` class as such:

```python
class Activation(Enum):
    relu = 'relu'
    gelu = 'gelu'
    tanh = 'tanh'


@spock
class ModelConfig:
    n_features: int
    dropout: List[float]
    hidden_sizes: Tuple[int, int, int]
    activation: Activation
```

To generate the namespace object, import the `ConfigArgBuilder` class, pass in your `@spock` classes as `*args`, 
add an optional description, and then chain call the `generate()` method. Each `spock` class is defined in the 
namespace object given by the class name.

```python
from spock.builder import ConfigArgBuilder

def main():
    # A simple description
    description = 'spock Tutorial'
    # Build out the parser by passing in Spock config objects as *args after description
    config = ConfigArgBuilder(ModelConfig, desc=description).generate()
    # One can now access the Spock config object by class name with the returned namespace
    # For instance...
    print(config.ModelConfig)


if __name__ == '__main__':
    main()
```

### Using spock Parameters

Our simple neural network code referenced some `spock` defined parameters. So let's link them together correctly and 
test our model. We will pass the full `spock` class from the generated namespace object to our `nn.module` class.

Continuing in: `tutorial.py`

```python
import torch
from .basic_nn import BasicNet

def main():
    # A simple description
    description = 'spock Tutorial'
    # Build out the parser by passing in Spock config objects as *args after description
    config = ConfigArgBuilder(ModelConfig, desc=description).generate()
    # Instantiate our neural net using
    basic_nn = BasicNet(model_config=config.ModelConfig)
    # Make some random data (BxH): H has dim of features in
    test_data = torch.rand(10, config.ModelConfig.n_features)
    result = basic_nn(test_data)
    print(result)
```