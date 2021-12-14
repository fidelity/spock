---
sidebar_label: ax
title: addons.tune.ax
---

Handles the ax backend

## AxTunerStatus Objects

```python
class AxTunerStatus(TypedDict)
```

Tuner status return object for Ax -- supports the service style API from Ax

*Attributes*:

    client: current AxClient instance
    trial_index: current trial index

## AxInterface Objects

```python
class AxInterface(BaseInterface)
```

Specific override to support the Ax backend -- supports the service style API from Ax

#### \_\_init\_\_

```python
def __init__(tuner_config: AxTunerConfig, tuner_namespace)
```

AxInterface init call that maps variables, creates a map to fnc calls, and constructs the necessary
underlying objects

*Args*:

    tuner_config: configuration object for the ax backend
    tuner_namespace: tuner namespace that has attr classes that maps to an underlying library types

#### \_ax\_range

```python
def _ax_range(name, val)
```

Assemble the dictionary for ax range parameters

*Args*:

    name: parameter name
    val: current attr val

*Returns*:

    dictionary that can be added to a parameter list

#### \_ax\_choice

```python
def _ax_choice(name, val)
```

Assemble the dictionary for ax choice parameters

*Args*:

    name: parameter name
    val: current attr val

*Returns*:

    dictionary that can be added to a parameter list

