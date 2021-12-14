---
sidebar_label: field_handlers
title: backend.field_handlers
---

Handles registering field attributes for spock classes -- deals with the recursive nature of dependencies

## SpockInstantiationError Objects

```python
class SpockInstantiationError(Exception)
```

Custom exception for when the spock class cannot be instantiated correctly

## SpockNotOptionalError Objects

```python
class SpockNotOptionalError(Exception)
```

Custom exception for missing value

## RegisterFieldTemplate Objects

```python
class RegisterFieldTemplate(ABC)
```

Base class for handing different field types

Once the configuration dictionary has been assembled from the config file and the command line then we need to
map these values to the correct spock classes -- seeing as different types need to be handled differently and
recursive calls might be needed (when referencing other spock classes) classes derived from RegisterFieldTemplate
handle the logic for making sure the argument dictionary passes to the instantiation of each spock class is
correct

**Attributes**:

- `special_keys` - dictionary to check special keys

#### \_\_init\_\_

```python
def __init__()
```

Init call for RegisterFieldTemplate class

**Arguments**:


#### \_\_call\_\_

```python
def __call__(attr_space: AttributeSpace, builder_space: BuilderSpace)
```

Call method for RegisterFieldTemplate

Handles calling the correct method for the type of the attribute

**Arguments**:

- `attr_space` - holds information about a single attribute that is mapped to a ConfigSpace
- `builder_space` - named_tuple containing the arguments and spock_space
  

**Returns**:


#### \_is\_attribute\_in\_config\_arguments

```python
@staticmethod
def _is_attribute_in_config_arguments(attr_space: AttributeSpace, arguments: SpockArguments)
```

Checks if an attribute is in the configuration file or keyword arguments dictionary

**Arguments**:

- `attr_space` - holds information about a single attribute that is mapped to a ConfigSpace
- `arguments` - map of the read/cmd-line parameter dictionary to general or class level arguments
  

**Returns**:

  boolean if in dictionary

#### \_is\_attribute\_optional

```python
@staticmethod
def _is_attribute_optional(attribute: Type[Attribute])
```

Checks if an attribute is allowed to be optional

**Arguments**:

- `attribute` - current attribute class
  

**Returns**:

  boolean if the optional state is allowed

#### handle\_optional\_attribute\_value

```python
def handle_optional_attribute_value(attr_space: AttributeSpace, builder_space: BuilderSpace)
```

Handles setting an optional value with its default

**Arguments**:

- `attr_space` - holds information about a single attribute that is mapped to a ConfigSpace
- `builder_space` - named_tuple containing the arguments and spock_space
  

**Returns**:


## RegisterList Objects

```python
class RegisterList(RegisterFieldTemplate)
```

Class that registers list types

**Attributes**:

- `special_keys` - dictionary to check special keys

#### \_\_init\_\_

```python
def __init__()
```

Init call to RegisterList

**Arguments**:


#### handle\_attribute\_from\_config

```python
def handle_attribute_from_config(attr_space: AttributeSpace, builder_space: BuilderSpace)
```

Handles a list of spock config classes (aka repeated classes)

**Arguments**:

- `attr_space` - holds information about a single attribute that is mapped to a ConfigSpace
- `builder_space` - named_tuple containing the arguments and spock_space
  

**Returns**:


#### handle\_optional\_attribute\_type

```python
def handle_optional_attribute_type(attr_space: AttributeSpace, builder_space: BuilderSpace)
```

Handles a list of spock config classes (aka repeated classes) if it is optional

**Arguments**:

- `attr_space` - holds information about a single attribute that is mapped to a ConfigSpace
- `builder_space` - named_tuple containing the arguments and spock_space
  

**Returns**:


#### handle\_optional\_attribute\_value

```python
def handle_optional_attribute_value(attr_space: AttributeSpace, builder_space: BuilderSpace)
```

Handles setting the value for an optional basic attribute

**Arguments**:

- `attr_space` - holds information about a single attribute that is mapped to a ConfigSpace
- `builder_space` - named_tuple containing the arguments and spock_space
  

