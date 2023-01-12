# Resolvers

`spock` currently supports the resolver notation(s) `.env` and `.var` with 
two annotations `.crypto` and `.inject` for `.env`.

### Variable Resolver

`spock` supports resolving value definitions from other defined variable definitions with the
following syntax, `${spock.var:RefClass.ref_value}`.This will set the value from the
value set within the referenced class and attribute. In addition, `spock` supports using
multiple references within the definition such as, 
`version-${spock.var:RefClass.ref_value1}-${spock.var:RefClass.ref_value2}` which will
resolve both references. Currently, variable resolution only supports simple 
types: `float`, `int`, `string`, and `bool`. For example, let's define a bunch of 
parameters that will rely on the variable resolver:

```python
from spock import spock
from spock import SpockBuilder

from typing import Optional
import os


@spock
class Lastly:
    ooooyah: int = 12
    tester: int = 1
    hiyah: bool = True


@spock
class BarFoo:
    newval: Optional[int] = 2
    moreref: int = "${spock.var:Lastly.ooooyah}"


@spock
class FooBar:
    val: int = 12


@spock
class RefClass:
    a_float: float = 12.1
    a_int: int = 3
    a_bool: bool = True
    a_string: str = "helloo"


@spock
class RefClassFile:
    ref_float: float
    ref_int: int
    ref_bool: bool
    ref_string: str
    ref_nested_to_str: str
    ref_nested_to_float: float


@spock
class RefClassOptionalFile:
    ref_float: Optional[float]
    ref_int: Optional[int]
    ref_bool: Optional[bool]
    ref_string: Optional[str]
    ref_nested_to_str: Optional[str]
    ref_nested_to_float: Optional[float]


@spock
class RefClassDefault:
    ref_float: float = "${spock.var:RefClass.a_float}"
    ref_int: int = "${spock.var:RefClass.a_int}"
    ref_bool: bool = "${spock.var:RefClass.a_bool}"
    ref_string: str = "${spock.var:RefClass.a_string}"
    ref_nested_to_str: str = "${spock.var:FooBar.val}.${spock.var:Lastly.tester}"
    ref_nested_to_float: float = "${spock.var:FooBar.val}.${spock.var:Lastly.tester}"
```


These demonstrate the basic paradigms of variable references as well as the ability to
use multiple variable references within a single definition. The returned 
`Spockspace` would be:

```shell
BarFoo: !!python/object:spock.backend.config.BarFoo
  moreref: 12
  newval: 2
FooBar: !!python/object:spock.backend.config.FooBar
  val: 12
Lastly: !!python/object:spock.backend.config.Lastly
  hiyah: true
  ooooyah: 12
  tester: 1
RefClass: !!python/object:spock.backend.config.RefClass
  a_bool: true
  a_float: 12.1
  a_int: 3
  a_string: helloo
RefClassDefault: !!python/object:spock.backend.config.RefClassDefault
  ref_bool: true
  ref_float: 12.1
  ref_int: 3
  ref_nested_to_float: 12.1
  ref_nested_to_str: '12.1'
  ref_string: helloo
```

### Environment Resolver

`spock` supports resolving value definitions from environmental variables with the following syntax, 
`${spock.env:name, default}`. This will read the value from the named env variable and fall back on the default if 
specified. Currently, environmental variable resolution only supports simple types: `float`, `int`, `string`, and 
`bool`. For example, let's define a bunch of parameters that will rely on the environment resolver:

```python
from spock import spock
from spock import SpockBuilder

from typing import Optional
import os

# Set some ENV variables here just as an example -- these can/should already be defined in your local/cluster env
os.environ['INT_ENV'] = "2"
os.environ['FLOAT_ENV'] = "2.0"
os.environ["BOOL_ENV"] = "true"
os.environ["STRING_ENV"] = "boo"


@spock
class EnvClass:
    # Basic types no defaults
    env_int: int = "${spock.env:INT_ENV}"
    env_float: float = "${spock.env:FLOAT_ENV}"
    env_bool: bool = "${spock.env:BOOL_ENV}"
    env_str: str = "${spock.env:STRING_ENV}"
    # Basic types w/ defaults
    env_int_def: int = "${spock.env:INT_DEF, 3}"
    env_float_def: float = "${spock.env:FLOAT_DEF, 3.0}"
    env_bool_def: bool = "${spock.env:BOOL_DEF, True}"
    env_str_def: str = "${spock.env:STRING_DEF, hello}"
    # Basic types allowing None as default
    env_int_def_opt: Optional[int] = "${spock.env:INT_DEF, None}"
    env_float_def_opt: Optional[float] = "${spock.env:FLOAT_DEF, None}"
    env_bool_def_opt: Optional[bool] = "${spock.env:BOOL_DEF, False}"
    env_str_def_opt: Optional[str] = "${spock.env:STRING_DEF, None}"

config = SpockBuilder(EnvClass).generate().save(user_specified_path='/tmp')
```

