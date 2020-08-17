# -*- coding: utf-8 -*-

# Copyright 2019 FMR LLC <opensource@fidelity.com>
# SPDX-License-Identifier: Apache-2.0

"""Creates the spock config interface that wraps attr"""

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
    attrs_dict = {}
    for k, v in cls.__annotations__.items():
        # If the cls has the attribute then a default was set
        if hasattr(cls, k):
            default = getattr(cls, k)
        else:
            default = None
        attrs_dict.update({k: katra(typed=v, default=default)})
    return attr.make_class(name=cls.__name__, attrs=attrs_dict, kw_only=True, frozen=True, slots=True)