---
sidebar_label: payload
title: backend.payload
---

Handles payloads from markup files

## BasePayload Objects

```python
class BasePayload(BaseHandler)
```

Handles building the payload for config file(s)

This class builds out the payload from config files of multiple types. It handles various
file types and also composition of config files via recursive calls

*Attributes*:

    _loaders: maps of each file extension to the loader class
    __s3_config: optional S3Config object to handle s3 access

#### \_update\_payload

```python
@staticmethod
@abstractmethod
def _update_payload(base_payload, input_classes, ignore_classes, payload)
```

Updates the payload

Checks the parameters defined in the config files against the provided classes and if
passable adds them to the payload

*Args*:

    base_payload: current payload
    input_classes: class to roll into
    ignore_classes: list of classes to ignore
    payload: total payload

*Returns*:

    payload: updated payload

#### payload

```python
def payload(input_classes, ignore_classes, path, cmd_args, deps)
```

Builds the payload from config files

Public exposed call to build the payload and set any command line overrides

*Args*:

    input_classes: list of backend classes
    ignore_classes: list of classes to ignore
    path: path to config file(s)
    cmd_args: command line overrides
    deps: dictionary of config dependencies

*Returns*:

    payload: dictionary of all mapped parameters

#### \_payload

```python
def _payload(input_classes, ignore_classes, path, deps, root=False)
```

Private call to construct the payload

Main function call that builds out the payload from config files of multiple types. It handles
various file types and also composition of config files via a recursive calls

*Args*:
    input_classes: list of backend classes
    ignore_classes: list of classes to ignore
    path: path to config file(s)
    deps: dictionary of config dependencies

*Returns*:

    payload: dictionary of all mapped parameters

#### \_handle\_dependencies

```python
@staticmethod
def _handle_dependencies(deps, path, root)
```

Handles config file dependencies

Checks to see if the config path (full or relative) has already been encountered. Essentially a DFS for graph
cycles

*Args*:

    deps: dictionary of config dependencies
    path: current config path
    root: boolean if root

*Returns*:

    deps: updated dependencies

#### \_handle\_includes

```python
def _handle_includes(base_payload, config_extension, input_classes, ignore_classes, path: Path, payload, deps)
```

Handles config composition

For all of the config tags in the config file this function will recursively call the payload function
with the composition path to get the additional payload(s) from the composed file(s) -- checks for file
validity or if it is an S3 URI via regex

*Args*:

    base_payload: base payload that has a config kwarg
    config_extension: file type
    input_classes: defined backend classes
    ignore_classes: list of classes to ignore
    path: path to base file
    payload: payload pulled from composed files
    deps: dictionary of config dependencies

*Returns*:

    payload: payload update from composed files

#### \_handle\_overrides

```python
def _handle_overrides(payload, ignore_classes, args)
```

Handle command line overrides

Iterate through the command line override values, determine at what level to set them, and set them if possible

*Args*:

    payload: current payload dictionary
    args: command line override args

*Returns*:

    payload: updated payload dictionary with override values set

#### \_prune\_args

```python
@staticmethod
def _prune_args(args, ignore_classes)
```

Prunes ignored class names from the cmd line args list to prevent incorrect access

*Args*:

    args: current cmd line args
    ignore_classes: list of class names to ignore

*Returns*:

    dictionary of pruned cmd line args

#### \_handle\_payload\_override

```python
@staticmethod
@abstractmethod
def _handle_payload_override(payload, key, value)
```

Handles the complex logic needed for List[spock class] overrides

Messy logic that sets overrides for the various different types. The hardest being List[spock class] since str
names have to be mapped backed to sys.modules and can be set at either the general or class level.

*Args*:

    payload: current payload dictionary
    key: current arg key
    value: value at current arg key

*Returns*:

    payload: modified payload with overrides

## AttrPayload Objects

```python
class AttrPayload(BasePayload)
```

Handles building the payload for attrs backend

This class builds out the payload from config files of multiple types. It handles various
file types and also composition of config files via a recursive calls

*Attributes*:

    _loaders: maps of each file extension to the loader class

#### \_\_init\_\_

```python
def __init__(s3_config=None)
```

Init for AttrPayload

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

#### \_handle\_payload\_override

```python
@staticmethod
def _handle_payload_override(payload, key, value)
```

Handles the complex logic needed for List[spock class] overrides

Messy logic that sets overrides for the various different types. The hardest being List[spock class] since str
names have to be mapped backed to sys.modules and can be set at either the general or class level.

*Args*:

    payload: current payload dictionary
    key: current arg key
    value: value at current arg key

*Returns*:

    payload: modified payload with overrides

