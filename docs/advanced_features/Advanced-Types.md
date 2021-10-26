# Advanced Types

`spock` also supports nested `List` or `Tuple` types and advanced argument types (such as repeated objects) that 
use `Enum` or `@spock` decorated classes. All of the advanced types support the use of `Optional` and setting default 
values. Example usage of advanced types can be found in the unittests 
[here](https://github.com/fidelity/spock/tree/master/tests).

### Nested List/Tuple Types

`List[List[int]]` -- Defines a list of list of integers.

`List[List[str]]` -- Defines a list of list of strings.

### Lists/Tuples of `Enum`

```python
from enum import Enum
from spock.config import spock
from typing import List


class StrChoice(Enum):
    option_1 = 'option_1'
    option_2 = 'option_2'

@spock
class TypeConfig:
    list_choice_p_str: List[StrChoice]
```

With YAML definitions:

```yaml
list_choice_p_str: ['option_1', 'option_2']
```

### List/Tuple of Repeated `@spock` Classes 

These can be accessed by index and are iterable.

```python
from spock.config import spock
from typing import List


@spock
class NestedListStuff:
    one: int
    two: str

@spock
class TypeConfig:
    nested_list: List[NestedListStuff] # To Set Default Value append '= NestedListStuff'
```

With YAML definitions:

```yaml
# Nested List configuration
nested_list: NestedListStuff
NestedListStuff:
    - one: 10
      two: hello
    - one: 20
      two: bye
```

### `Enum` of `@spock` Classes

```python
from enum import Enum
from spock.config import spock


@spock
class ClassOne:
    one: int
    two: str


@spock
class ClassTwo:
    one: int
    two: str


class ClassChoice(Enum):
    class_one = ClassOne
    class_two = ClassTwo

@spock
class TypeConfig:
    param: ClassChoice

```

With YAML definitions:

```yaml
# Nested List configuration
TypeConfig:
  param: ClassTwo

ClassOne:
    one: 20
    two: bye

ClassTwo:
    one: 10
    two: hello

```
