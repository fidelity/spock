# -*- coding: utf-8 -*-

# Copyright 2019 FMR LLC <opensource@fidelity.com>
# SPDX-License-Identifier: Apache-2.0

"""Creates the spock config decorator that wraps dataclasses - now an adapter to attr"""

import attr
import enum
from inspect import isfunction
from spock.backend.attr.typed import katra
from spock.backend.attr.typed import SavePath
from spock.backend.dataclass._dataclasses import dataclass
from typing import List
from typing import Optional
from typing import Tuple


def _enum_adapter(key, obj):
    enum_set = {('option_' + str(idx)): val for idx, val in enumerate(obj.choice_set)}
    enum_obj = enum.Enum(key, enum_set)
    return enum_obj


def _list_adapter(key, obj):
    return List[obj.__args__[0]]


def _list_optional_adapter(key, obj):
    return Optional[List[obj.__args__[0]]]


def _tuple_adapter(key, obj):
    return Tuple[obj.__args__[0]]


def _tuple_optional_adapter(key, obj):
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
