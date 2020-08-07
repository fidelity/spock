# -*- coding: utf-8 -*-

# Copyright 2019 FMR LLC <opensource@fidelity.com>
# SPDX-License-Identifier: Apache-2.0

"""Creates the spock config decorator that wraps dataclasses"""

from spock._dataclasses import dataclass


def spock_config(*args, **kwargs):
    """Wrapper to dataclass that forms the base of Spock configs

    *Args*:

        *args:
        **kwargs:

    *Returns*:

        frozen dataclass: frozen version of the dataclass
    """
    kwargs['frozen'] = True
    return dataclass(*args, **kwargs)