**Returns**:


#### \_process\_list

```python
@staticmethod
def _process_list(spock_cls, builder_space: BuilderSpace)
```

Rolls up repeated classes into the expected list format

**Arguments**:

- `spock_cls` - current spock class
- `builder_space` - named_tuple containing the arguments and spock_space
  

**Returns**:

  list of rolled up repeated spock classes

## RegisterEnum Objects

```python
class RegisterEnum(RegisterFieldTemplate)
```

Class that registers enum types

**Attributes**:

- `special_keys` - dictionary to check special keys

#### \_\_init\_\_

```python
def __init__()
```

Init call to RegisterEnum

**Arguments**:


#### handle\_attribute\_from\_config

```python
def handle_attribute_from_config(attr_space: AttributeSpace, builder_space: BuilderSpace)
```

Handles getting the attribute set value when the Enum is made up of spock classes

**Arguments**:

- `attr_space` - holds information about a single attribute that is mapped to a ConfigSpace
- `builder_space` - named_tuple containing the arguments and spock_space
  

**Returns**:


#### handle\_optional\_attribute\_type

```python
def handle_optional_attribute_type(attr_space: AttributeSpace, builder_space: BuilderSpace)
```

Handles falling back on the optional default for a type based attribute

**Arguments**:

- `attr_space` - holds information about a single attribute that is mapped to a ConfigSpace
- `builder_space` - named_tuple containing the arguments and spock_space
  

**Returns**:


#### \_handle\_and\_register\_enum

```python
def _handle_and_register_enum(enum_cls, attr_space: AttributeSpace, builder_space: BuilderSpace)
```

Recurses the enum in case there are nested type definitions

**Arguments**:

- `enum_cls` - current enum class
- `attr_space` - holds information about a single attribute that is mapped to a ConfigSpace
- `builder_space` - named_tuple containing the arguments and spock_space
  

**Returns**:


## RegisterSimpleField Objects

```python
class RegisterSimpleField(RegisterFieldTemplate)
```

Class that registers basic python types

**Attributes**:

- `special_keys` - dictionary to check special keys

#### \_\_init\_\_

```python
def __init__()
```

Init call to RegisterSimpleField

**Arguments**:


#### handle\_attribute\_from\_config

```python
def handle_attribute_from_config(attr_space: AttributeSpace, builder_space: BuilderSpace)
```

Handles setting a simple attribute when it is a spock class type

**Arguments**:

- `attr_space` - holds information about a single attribute that is mapped to a ConfigSpace
- `builder_space` - named_tuple containing the arguments and spock_space
  

**Returns**:


#### handle\_optional\_attribute\_type

```python
def handle_optional_attribute_type(attr_space: AttributeSpace, builder_space: BuilderSpace)
```

Not implemented for this type

**Arguments**:

- `attr_space` - holds information about a single attribute that is mapped to a ConfigSpace
- `builder_space` - named_tuple containing the arguments and spock_space
  

**Raises**:

  SpockNotOptionalError

#### handle\_optional\_attribute\_value

```python
def handle_optional_attribute_value(attr_space: AttributeSpace, builder_space: BuilderSpace)
```

Handles setting the attribute from default if optional

Also checks for clashes with special keys

**Arguments**:

- `attr_space` - holds information about a single attribute that is mapped to a ConfigSpace
- `builder_space` - named_tuple containing the arguments and spock_space
  

**Returns**:


#### register\_special\_key

```python
def register_special_key(attr_space: AttributeSpace)
```

Registers a special key if it is found in the attribute metadata

**Arguments**:

- `attr_space` - holds information about a single attribute that is mapped to a ConfigSpace
  

**Returns**:


## RegisterTuneCls Objects

```python
class RegisterTuneCls(RegisterFieldTemplate)
```

Class that registers spock tune classes

**Attributes**:

- `special_keys` - dictionary to check special keys

#### \_\_init\_\_

```python
def __init__()
```

Init call to RegisterTuneCls

**Arguments**:


