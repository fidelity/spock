---
sidebar_label: optuna
title: addons.tune.optuna
---

Handles the optuna backend

## OptunaTunerStatus Objects

```python
class OptunaTunerStatus(TypedDict)
```

Tuner status return object for Optuna -- supports the define-and-run style interface from Optuna

*Attributes*:

    trial: current ask trial sample
    study: current optuna study object

## OptunaInterface Objects

```python
class OptunaInterface(BaseInterface)
```

Specific override to support the optuna backend -- supports the define-and-run style interface from Optuna

*Attributes*:

    _map_type: dictionary that maps class names and types to fns that create optuna distributions
    _trial: current trial object from the optuna backend
    _tuner_obj: underlying optuna study object
    _tuner_namespace: tuner namespace that has attr classes that maps to an underlying library types
    _param_obj: underlying object that optuna study can sample from (flat dictionary)
    _sample_hash: hash of the most recent sample draw

#### \_\_init\_\_

```python
def __init__(tuner_config: OptunaTunerConfig, tuner_namespace)
```

OptunaInterface init call that maps variables, creates a map to fnc calls, and constructs the necessary
underlying objects

*Args*:

    tuner_config: configuration object for the optuna backend
    tuner_namespace: tuner namespace that has attr classes that maps to an underlying library types

#### \_uniform\_float\_dist

```python
def _uniform_float_dist(val)
```

Assemble the optuna.distributions.(Log)UniformDistribution object

https://optuna.readthedocs.io/en/stable/reference/generated/optuna.distributions.UniformDistribution.html
https://optuna.readthedocs.io/en/stable/reference/generated/optuna.distributions.LogUniformDistribution.html

*Args*:

    val: current attr val

*Returns*:

    optuna.distributions.UniformDistribution or optuna.distributions.LogUniformDistribution

#### \_uniform\_int\_dist

```python
def _uniform_int_dist(val)
```

Assemble the optuna.distributions.Int(Log)UniformDistribution object

https://optuna.readthedocs.io/en/stable/reference/generated/optuna.distributions.IntUniformDistribution.html
https://optuna.readthedocs.io/en/stable/reference/generated/optuna.distributions.IntLogUniformDistribution.html

*Args*:

    val: current attr val

*Returns*:

    optuna.distributions.IntUniformDistribution or optuna.distributions.IntLogUniformDistribution

#### \_categorical\_dist

```python
def _categorical_dist(val)
```

Assemble the optuna.distributions.CategoricalDistribution object

https://optuna.readthedocs.io/en/stable/reference/generated/optuna.distributions.CategoricalDistribution.html

*Args*:

    val: current attr val

*Returns*:

    optuna.distributions.CategoricalDistribution

