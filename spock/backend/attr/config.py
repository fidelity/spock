# -*- coding: utf-8 -*-

# Copyright 2019 FMR LLC <opensource@fidelity.com>
# SPDX-License-Identifier: Apache-2.0

"""Creates the spock config interface that wraps attr"""

import sys
import attr
from spock.backend.attr.typed import katra


def spock_attr(cls):
    """Map type hints to katras

    Connector function that maps type hinting style to the defined katra style which uses the more strict
    attr.ib() definition

    *Args*:

        cls: basic class def

    *Returns*:

        cls: slotted attrs class that is frozen and kw only
    """

    # Since we are not using the @attr.s decorator we need to get the parent classes for inheritance
    # We do this by using the mro and grabbing anything that is not the first and last indices in the list and wrapping
    # it into a tuple
    if len(cls.__mro__[1:-1]) > 0:
        bases = tuple(cls.__mro__[1:-1])
    # if there are not parents pass a blank tuple
    else:
        bases = ()
    # Make a blank attrs dict for new attrs
    attrs_dict = {}
    if hasattr(cls, '__annotations__'):
        for k, v in cls.__annotations__.items():
            # If the cls has the attribute then a default was set
            if hasattr(cls, k):
                default = getattr(cls, k)
            else:
                default = None
            attrs_dict.update({k: katra(typed=v, default=default)})
    # For each class we dynamically create we need to register it within the system modules for pickle to work
    obj = attr.make_class(name=cls.__name__, bases=bases, attrs=attrs_dict, kw_only=True, frozen=True)
    setattr(sys.modules['spock'].backend.attr.config, obj.__name__, obj)
    return obj
