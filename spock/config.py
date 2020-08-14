# -*- coding: utf-8 -*-

# Copyright 2019 FMR LLC <opensource@fidelity.com>
# SPDX-License-Identifier: Apache-2.0

"""Creates the spock config decorator that wraps dataclasses"""

from attr import make_class
from spock._dataclasses import dataclass
from spock.attr_backend.typed import katra


def _spock_dataclass(*args, **kwargs):
    """Wrapper to dataclass that forms the base of Spock configs

    *Args*:

        *args:
        **kwargs:

    *Returns*:

        frozen dataclass: frozen version of the dataclass
    """
    kwargs['frozen'] = True
    return dataclass(*args, **kwargs)


def _spock_attrs(cls):
    """Wrapper to attrs that forms the base of Spock configs

    *Args*:

        cls: basic class def

    *Returns*:

        cls: slotted attrs class that is frozen and kw only
    """
    return _hints_to_katras(cls)


def _hints_to_katras(cls):
    """Map type hints to katras

    Connector function that maps type hinting style to the defined katra style which uses the more strict
    attr.ib() definition

    *Args*:

        cls: basic class def

    *Returns*:

        cls: slotted attrs class that is frozen and kw only
    """
    attrs_dict = {}
    for k, v in cls.__annotations__.items():
        # If the cls has the attribute then a default was set
        if hasattr(cls, k):
            default = getattr(cls, k)
        else:
            default = None
        attrs_dict.update({k: katra(typed=v, default=default)})
    return make_class(name=cls.__name__, attrs=attrs_dict, kw_only=True, frozen=True, slots=True)


# For legacy support
spock_config = _spock_dataclass

# Simplified decorator
spock = _spock_attrs
