---
sidebar_label: typed
title: backend.typed
---

Handles the definitions of arguments types for Spock (backend: attrs)

## SavePath Objects

```python
class SavePath(str)
```

Spock special key for saving the Spock config to file

Defines a special key use to save the current Spock config to file

#### \_get\_name\_py\_version

```python
def _get_name_py_version(typed)
```

Gets the name of the type depending on the python version

*Args*:

    typed: the type of the parameter

*Returns*:

    name of the type

#### \_extract\_base\_type

```python
def _extract_base_type(typed)
```

Extracts the name of the type from a _GenericAlias

Assumes that the derived types are only of length 1 as the __args__ are [0] recursed... this is not true for
tuples

*Args*:

    typed: the type of the parameter

*Returns*:

    name of type

#### \_recursive\_generic\_validator

```python
def _recursive_generic_validator(typed)
```

Recursively assembles the validators for nested generic types

Walks through the nested type structure and determines whether to recurse all the way to a base type. Once it
hits the base type it bubbles up the correct validator that is nested within the upper validator

*Args*:

    typed: input type

*Returns*:

    return_type: recursively built deep_iterable validators

#### \_generic\_alias\_katra

```python
def _generic_alias_katra(typed, default=None, optional=False)
```

Private interface to create a subscripted generic_alias katra

A &#x27;katra&#x27; is the basic functional unit of `spock`. It defines a parameter using attrs as the backend, type checks
both simple types and subscripted GenericAlias types (e.g. lists and tuples), handles setting default parameters,
and deals with parameter optionality

Handles: List[type] and Tuple[type]

*Args*:

    typed: the type of the parameter to define
    default: the default value to assign if given
    optional: whether to make the parameter optional or not (thus allowing None)

*Returns*:

    x: Attribute from attrs

#### \_check\_enum\_props

```python
def _check_enum_props(typed)
```

Handles properties of enums

Checks if all types of the enum are the same and assembles a list of allowed values

*Args*:

    typed: the type of parameter (Enum)

*Returns*:

    base_type: the base type of the Enum
    allowed: List of allowed values of the Enum

#### \_enum\_katra

```python
def _enum_katra(typed, default=None, optional=False)
```

Private interface to create a Enum typed katra

A &#x27;katra&#x27; is the basic functional unit of `spock`. It defines a parameter using attrs as the backend, type checks
both simple types and subscripted GenericAlias types (e.g. lists and tuples), handles setting default parameters,
and deals with parameter optionality

*Args*:

    typed: the type of the parameter to define
    default: the default value to assign if given
    optional: whether to make the parameter optional or not (thus allowing None)

*Returns*:

    x: Attribute from attrs

#### \_enum\_base\_katra

```python
def _enum_base_katra(typed, base_type, allowed, default=None, optional=False)
```

Private interface to create a base Enum typed katra

Here we handle the base types of enums that allows us to force a type check on the instance

A &#x27;katra&#x27; is the basic functional unit of `spock`. It defines a parameter using attrs as the backend, type checks
both simple types and subscripted GenericAlias types (e.g. lists and tuples), handles setting default parameters,
and deals with parameter optionality

*Args*:
    typed: the type of the parameter to define
    base_type: underlying base type
    allowed: set of allowed values
    default: the default value to assign if given
    optional: whether to make the parameter optional or not (thus allowing None)

*Returns*:

    x: Attribute from attrs

#### \_in\_type

```python
def _in_type(instance, attribute, value, options)
```

attrs validator for class type enum

Checks if the type of the class (e.g. value) is in the specified set of types provided

*Args*:

    instance: current object instance
    attribute: current attribute instance
    value: current value trying to be set in the attrs instance
    options: list, tuple, or enum of allowed options

*Returns*:

#### \_enum\_class\_katra

```python
def _enum_class_katra(typed, allowed, default=None, optional=False)
```

Private interface to create a base Enum typed katra

Here we handle the class based types of enums. Seeing as these classes are generated dynamically we cannot
force type checking of a specific instance however the in_ validator will catch an incorrect instance type

A &#x27;katra&#x27; is the basic functional unit of `spock`. It defines a parameter using attrs as the backend, type checks
both simple types and subscripted GenericAlias types (e.g. lists and tuples), handles setting default parameters,
and deals with parameter optionality

*Args*:

    typed: the type of the parameter to define
    allowed: set of allowed values
    default: the default value to assign if given
    optional: whether to make the parameter optional or not (thus allowing None)

*Returns*:

    x: Attribute from attrs

#### \_type\_katra

```python
def _type_katra(typed, default=None, optional=False)
```

Private interface to create a simple typed katra

A &#x27;katra&#x27; is the basic functional unit of `spock`. It defines a parameter using attrs as the backend, type checks
both simple types and subscripted GenericAlias types (e.g. lists and tuples), handles setting default parameters,
and deals with parameter optionality

Handles: bool, string, float, int, List, and Tuple

*Args*:

    typed: the type of the parameter to define
    default: the default value to assign if given
    optional: whether to make the parameter optional or not (thus allowing None)

*Returns*:

    x: Attribute from attrs

#### \_handle\_optional\_typing

```python
def _handle_optional_typing(typed)
```

Handles when a type hint is Optional

Handles Optional[type] typing and strips out the base type to pass back to the creation of a katra which needs base
typing

*Args*:

    typed: type

*Returns*:

    typed: type (modified if Optional)
    optional: boolean for katra creation

#### \_check\_generic\_recursive\_single\_type

```python
def _check_generic_recursive_single_type(typed)
```

Checks generics for the single types -- mixed types of generics are not allowed

DEPRECATED -- NOW SUPPORTS MIXED TYPES OF TUPLES

*Args*:

    typed: type

*Returns*:

#### katra

```python
def katra(typed, default=None)
```

Public interface to create a katra

A &#x27;katra&#x27; is the basic functional unit of `spock`. It defines a parameter using attrs as the backend, type checks
both simple types and subscripted GenericAlias types (e.g. lists and tuples), handles setting default parameters,
and deals with parameter optionality

*Args*:

typed: the type of the parameter to define
default: the default value to assign if given
optional: whether to make the parameter optional or not (thus allowing None)

**Returns**:

  
- `x` - Attribute from attrs

