# -*- coding: utf-8 -*-

# Copyright 2019 FMR LLC <opensource@fidelity.com>
# SPDX-License-Identifier: Apache-2.0

"""Creates the spock config decorator that wraps dataclasses - now an adapter to attr"""

import enum
from inspect import isfunction
from typing import List
from typing import Optional
from typing import Tuple
import attr
from spock.backend.attr.typed import katra
from spock.backend.attr.typed import SavePath
from spock.backend.dataclass._dataclasses import dataclass


def _enum_adapter(key, obj):
    """Adapter for ChoiceSet to Enum

    *Args*:

        key: name of enum
        obj: values in the ChoiceSet

    Returns:

        enum_obj: constructed enum object

    """
    enum_set = {('option_' + str(idx)): val for idx, val in enumerate(obj.choice_set)}
    enum_obj = enum.Enum(key, enum_set)
    return enum_obj


def _list_adapter(_, obj):
    """Adapter for List types

    *Args*:

        _: unused
        obj: old list type

    Returns:

        List type

    """
    return List[obj.__args__[0]]


def _list_optional_adapter(_, obj):
    """Adapter for Optional List types

    *Args*:

        _: unused
        obj: old list type

    Returns:

        Optional List type

    """
    return Optional[List[obj.__args__[0]]]


def _tuple_adapter(_, obj):
    """Adapter for Tuple types

    *Args*:

        _: unused
        obj: old tuple type

    Returns:

        Tuple type

    """
    return Tuple[obj.__args__[0]]


def _tuple_optional_adapter(_, obj):
    """Adapter for Optional Tuple types

    *Args*:

        _: unused
        obj: old tuple type

    Returns:

        Optional Tuple type

    """
    return Optional[Tuple[obj.__args__[0]]]


TYPE_MAP = {
    'BoolArg': bool,
    'IntArg': int,
    'IntOptArg': Optional[int],
    'FloatArg': float,
    'FloatOptArg': Optional[float],
    'StrArg': str,
    'StrOptArg': Optional[str],
    'ListArg': _list_adapter,
    'ListOptArg': _list_optional_adapter,
    'TupleArg': _tuple_adapter,
    'TupleOptArg': _tuple_optional_adapter,
    'SavePathOptArg': SavePath,
    'ChoiceArg': _enum_adapter
}


def spock_legacy_dataclass(*args, **kwargs):
    """Wrapper to dataclass that forms the base of Spock configs
    *Args*:
        *args:
        **kwargs:
    *Returns*:
        frozen dataclass: frozen version of the dataclass
    """
    kwargs['frozen'] = True
    return dataclass(*args, **kwargs)


def spock_dataclass(*args, **kwargs):
    """Wrapper to dataclass that forms the base of Spock configs

    *Args*:

        *args:
        **kwargs:

    *Returns*:

        frozen dataclass: frozen version of the dataclass
    """
    cls = args[0]
    # Use the adaptor to convert into the attr class
    attrs_dict, bases = _adapter(cls=cls)
    return attr.make_class(name=cls.__name__, bases=bases, attrs=attrs_dict, kw_only=True, frozen=True)


def _adapter(cls):
    """Takes a class an adapts the dataclass backend to the attr backend

    Maps the old interface and backend of dataclasses to the new interface and backend of attrs. Based on a type map
    dictionary and mapping functions it provides the ability to 1:1 map between inferfaces.

    *Args*:

        cls: input class

    *Returns*:

        attrs_dict: a dictionary of current attributes to make
        bases: any base classes to inherit from

    """
    # Make a blank attrs dict for new attrs
    attrs_dict = {}
    # We are mapping to the attr backend thus we need to get the parent classes for inheritance
    # We do this by using the mro and grabbing anything that is not the first and last indices in the list and wrapping
    # it into a tuple
    if len(cls.__mro__[1:-1]) > 0:
        bases = tuple(cls.__mro__[1:-1])
    # if there are not parents pass a blank tuple
    else:
        bases = ()
    if hasattr(cls, '__annotations__'):
        for k, v in cls.__annotations__.items():
            # If the cls has the attribute then a default was set
            if hasattr(cls, k):
                default = getattr(cls, k)
            elif hasattr(v, 'default'):
                default = getattr(v, 'default')
            else:
                default = None
            if hasattr(v, '__name__'):
                typed = TYPE_MAP.get(v.__name__)
            elif hasattr(v, '__origin__'):
                typed = TYPE_MAP.get(v.__origin__.__name__)
            else:
                typed = TYPE_MAP.get(type(v).__name__)
            if isfunction(typed):
                typed = typed(k, v)
            attrs_dict.update({k: katra(typed=typed, default=default)})
    return attrs_dict, bases
