---
sidebar_label: interface
title: addons.tune.interface
---

Handles the base interface

## BaseInterface Objects

```python
class BaseInterface(ABC)
```

Base interface for the various hyper-parameter tuner backends

*Attributes*

    _tuner_config: spock version of the tuner configuration
    _tuner_namespace: tuner namespace that has attr classes that maps to an underlying library types

#### \_\_init\_\_

```python
def __init__(tuner_config, tuner_namespace: Spockspace)
```

Base init call that maps a few variables

*Args*:

    tuner_config: necessary dict object to determine the interface and sample correctly from the underlying library
    tuner_namespace: tuner namespace that has attr classes that maps to an underlying library types

#### sample

```python
@abstractmethod
def sample()
```

Calls the underlying library sample to get a single sample/draw from the hyper-parameter
sets (e.g. ranges, choices)

*Returns*:

    Spockspace of the current hyper-parameter draw

#### \_construct

```python
@abstractmethod
def _construct()
```

Constructs the base object needed by the underlying library to construct the correct object that allows
for hyper-parameter sampling

*Returns*:

    flat dictionary of all hyper-parameters named with dot notation (class.param_name)

#### \_get\_sample

```python
@property
@abstractmethod
def _get_sample()
```

Gets the sample parameter dictionary from the underlying backend

#### tuner\_status

```python
@property
@abstractmethod
def tuner_status()
```

Returns a dictionary of all the necessary underlying tuner internals to report the result

#### best

```python
@property
@abstractmethod
def best()
```

Returns a Spockspace of the best hyper-parameter config and the associated metric value

#### \_sample\_rollup

```python
@staticmethod
def _sample_rollup(params)
```

Rollup the sample draw into a dictionary that can be converted to a spockspace with the correct names and
roots -- un-dots the name structure

*Args*:

    params: current parameter dictionary -- named by dot notation

*Returns*:

    dictionary of rolled up sampled parameters
    md5 hash of the dictionary contents

#### \_gen\_spockspace

```python
def _gen_spockspace(tune_dict: Dict)
```

Converts a dictionary of dictionaries of parameters into a valid Spockspace

*Args*:

tune_dict: dictionary of current parameters

**Returns**:

  
- `tune_dict` - Spockspace

#### \_config\_to\_dict

```python
@staticmethod
def _config_to_dict(tuner_config: Union[OptunaTunerConfig, AxTunerConfig])
```

Turns an attrs config object into a dictionary

*Args*:

    tuner_config: attrs config object

*Returns*:

    dictionary of the attrs config object

#### \_to\_spockspace

```python
@staticmethod
def _to_spockspace(tune_dict: Dict)
```

Converts a dict to a Spockspace

*Args*:

    tune_dict: current dictionary

*Returns*:

    Spockspace of dict

#### \_get\_caster

```python
@staticmethod
def _get_caster(val)
```

Gets a callable type object from a string type

*Args*:

    val: current attr val:

*Returns*:

    type class object

#### \_try\_choice\_cast

```python
def _try_choice_cast(val, type_string: str)
```

Try/except for casting choice parameters

*Args*:

    val: current attr val
    type_string: spock hyper-parameter type name

*Returns*:

    val: updated attr val

#### \_try\_range\_cast

```python
def _try_range_cast(val, type_string: str)
```

Try/except for casting range parameters

*Args*:

    val: current attr val
    type_string: spock hyper-parameter type name

*Returns*:

    low: low bound
    high: high bound

