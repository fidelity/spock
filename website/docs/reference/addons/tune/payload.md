---
sidebar_label: payload
title: addons.tune.payload
---

Handles the tuner payload backend

## TunerPayload Objects

```python
class TunerPayload(BasePayload)
```

Handles building the payload for tuners

This class builds out the payload from config files of multiple types. It handles various
file types and also composition of config files via a recursive calls

*Attributes*:

    _loaders: maps of each file extension to the loader class

#### \_\_init\_\_

```python
def __init__(s3_config=None)
```

Init for TunerPayload

*Args*:

    s3_config: optional S3 config object

#### \_\_call\_\_

```python
def __call__(*args, **kwargs)
```

Call to allow self chaining

*Args*:

    *args:
    **kwargs:

*Returns*:

    Payload: instance of self

