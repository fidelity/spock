---
sidebar_label: spaces
title: backend.spaces
---

Handles classes/named tuples for holding class, field, and attribute value(s)

## ConfigSpace Objects

```python
class ConfigSpace()
```

Class that holds information about the final values of spock class attributes

**Attributes**:

- `spock_cls` - reference to spock class to store information
- `fields` - dictionary of the current value of attributes

#### \_\_init\_\_

```python
def __init__(spock_cls: Type, fields: dict)
```

Init call for ConfigSpace class

**Arguments**:

- `spock_cls` - reference to spock class to store information
- `fields` - dictionary of the current value of attributes

#### name

```python
@property
def name() -> str
```

Returns the name of the spock class associated with ConfigSpace

## AttributeSpace Objects

```python
class AttributeSpace()
```

Class that holds information about a single attribute that is mapped to a ConfigSpace

**Attributes**:

- `config_space` - ConfigSpace that the attribute is contained in
- `attribute` - current Attribute class

#### \_\_init\_\_

```python
def __init__(attribute: Type[Attribute], config_space: ConfigSpace)
```

Init call for AttributeSpace class

**Arguments**:

- `config_space` - ConfigSpace that the attribute is contained in
- `attribute` - current Attribute class

#### field

```python
@property
def field()
```

Returns the field value from the ConfigSpace based on the attribute name

#### field

```python
@field.setter
def field(value)
```

Setter for the field value from the ConfigSpace based on the attribute name

