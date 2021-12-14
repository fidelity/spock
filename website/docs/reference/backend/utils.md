---
sidebar_label: utils
title: backend.utils
---

Attr utility functions for Spock

#### get\_attr\_fields

```python
def get_attr_fields(input_classes)
```

Gets the attribute fields from all classes

*Args*:

    input_classes: current list of input classes

*Returns*:

    dictionary of all attrs attribute fields

#### get\_type\_fields

```python
def get_type_fields(input_classes)
```

Creates a dictionary of names and types

*Args*:

    input_classes: list of input classes

*Returns*:

    type_fields: dictionary of names and types

#### flatten\_type\_dict

```python
def flatten_type_dict(type_dict)
```

Flattens a nested dictionary

*Args*:

    type_dict: dictionary of types that are generic

*Returns*:

    flat_dict: flatten dictionary to a single level

#### convert\_to\_tuples

```python
def convert_to_tuples(input_dict, named_type_dict, class_names)
```

Convert lists to tuples

Payloads from markup come in as Lists and not Tuples. This function turns lists in to tuples for the payloads
so the attr values are set correctly. Will call itself recursively if a dictionary is present for class specific
values

*Args*:

    input_dict: input dictionary
    named_type_dict: dictionary of names with generic types

*Returns*:

    updated_dict: a dictionary with lists converted to tuples

#### deep\_update

```python
def deep_update(source, updates)
```

Deeply updates a dictionary

Iterates through a dictionary recursively to update individual values within a possibly nested dictionary
of dictionaries

*Args*:

    source: source dictionary
    updates: updates to the dictionary

*Returns*:

    source: updated version of the source dictionary

#### \_recursive\_list\_to\_tuple

```python
def _recursive_list_to_tuple(key, value, typed, class_names)
```

Recursively turn lists into tuples

Recursively looks through a pair of value and type and sets any of the possibly nested type of value to tuple
if tuple is the specified type

*Args*:

    key: name of parameter
    value: value to check and set typ if necessary
    typed: type of the generic alias to check against
    class_names: list of all spock class names

*Returns*:

    value: updated value with correct type casts

