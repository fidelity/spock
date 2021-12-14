---
sidebar_label: help
title: backend.help
---

Handles all ops for assembling and pretty printing help info

#### find\_attribute\_idx

```python
def find_attribute_idx(newline_split_docs)
```

Finds the possible split between the header and Attribute annotations

*Args*:

newline_split_docs: new line split text

**Returns**:

  
- `idx` - -1 if none or the idx of Attributes

#### split\_docs

```python
def split_docs(obj)
```

Possibly splits head class doc string from attribute docstrings

Attempts to find the first contiguous line within the Google style docstring to use as the class docstring.
Splits the docs base on the Attributes tag if present.

*Args*:

    obj: class object to rip info from

*Returns*:

    class_doc: class docstring if present or blank str
    attr_doc: list of attribute doc strings

#### match\_attribute\_docs

```python
def match_attribute_docs(attr_name, attr_docs, attr_type_str, attr_default=NOTHING)
```

Matches class attributes with attribute docstrings via regex

*Args*:

    attr_name: attribute name
    attr_docs: list of attribute docstrings
    attr_type_str: str representation of the attribute type
    attr_default: str representation of a possible default value

*Returns*:

    dictionary of packed attribute information

#### handle\_attributes\_print

```python
def handle_attributes_print(info_dict, max_indent: int)
```

Prints attribute information in an argparser style format

*Args*:

    info_dict: packed attribute info dictionary to print
    max_indent: max indent for pretty print of help

#### get\_type\_string

```python
def get_type_string(val, nested_others)
```

Gets the type of the attr val as a string

*Args*:

    val: current attr being processed
    nested_others: list of nested others to deal with that might have module path info in the string

*Returns*:

    type_string: type of the attr as a str

#### get\_from\_sys\_modules

```python
def get_from_sys_modules(cls_name)
```

Gets the class from a dot notation name

*Args*:

    cls_name: dot notation enum name

*Returns*:

    module: enum class

#### handle\_help\_main

```python
def handle_help_main(input_classes: list, module_name: str, extract_fnc: Callable, max_indent: int)
```

Handles the print of the main class types

*Args*:

    input_classes: current set of input classes
    module_name: module name to match
    extract_fnc: function that gets the nested lists within classes
    max_indent: max indent for pretty print of help

*Returns*:

    other_list: extended list of other classes/enums to process

#### handle\_help\_enums

```python
def handle_help_enums(other_list: list, module_name: str, extract_fnc: Callable, max_indent: int)
```

Handles any extra enums from non main args

*Args*:

    other_list: extended list of other classes/enums to process
    module_name: module name to match
    extract_fnc: function that gets the nested lists within classes
    max_indent: max indent for pretty print of help

*Returns*:

    None

#### attrs\_help

```python
def attrs_help(input_classes: Union[list, tuple], module_name: str, extract_fnc: Callable, max_indent: int)
```

Handles walking through a list classes to get help info

For each class this function will search __doc__ and attempt to pull out help information for both the class
itself and each attribute within the class. If it finds a repeated class in a iterable object it will
recursively call self to handle information

*Args*:

    input_classes: list of attr classes
    module_name: name of module to match
    extract_fnc: function that gets the nested lists within classes
    max_indent: max indent for pretty print of help

*Returns*:

    None

