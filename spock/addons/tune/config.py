# -*- coding: utf-8 -*-

# Copyright FMR LLC <opensource@fidelity.com>
# SPDX-License-Identifier: Apache-2.0

"""Creates the spock config interface that wraps attr -- tune version for hyper-parameters"""
import typing

import attr
from enum import Enum
from spock.backend.config import _base_attr
import sys
from typing import List, Optional, Tuple, Union


class _TypeEnum(Enum):
    int = 'int'
    float = 'float'


def _spock_tune(cls):
    """Ovverides basic spock_attr decorator with another name

    Using a different name allows spock to easily determine which parameters are normal and which are
    meant to be used in a hyper-parameter tuning backend

    *Args*:

        cls: basic class def

    *Returns*:

        cls: slotted attrs class that is frozen and kw only
    """
    bases, attrs_dict = _base_attr(cls)
    # Dynamically make an attr class
    obj = attr.make_class(name=cls.__name__, bases=bases, attrs=attrs_dict, kw_only=True, frozen=True)
    # For each class we dynamically create we need to register it within the system modules for pickle to work
    setattr(sys.modules['spock'].addons.tune.config, obj.__name__, obj)
    # Swap the __doc__ string from cls to obj
    obj.__doc__ = cls.__doc__
    return obj


# Make the alias for the decorator
spockTuner = _spock_tune


@attr.s(auto_attribs=True)
class RangeHyperParameter:
    type: _TypeEnum
    bounds: Tuple[Union[int, float], Union[int, float]]
    log_scale: bool


@attr.s(auto_attribs=True)
class ChoiceHyperParameter:
    choices: Union[List[int], List[float], List[str], List[bool]]
