# Post Initialization Hooks

`spock` supports post initialization (post-init) hooks via the `__post_hook__` and
`__map__` methods within a `@spock` decorated class.
These methods are automatically called after the `Spockspace` object is created thus 
allow the user to do any post instantiation work (such as validation) or map parameter
values to object/class instantiation.

### Post-Init Hooks

Simply add the `__post_hook__` method to your `@spock` decorated class:

```python
from spock import spock
from spock.utils import within, ge
from typing import List


def my_post_init_hook(list_vals: List[float], sum_val: float):
    if sum(list_vals) != sum_val:
        raise ValueError(f"Sum of `{sum(list_vals)}` does not equal 1.0")


@spock
class PostInitExample:
    list_vals: List[float] = [0.5, 0.25, 0.25]
    check_sum: float = 1.0
    my_value: float = 1.2
    other: float = 0.1
    lower_bound: float = 0.0
    
    def __post_hook__(self):
        # Validate that value is between 0.0 and 1.0 (inclusive)
        within(self.my_value, low_bound=0.0, upper_bound=1.0, inclusive_lower=True, inclusive_upper=True)
        # Validate that other is greater than lower_bound
        ge(self.other, bound=self.lower_bound)
        my_post_init_hook(self.list_vals, self.check_sum)
```

The `__post_hook__` method will be triggered post instantiation. Therefore, the example above will throw an `Exception` 
since the value of `my_value` does not fall within the given bounds. Also notice that you can reference other defined
parameters within the `__post_hook__` methods and use them in custom functions (here we use `lower_bound` and 
`check_sum` to do some validation comparisons)


### Map Hooks

Simply add the `__maps__` method to your `@spock` decorated class. This method must
contain an explict return. The return(s) of the `__maps__` method will be mapped to the 
`_map` variable within the instantiated class> For instance: 


```python
# -*- coding: utf-8 -*-
from spock import spock, SpockBuilder
from sagemaker.processing import ProcessingInput

from enum import Enum
from typing import Optional

class UploadMode(Enum):
    end_of_job = "EndOfJob"
    continuous = "Continuous"

@spock
class S3ScratchConfig:
    name: Optional[str] = None
    source: str = "s3://my-path"
    destination: str = "/local/path"
    upload_mode: UploadMode = UploadMode.end_of_job

    def __post_hook__(self):
        print(self.name)

    def __maps__(self):
        return ProcessingInput(
            input_name=self.name,
            source=self.source,
            destination=self.destination
        )

def main():
    # Get configs
    configs = SpockBuilder(
        S3ScratchConfig,
        desc="Configs for testing containers on SM",
        lazy=True
    ).generate()
    print(configs.S3ScatchConfig._maps)

```

The `__maps__` method will be triggered post-instantiation. This means that the parameter
values defined within the `S3ScratchConfig` class will get mapped into the creation of
the `ProcessingInput` instance. Therefore, the return of `_maps` will be the 
instantiated `ProcessingInput` object with the `spock` defined parameters.


### Common Post Initialization Hooks

`spock` provides some common validators (in the `utils` module) that would be typically run as post-init 
hooks including: greater than (`gt`), greater than or equals to (`ge`), less than (`lt`), less than or equals to (`le`),
and if a parameter falls within a set of inclusive/exclusive bounds (`within`).



