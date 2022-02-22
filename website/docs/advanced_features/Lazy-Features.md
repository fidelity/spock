# Lazy Evaluation

`spock` supports lazy evaluation for both dependencies between classes and class inheritance.

### Lazy Class Dependencies
When we create a new `spock` class that depends on another `spock` class we can be 'lazy' and pass only the top-level 
class(es) to the `SpockBuilder` instead of all the dependent classes. This tends to make your code much less verbose 
when there are many `@spock` decorated classes. We do this by setting the `lazy` flag to `True` 
within the `SpockBuilder`. This will tell spock to look for any missing references to `@spock` decorated classes
within `sys.modules["spock"].backend.config` and add them to the underlying list of classes within graph construction.
For instance, 

```python
from spock import spock
from spock import SpockBuilder

@spock
class NestedStuffDefault:
    away: str = "arsenal"
    goals: int = 0


@spock
class Maybe:
    r: int = 4
    t: float = 1.9
    nested_no_conf_def: NestedStuffDefault = NestedStuffDefault


# Set lazy to True to make sure spock lazily finds @spock decorated classes 
# Not we only pass the Maybe class here instead of both Maybe and NestedStuffDefault
config = SpockBuilder(Maybe, desc='Lazy Example', lazy=True).generate()
```

The above is equivalent to passing both `Maybe` and `NestedStuffDefault` to the `SpockBuilder`.

### Lazy Class Inheritance

When we create a new `spock` class that inherits from another `spock` class we can be 'lazy' and leave off the
`@spock` decorator for any parent classes. We do this by setting the `dynamic` flag within the `@spock` decorator to
`True`. With this flag, `spock` will traverse the MRO and automatically cast parent classes to the equivalent of a 
`@spock` decorated class. With lazy inheritance you only need to pass the child class to the `SpockBuilder` instead of
all parents and children. Additionally, set the `lazy` flag to `True` within the `SpockBuilder` to lazily find and 
return the parent classes to the generated `Spockspace`. For instance:

```python
from spock import spock
from spock import SpockBuilder
from typing import Optional

class OptimizerConfig:
    lr: float = 0.01
    n_epochs: int = 2
    grad_clip: Optional[float]


class DataConfig:
    batch_size: int = 2


# Set dynamic=True to allow for lazy inheritance
@spock(dynamic=True)
class SGDConfig(OptimizerConfig, DataConfig):
    weight_decay: float
    momentum: float
    nesterov: bool

# Set lazy to True to make sure the parent classes are returned from the generate call
config = SpockBuilder(SGDConfig, desc='Lazy Example', lazy=True).generate()
```

The above is equivalent to decorating each class with the `@spock` decorator and additionally passing `DataConfig` and
`OptimizerConfig` to the `SpockBuilder`.