These demonstrate the three common paradigms: (1) read from an env variable and if not present throw an exception since
no default is defined, (2) read from an env variable and if not present fallback on the given default value, (3) read
from an optional env variable and fallback on None or False if not present (i.e. optional values). The returned 
`Spockspace` would be:

```shell
EnvClass: !!python/object:spock.backend.config.EnvClass
  env_bool: true
  env_bool_def: true
  env_bool_def_opt: false
  env_float: 2.0
  env_float_def: 3.0
  env_float_def_opt: null
  env_int: 2
  env_int_def: 3
  env_int_def_opt: null
  env_str: boo
  env_str_def: hello
  env_str_def_opt: null
```

and the saved output YAML (from the `.save` call) would be:

```yaml
EnvClass:
  env_bool: true
  env_bool_def: true
  env_bool_def_opt: false
  env_float: 2.0
  env_float_def: 3.0
  env_int: 2
  env_int_def: 3
  env_str: boo
  env_str_def: hello
```

### Inject Annotation

In some cases you might want to save the configuration state with the same references to the env variables that you
defined the parameters with instead of the resolved variables. This is available via the `.inject` annotation that 
can be added to the `.env` notation. For instance, let's change a few of the definitions above to use the `.inject` 
annotation:

```python
from spock import spock
from spock import SpockBuilder

from typing import Optional
import os

# Set some ENV variables here just as an example -- these can/should already be defined in your local/cluster env
os.environ['INT_ENV'] = "2"
os.environ['FLOAT_ENV'] = "2.0"
os.environ["BOOL_ENV"] = "true"
os.environ["STRING_ENV"] = "boo"


@spock
class EnvClass:
    # Basic types no defaults
    env_int: int = "${spock.env:INT_ENV}"
    env_float: float = "${spock.env:FLOAT_ENV}"
    env_bool: bool = "${spock.env:BOOL_ENV}"
    env_str: str = "${spock.env:STRING_ENV}"
    # Basic types w/ defaults    env_int_def: int = "${spock.env.inject:INT_DEF, 3}"
    env_float_def: float = "${spock.env.inject:FLOAT_DEF, 3.0}"
    env_bool_def: bool = "${spock.env.inject:BOOL_DEF, True}"
    env_str_def: str = "${spock.env.inject:STRING_DEF, hello}"
    # Basic types allowing None as default
    env_int_def_opt: Optional[int] = "${spock.env:INT_DEF, None}"
    env_float_def_opt: Optional[float] = "${spock.env:FLOAT_DEF, None}"
    env_bool_def_opt: Optional[bool] = "${spock.env:BOOL_DEF, False}"
    env_str_def_opt: Optional[str] = "${spock.env:STRING_DEF, None}"

config = SpockBuilder(EnvClass).generate().save(user_specified_path='/tmp')
```

The returned `Spockspace` within Python would still be the same as above:

```shell
EnvClass: !!python/object:spock.backend.config.EnvClass
  env_bool: true
  env_bool_def: true
  env_bool_def_opt: false
  env_float: 2.0
  env_float_def: 3.0
  env_float_def_opt: null
  env_int: 2
  env_int_def: 3
  env_int_def_opt: null
  env_str: boo
  env_str_def: hello
  env_str_def_opt: null
```

However, the saved output YAML (from the `.save` call) would change to a version where the values of those annotated 
with the `.inject` annotation will fall back to the env syntax:

```yaml
EnvClass:
  env_bool: true
  env_bool_def: ${spock.env.inject:BOOL_DEF, True}
  env_bool_def_opt: false
  env_float: 2.0
  env_float_def: ${spock.env.inject:FLOAT_DEF, 3.0}
  env_int: 2
  env_int_def: ${spock.env.inject:INT_DEF, 3}
  env_str: boo
  env_str_def: ${spock.env.inject:STRING_DEF, hello}
```

### Cryptographic Annotation

Sometimes environmental variables within a set of `spock` definitions and `Spockspace` output might contain sensitive 
information (i.e. a lot of cloud infra use env variables that might contain passwords, internal DNS domains, etc.) that 
shouldn't be stored in simple plaintext. The `.crypto` annotation provides a simple way to hide these sensitive 
variables while still maintaining the written/loadable state of the spock config by 'encrypting' annotated values. 

For example, let's define a parameter that will rely on the environment resolver but contains sensitive information 
such that we don't want to store it in plaintext (so we add the `.crypto` annotation):