#### \_attr\_type

```python
@staticmethod
def _attr_type(attr_space: AttributeSpace)
```

Gets the attribute type

**Arguments**:

- `attr_space` - holds information about a single attribute that is mapped to a ConfigSpace
  

**Returns**:

  the type of the attribute

#### handle\_attribute\_from\_config

```python
def handle_attribute_from_config(attr_space: AttributeSpace, builder_space: BuilderSpace)
```

Handles when the spock tune class is made up of spock classes

**Arguments**:

- `attr_space` - holds information about a single attribute that is mapped to a ConfigSpace
- `builder_space` - named_tuple containing the arguments and spock_space
  

**Returns**:


#### handle\_optional\_attribute\_value

```python
def handle_optional_attribute_value(attr_space: AttributeSpace, builder_space: BuilderSpace)
```

Not implemented for this type

**Arguments**:

- `attr_space` - holds information about a single attribute that is mapped to a ConfigSpace
- `builder_space` - named_tuple containing the arguments and spock_space
  

**Raises**:

  SpockNotOptionalError

#### handle\_optional\_attribute\_type

```python
def handle_optional_attribute_type(attr_space: AttributeSpace, builder_space: BuilderSpace)
```

Not implemented for this type

**Arguments**:

- `attr_space` - holds information about a single attribute that is mapped to a ConfigSpace
- `builder_space` - named_tuple containing the arguments and spock_space
  

**Raises**:

  SpockNotOptionalError

## RegisterSpockCls Objects

```python
class RegisterSpockCls(RegisterFieldTemplate)
```

Class that registers attributes within a spock class

Might be called recursively so it has methods to deal with spock classes when invoked via the __call__ method

**Attributes**:

- `special_keys` - dictionary to check special keys

#### \_\_init\_\_

```python
def __init__()
```

Init call to RegisterSpockCls

**Arguments**:


#### \_attr\_type

```python
@staticmethod
def _attr_type(attr_space: AttributeSpace)
```

Gets the attribute type

**Arguments**:

- `attr_space` - holds information about a single attribute that is mapped to a ConfigSpace
  

**Returns**:

  the type of the attribute

#### handle\_attribute\_from\_config

```python
def handle_attribute_from_config(attr_space: AttributeSpace, builder_space: BuilderSpace)
```

Handles when the attribute is made up of a spock class or classes

Calls the recurse_generate function which handles nesting of spock classes

**Arguments**:

- `attr_space` - holds information about a single attribute that is mapped to a ConfigSpace
- `builder_space` - named_tuple containing the arguments and spock_space
  

**Returns**:


#### handle\_optional\_attribute\_value

```python
def handle_optional_attribute_value(attr_space: AttributeSpace, builder_space: BuilderSpace)
```

Handles when the falling back onto the default for the attribute of spock class type and the field value
already exits within the attr_space

**Arguments**:

- `attr_space` - holds information about a single attribute that is mapped to a ConfigSpace
- `builder_space` - named_tuple containing the arguments and spock_space
  

**Returns**:


#### handle\_optional\_attribute\_type

```python
def handle_optional_attribute_type(attr_space: AttributeSpace, builder_space: BuilderSpace)
```

Handles when the falling back onto the default for the attribute of spock class type

Calls the recurse_generate function which handles nesting of spock classes -- to make sure the attr_space.field
value is defined

**Arguments**:

- `attr_space` - holds information about a single attribute that is mapped to a ConfigSpace
- `builder_space` - named_tuple containing the arguments and spock_space
  

**Returns**:


#### recurse\_generate

```python
@classmethod
def recurse_generate(cls, spock_cls, builder_space: BuilderSpace)
```

Call on a spock classes to iterate through the attrs attributes and handle each based on type and optionality

Triggers a recursive call when an attribute refers to another spock classes

**Arguments**:

- `spock_cls` - current spock class that is being handled
- `builder_space` - named_tuple containing the arguments and spock_space
  

**Returns**:

  tuple of the instantiated spock class and the dictionary of special keys

