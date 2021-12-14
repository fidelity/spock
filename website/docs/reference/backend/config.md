---
sidebar_label: config
title: backend.config
---

Creates the spock config interface that wraps attr

#### \_base\_attr

```python
def _base_attr(cls)
```

Map type hints to katras

Connector function that maps type hinting style to the defined katra style which uses the more strict
attr.ib() definition

*Args*:

    cls: basic class def

*Returns*:

    cls: slotted attrs class that is frozen and kw only

#### spock\_attr

```python
def spock_attr(cls)
```

Map type hints to katras

Connector function that maps type hinting style to the defined katra style which uses the more strict
attr.ib() definition

*Args*:

    cls: basic class def

*Returns*:

    cls: slotted attrs class that is frozen and kw only

