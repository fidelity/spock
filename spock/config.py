# -*- coding: utf-8 -*-

# Copyright 2019 FMR LLC <opensource@fidelity.com>
# SPDX-License-Identifier: Apache-2.0

"""Creates the spock config decorator that wraps dataclasses"""
from attr import s
from spock._dataclasses import dataclass


def spock_dataclass(*args, **kwargs):
    """Wrapper to dataclass that forms the base of Spock configs

    *Args*:

        *args:
        **kwargs:

    *Returns*:

        frozen dataclass: frozen version of the dataclass
    """
    kwargs['frozen'] = True
    return dataclass(*args, **kwargs)


def spock(cls):
    """Wrapper to attrs that forms the base of Spock configs

    *Args*:

        cls: basic class def

    *Returns*:

        cls: slotted attrs class that is frozen and kw only
    """
    return s(cls, auto_attribs=True, kw_only=True, frozen=True, slots=True)


# For legacy support
spock_config = spock_dataclass