```python
from spock import spock
from spock import SpockBuilder
import os

# Set some ENV variables here just as an example -- these can/should already be defined in your local/cluster env
os.environ['PASSWORD'] = "youshouldntseeme!"


@spock
class SecretClass:
    # Basic types w/ defaults    env_int_def: int = "${spock.env.inject:INT_DEF, 3}"
    env_float_def: float = "${spock.env.inject:FLOAT_DEF, 3.0}"
    env_bool_def: bool = "${spock.env.inject:BOOL_DEF, True}"
    env_str_def: str = "${spock.env.inject:STRING_DEF, hello}"
    # A value that needs to be 'encrypted'
    env_password: str = "${spock.env.crypto:PASSWORD}"

config = SpockBuilder(SecretClass).generate().save(user_specified_path='/tmp')
```

The returned `Spockspace` within Python would contain plaintext information for use within code:

```shell
SecretClass: !!python/object:spock.backend.config.SecretClass
  env_bool_def: true
  env_float_def: 3.0
  env_password: youshouldntseeme!
  env_str_def: hello
```

However, the saved output YAML (from the `.save` call) would change to a version where the values of those values 
annotated with the `.crypto` annotation will be encrypted with a salt and key (via 
[Cryptography](https://github.com/pyca/cryptography)):

```yaml
SecretClass:
  env_bool_def: ${spock.env.inject:BOOL_DEF, True}
  env_float_def: ${spock.env.inject:FLOAT_DEF, 3.0}
  env_password: ${spock.crypto:gAAAAABig8FexSFATx1hdYZa_Knk8wfS2KSb8ylqFWTcfBsC_1nprKK4_G6EI9hMAJ7C39sxDWMMEGlKBfeYsb_NTTCTeaRmlxO3T37_AlAwCWfgG0cnzmyZaTctquKRNc6RnKL8VK2m}
  env_str_def: ${spock.env.inject:STRING_DEF, hello}
```

Additionally, two extra files will be written to file: a YAML containing the salt (`*.spock.cfg.salt.yaml`) and another 
YAML containing the key (`*.spock.cfg.key.yaml`). These files contain the salt and key that were used to encrypt values
annotated with `.crypto`.

In order to use the 'encrypted' versions of `spock` parameters (from a config file or as a given default within the
code) the `salt` and `key` used to encrypt the value must be passed to the `SpockBuilder` as keyword args. For 
instance, let's use the output from above (here we set the default value for instructional purposes, but this could 
also be the value in a configuration file):

```python
from spock import spock
from spock import SpockBuilder
import os

# Set some ENV variables here just as an example -- these can/should already be defined in your local/cluster env
os.environ['PASSWORD'] = "youshouldntseeme!"


@spock
class SecretClass:
    # Basic types w/ defaults    env_int_def: int = "${spock.env.inject:INT_DEF, 3}"
    env_float_def: float = "${spock.env.inject:FLOAT_DEF, 3.0}"
    env_bool_def: bool = "${spock.env.inject:BOOL_DEF, True}"
    env_str_def: str = "${spock.env.inject:STRING_DEF, hello}"
    # A value that needs to be 'encrypted' -- here we 
    env_password: str = "${spock.crypto:gAAAAABig8FexSFATx1hdYZa_Knk8wfS2KSb8ylqFWTcfBsC_1nprKK4_G6EI9hMAJ7C39sxDWMMEGlKBfeYsb_NTTCTeaRmlxO3T37_AlAwCWfgG0cnzmyZaTctquKRNc6RnKL8VK2m}"

config = SpockBuilder(
    SecretClass,
    key="/path/to/file/b4635a04-7fba-42f7-9257-04532a4715fd.spock.cfg.key.yaml",
    salt="/path/to/file/b4635a04-7fba-42f7-9257-04532a4715fd.spock.cfg.salt.yaml"
).generate()
```

Here we pass in the path to the YAML files that contain the `salt` and `key` to the `SpockBuilder` which allows the
'encrypted' values to be 'decrypted' and used within code. The returned `Spockspace` would be exactly as before:

```shell
SecretClass: !!python/object:spock.backend.config.SecretClass
  env_bool_def: true
  env_float_def: 3.0
  env_password: youshouldntseeme!
  env_str_def: hello
```

The `salt` and `key` can also be directly specified from a `str` and `ByteString` accordingly:

```python
config = SpockBuilder(
    SecretClass,
    key=b'9DbRPjN4B_aRBZjfhIgDUnzYLQcmK2gGURhmIDtamSA=',
    salt="NrnNndAEbXD2PT6n"
).generate()
```

or the `salt` and `key` can be specified as environmental variables which will then be resolved by the environment 
resolver:

```python
config = SpockBuilder(
    SecretClass,
    key='${spock.env:KEY}',
    salt="${spock.env:SALT}"
).generate()
```




