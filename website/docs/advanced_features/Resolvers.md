# Resolvers

`spock` currently supports a single resolver notation `.env` with two annotations `.crypto` and `.inject`.

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




