---
sidebar_label: args
title: args
---

Handles mapping config arguments to a payload with both general and class specific sets

## SpockArguments Objects

```python
class SpockArguments()
```

Class that handles mapping the read parameter dictionary to general or class level arguments

**Attributes**:

- `_arguments` - dictionary of arguments

#### \_\_init\_\_

```python
def __init__(arguments: dict, config_dag: Graph)
```

Init call for SpockArguments class

Handles creating a clean arguments dictionary that can be cleanly mapped to spock classes

**Arguments**:

- `arguments` - dictionary of parameters from the config file(s)
- `config_dag` - graph of the dependencies between spock classes

#### \_\_getitem\_\_

```python
def __getitem__(key: str)
```

Gets value from the _arguments dictionary

**Arguments**:

- `key` - dictionary key
  

**Returns**:

  argument at the specified key

#### \_\_iter\_\_

```python
def __iter__()
```

Returns the next value of the keys within the _arguments dictionary

**Returns**:

  current key for the _arguments dictionary

#### items

```python
@property
def items()
```

Returns the k,v tuple iterator for the _arguments dictionary

#### keys

```python
@property
def keys()
```

Returns an iterator for the keys of the _arguments dictionary

#### values

```python
@property
def values()
```

Returns an iterator for the values of the _arguments dictionary

#### \_get\_general\_arguments

```python
@staticmethod
def _get_general_arguments(arguments: dict, config_dag: Graph)
```

Creates a dictionary of config file parameters that are defined at the general level (not class specific)

**Arguments**:

- `arguments` - dictionary of parameters from the config file(s)
- `config_dag` - graph of the dependencies between spock classes
  

**Returns**:

  dictionary of general level parameters

#### \_attribute\_name\_to\_config\_name\_mapping

```python
def _attribute_name_to_config_name_mapping(config_dag: Graph, general_arguments: dict)
```

Returns a mapping of names to spock config class parameter names

**Arguments**:

- `config_dag` - graph of the dependencies between spock classes
- `general_arguments` - dictionary of arguments at the general level
  

**Returns**:

  dictionary of parameters mapped to spock classes

#### \_is\_duplicated\_key

```python
@staticmethod
def _is_duplicated_key(attribute_name_to_config_name_mapping: dict, attr_name: str, config_name: str)
```

Checks if a duplicated key exists in multiple classes

**Arguments**:

- `attribute_name_to_config_name_mapping` - dictionary of class specific name mappings
  attr_name:
  config_name:
  

**Returns**:

  boolean if duplicated

#### \_assign\_general\_arguments\_to\_config

```python
def _assign_general_arguments_to_config(general_arguments: dict, attribute_name_to_config_name_mapping: dict)
```

Assigns the values from general definitions to values within specific classes if the specific definition
doesn&#x27;t exist

**Arguments**:

  general_arguments:
  attribute_name_to_config_name_mapping:
  

**Returns**:

  None

#### \_clean\_arguments

```python
@staticmethod
def _clean_arguments(arguments: dict, general_arguments: dict)
```

Sets up a clean dictionary for those not in the general dictionary

**Arguments**:

- `arguments` - dictionary of all arguments
- `general_arguments` - dictionary of general level arguments
  

**Returns**:

  clean dictionary of parameters not at the general level

## SpockDuplicateArgumentError Objects

```python
class SpockDuplicateArgumentError(Exception)
```

Custom exception type for duplicated values

