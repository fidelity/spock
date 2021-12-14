---
sidebar_label: config
title: addons.tune.config
---

Creates the spock config interface that wraps attr -- tune version for hyper-parameters

#### \_spock\_tune

```python
def _spock_tune(cls)
```

Ovverides basic spock_attr decorator with another name

Using a different name allows spock to easily determine which parameters are normal and which are
meant to be used in a hyper-parameter tuning backend

*Args*:

    cls: basic class def

*Returns*:

    cls: slotted attrs class that is frozen and kw only

## RangeHyperParameter Objects

```python
@attr.s
class RangeHyperParameter()
```

Range based hyper-parameter that is sampled uniformly

**Attributes**:

- `type` - type of the hyper-parameter (note: spock will attempt to autocast into this type)
- `bounds` - min and max of the hyper-parameter range
- `log_scale` - log scale the values before sampling

## ChoiceHyperParameter Objects

```python
@attr.s
class ChoiceHyperParameter()
```

Choice based hyper-parameter that is sampled uniformly

**Attributes**:

- `type` - type of the hyper-parameter -- (note: spock will attempt to autocast into this type)
- `choices` - list of variable length that contains all the possible choices to select from

