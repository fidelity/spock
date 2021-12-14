---
sidebar_label: tuner
title: addons.tune.tuner
---

Handles the tuner interface interface

## TunerInterface Objects

```python
class TunerInterface()
```

Handles the general tuner interface by creating the necessary underlying tuner class and dispatches necessary
ops to the class instance

*Attributes*:

    _fixed_namespace: fixed parameter namespace used for combination with a sample draw
    _lib_interface: class instance of the underlying hyper-parameter library

#### \_\_init\_\_

```python
def __init__(tuner_config: Union[OptunaTunerConfig, AxTunerConfig], tuner_namespace: Spockspace, fixed_namespace: Spockspace)
```

Init call to the TunerInterface

*Args*:

    tuner_config: necessary object to determine the interface and sample correctly from the underlying library
    tuner_namespace: tuner namespace that has attr classes that maps to an underlying library types
    fixed_namespace: namespace of fixed parameters

#### sample

```python
def sample()
```

Public interface to underlying library sepcific sample that returns a single sample/draw from the
hyper-parameter sets (e.g. ranges, choices) and combines them with the fixed parameters into a single Spockspace

*Returns*:

    Spockspace of drawn sample of hyper-parameters and fixed parameters

#### tuner\_status

```python
@property
def tuner_status()
```

Returns a dictionary of all the necessary underlying tuner internals to report the result

#### best

```python
@property
def best()
```

Returns a Spockspace of the best hyper-parameter config and the associated metric value

