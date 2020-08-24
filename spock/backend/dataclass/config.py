# -*- coding: utf-8 -*-

# Copyright 2019 FMR LLC <opensource@fidelity.com>
# SPDX-License-Identifier: Apache-2.0

"""Creates the spock config decorator that wraps dataclasses"""

import attr
from spock.backend.attr.typed import katra
from spock.backend.dataclass._dataclasses import dataclass
from typing import List
from typing import Optional
from typing import Tuple


TYPE_MAP = {
    'BoolArg': bool,
    'IntArg': int,
    'IntOptArg': Optional[int],
    'FloatArg': float,
    'FloatOptArg': Optional[float],
    'StrArg': str,
    'StrOptArg': Optional[str],
    'ListArg': List,
    'ListOptArg': Optional[List],
    'TupleArg': Tuple,
    'TupleOptArg': Optional[Tuple]
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
    kwargs['frozen'] = True
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
            else:
                default = None
            typed = TYPE_MAP.get(v.__name__)
            attrs_dict.update({k: katra(typed=typed, default=default)})
    return attrs_dict, bases
