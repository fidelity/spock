---
sidebar_label: builder
title: addons.tune.builder
---

Handles the tuner builder backend

## TunerBuilder Objects

```python
class TunerBuilder(BaseBuilder)
```

#### \_\_init\_\_

```python
def __init__(*args, **kwargs)
```

TunerBuilder init

**Arguments**:

- `*args` - list of input classes that link to a backend
- `configs` - None or List of configs to read from
- `desc` - description for the arg parser
- `no_cmd_line` - flag to force no command line reads
- `**kwargs` - any extra keyword args

#### \_make\_group\_override\_parser

```python
@staticmethod
def _make_group_override_parser(parser, class_obj, class_name)
```

Makes a name specific override parser for a given class obj

Takes a class object of the backend and adds a new argument group with argument names given with name
Class.val.(unrolled config parameters) so that individual parameters specific to a class can be overridden.

*Args*:

    parser: argument parser
    class_obj: instance of a backend class
    class_name: used for module matching

*Returns*:

    parser: argument parser with new class specific overrides

