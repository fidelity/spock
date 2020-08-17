# -*- coding: utf-8 -*-

# Copyright 2019 FMR LLC <opensource@fidelity.com>
# SPDX-License-Identifier: Apache-2.0

"""Dataclass utility functions for Spock"""

from copy import copy
from typing import List
from typing import Tuple
from spock.backend.dataclass._dataclasses import field


def cast(x):
    """Recasts lists as tuples

    *Args*:

        x: object

    *Returns*:

        x: object or object recast as Tuple
    """
    if isinstance(x, list):
        x = tuple(x)
    return x


def _def_list(values: List):
    """Creates a list of default values for List datatype that is mutable

    *Args*:

        values: default list

    Returns:

        list built from default factory

    """
    return field(default_factory=lambda: copy(values))


def _def_tuple(values: Tuple):
    """Creates a tuple of default values for Tuple datatype that is mutable

        *Args*:

            values: default tuple

        Returns:

            tuple built from default factory

        """
    return field(default_factory=lambda: copy(values))
