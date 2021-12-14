---
sidebar_label: builder
title: backend.builder
---

Handles the building/saving of the configurations from the Spock config classes

## BaseBuilder Objects

```python
class BaseBuilder(ABC)
```

Base class for building the backend specific builders

This class handles the interface to the backend with the generic ConfigArgBuilder so that different
backends can be used to handle processing

*Attributes*

    _input_classes: list of input classes that link to a backend
    _graph: Graph, graph of the dependencies between spock classes
    _max_indent: maximum to indent between help prints
    _module_name: module name to register in the spock module space
    save_path: list of path(s) to save the configs to

#### \_\_init\_\_

```python
def __init__(*args, *, max_indent: int = 4, module_name: str, **kwargs)
```

Init call for BaseBuilder

**Arguments**:

- `*args` - iterable of @spock decorated classes
- `max_indent` - max indent for pretty print of help
- `module_name` - module name to register in the spock module space
- `**kwargs` - keyword args

#### input\_classes

```python
@property
def input_classes()
```

Returns the graph of dependencies between spock classes

#### \_make\_group\_override\_parser

```python
@staticmethod
@abstractmethod
def _make_group_override_parser(parser, class_obj, class_name)
```

Makes a name specific override parser for a given class obj

Takes a class object of the backend and adds a new argument group with argument names given with name
Class.name so that individual parameters specific to a class can be overridden.

*Args*:

    parser: argument parser
    class_obj: instance of a backend class
    class_name: used for module matching

*Returns*:

    parser: argument parser with new class specific overrides

#### handle\_help\_info

```python
def handle_help_info()
```

Handles walking through classes to get help info

For each class this function will search __doc__ and attempt to pull out help information for both the class
itself and each attribute within the class

*Returns*:

    None

#### generate

```python
def generate(dict_args)
```

Method to auto-generate the actual class instances from the generated args

Based on the generated arguments groups and the args read in from the config file(s)
this function instantiates the classes with the necessary field or attr values

*Args*:

    dict_args: dictionary of arguments from the configs

*Returns*:

    namespace containing automatically generated instances of the classes

#### resolve\_spock\_space\_kwargs

```python
def resolve_spock_space_kwargs(graph: Graph, dict_args: dict) -> dict
```

Build the dictionary that will define the spock space.

*Args*:

    graph: Dependency graph of nested spock configurations
    dict_args: dictionary of arguments from the configs

*Returns*:

    dictionary containing automatically generated instances of the classes

#### build\_override\_parsers

```python
def build_override_parsers(parser)
```

Creates parsers for command-line overrides

Builds the basic command line parser for configs and help then iterates through each attr instance to make
namespace specific cmd line override parsers

*Args*:

    parser: argument parser

*Returns*:

    parser: argument parser with new class specific overrides

#### \_extract\_other\_types

```python
def _extract_other_types(typed, module_name)
```

Takes a high level type and recursively extracts any enum or class types

*Args*:

    typed: highest level type
    module_name: name of module to match

*Returns*:

    return_list: list of nums (dot notation of module_path.enum_name or module_path.class_name)

#### \_extract\_fnc

```python
@abstractmethod
def _extract_fnc(val, module_name)
```

Function that gets the nested lists within classes

*Args*:

    val: current attr
    module_name: matching module name

*Returns*:

    list of any nested classes/enums

## AttrBuilder Objects

```python
class AttrBuilder(BaseBuilder)
```

Attr specific builder

Class that handles building for the attr backend

*Attributes*

    input_classes: list of input classes that link to a backend
    _configs: None or List of configs to read from
    _create_save_path: boolean to make the path to save to
    _desc: description for the arg parser
    _no_cmd_line: flag to force no command line reads
    save_path: list of path(s) to save the configs to

#### \_\_init\_\_

```python
def __init__(*args, **kwargs)
```

AttrBuilder init

**Arguments**:

- `*args` - list of input classes that link to a backend
- `**kwargs` - any extra keyword args

#### \_make\_group\_override\_parser

```python
@staticmethod
def _make_group_override_parser(parser, class_obj, class_name)
```

Makes a name specific override parser for a given class obj

Takes a class object of the backend and adds a new argument group with argument names given with name
Class.name so that individual parameters specific to a class can be overridden.

*Args*:

    parser: argument parser
    class_obj: instance of a backend class
    class_name: used for module matching

*Returns*:

    parser: argument parser with new class specific overrides

#### \_extract\_fnc

```python
def _extract_fnc(val, module_name)
```

Function that gets the nested lists within classes

*Args*:

    val: current attr
    module_name: matching module name

*Returns*:

    list of any nested classes/enums

