---
sidebar_label: graph
title: graph
---

Handles creation and ops for DAGs

## Graph Objects

```python
class Graph()
```

Class that holds graph methods for determining dependencies between spock classes

**Attributes**:

- `_input_classes` - list of input classes that link to a backend
- `_dag` - graph of the dependencies between spock classes

#### \_\_init\_\_

```python
def __init__(input_classes)
```

Init call for Graph class

**Arguments**:

- `input_classes` - list of input classes that link to a backend

#### nodes

```python
@property
def nodes()
```

Returns the node names/input_classes

#### roots

```python
@property
def roots()
```

Returns the roots of the dependency graph

#### \_build

```python
def _build()
```

Builds a dictionary of nodes and their edges (essentially builds the DAG)

**Returns**:

  dictionary of nodes and their edges

#### \_find\_all\_spock\_classes

```python
def _find_all_spock_classes(attr_class: Type)
```

Within a spock class determine if there are any references to other spock classes

**Arguments**:

- `attr_class` - a class with attrs attributes
  

**Returns**:

  list of dependent spock classes

#### \_check\_4\_spock\_iterable

```python
@staticmethod
def _check_4_spock_iterable(iter_obj: Union[tuple, list])
```

Checks if an iterable type contains a spock class

**Arguments**:

- `iter_obj` - iterable type
  

**Returns**:

  boolean if the iterable contains at least one spock class

#### \_get\_enum\_classes

```python
@staticmethod
def _get_enum_classes(enum_obj: EnumMeta)
```

Checks if any of the values of an enum are spock classes and adds to a list

**Arguments**:

- `enum_obj` - enum class
  

**Returns**:

  list of enum values that are spock classes

#### \_has\_cycles

```python
def _has_cycles()
```

Uses DFS to check for cycles within the spock dependency graph

**Returns**:

  boolean if a cycle is found

#### \_cycle\_dfs

```python
def _cycle_dfs(node: Type, visited: dict, recursion_stack: dict)
```

DFS via a recursion stack for cycles

**Arguments**:

- `node` - current graph node (spock class type)
- `visited` - dictionary of visited nodes
- `recursion_stack` - dictionary that is the recursion stack that is used to find cycles
  

**Returns**:

  boolean if a cycle is found

