---
sidebar_label: utils
title: utils
---

Utility functions for Spock

#### path\_object\_to\_s3path

```python
def path_object_to_s3path(path: Path) -> str
```

Convert a path object into a string s3 path

*Args*:

    path: a spock config path

*Returns*:

    string of s3 path

#### check\_path\_s3

```python
def check_path_s3(path: Path) -> bool
```

Checks the given path to see if it matches the s3:// regex

*Args*:

    path: a spock config path

*Returns*:

    boolean of regex match

#### \_is\_spock\_instance

```python
def _is_spock_instance(__obj: object)
```

Checks if the object is a @spock decorated class

Private interface that checks to see if the object passed in is registered within the spock module and also
is a class with attrs attributes (__attrs_attrs__)

*Args*:

    __obj: class to inspect

*Returns*:

    bool

#### \_is\_spock\_tune\_instance

```python
def _is_spock_tune_instance(__obj: object)
```

Checks if the object is a @spock decorated class

Private interface that checks to see if the object passed in is registered within the spock module tune addon and also
is a class with attrs attributes (__attrs_attrs__)

*Args*:

    __obj: class to inspect

*Returns*:

    bool

#### \_check\_iterable

```python
def _check_iterable(iter_obj: Union[tuple, list, EnumMeta])
```

Check if an iterable type contains a spock class

**Arguments**:

- `iter_obj` - iterable type
  

**Returns**:

  boolean if the iterable contains at least one spock class

#### make\_argument

```python
def make_argument(arg_name, arg_type, parser)
```

Make argparser argument based on type

Based on the type passed in handle the creation of the argparser argument so that overrides will have the correct
behavior when set

*Args*:

    arg_name: name for the argument
    arg_type: type of the argument
    parser: current parser

*Returns*:

    parser: updated argparser

#### \_handle\_generic\_type\_args

```python
def _handle_generic_type_args(val)
```

Evaluates a string containing a Python literal

Seeing a list and tuple types will come in as string literal format, use ast to get the actual type

*Args*:

    val: string literal

*Returns*:

    the underlying string literal type

#### add\_info

```python
def add_info()
```

Adds extra information to the output dictionary

*Args*:


*Returns*:

    out_dict: output dictionary

#### make\_blank\_git

```python
def make_blank_git(out_dict)
```

Adds blank git info

*Args*:

    out_dict: current output dictionary

*Returns*:

    out_dict: output dictionary with added git info

#### add\_repo\_info

```python
def add_repo_info(out_dict)
```

Adds GIT information to the output dictionary

*Args*:

    out_dict: output dictionary

*Returns*:

    out_dict: output dictionary

#### add\_generic\_info

```python
def add_generic_info(out_dict)
```

Adds date, fqdn information to the output dictionary

*Args*:

    out_dict: output dictionary

*Returns*:

    out_dict: output dictionary

#### \_maybe\_docker

```python
def _maybe_docker(cgroup_path="/proc/self/cgroup")
```

Make a best effort to determine if run in a docker container

*Args*:

    cgroup_path: path to cgroup file

*Returns*:

    boolean of best effort docker determination

#### \_maybe\_k8s

```python
def _maybe_k8s(cgroup_path="/proc/self/cgroup")
```

Make a best effort to determine if run in a container via k8s

*Args*:

    cgroup_path: path to cgroup file

*Returns*:

    boolean of best effort k8s determination

#### deep\_payload\_update

```python
def deep_payload_update(source, updates)
```

Deeply updates a dictionary

Iterates through a dictionary recursively to update individual values within a possibly nested dictionary
of dictionaries -- creates a dictionary if empty and trying to recurse

*Args*:

    source: source dictionary
    updates: updates to the dictionary

*Returns*:

    source: updated version of the source dictionary

#### check\_payload\_overwrite

```python
def check_payload_overwrite(payload, updates, configs, overwrite="")
```

Warns when parameters are overwritten across payloads as order will matter

*Args*:

    payload: current payload
    payload_update: update to add to payload
    configs: config path
    overwrite: name of parent

*Returns*:

