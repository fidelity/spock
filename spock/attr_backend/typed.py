# -*- coding: utf-8 -*-

# Copyright 2019 FMR LLC <opensource@fidelity.com>
# SPDX-License-Identifier: Apache-2.0

"""Handles the definitions of arguments types for Spock (backend: attrs)"""

import attr
from enum import Enum
from typing import List
from typing import Tuple


class SpockTypes(Enum):
    BOOL = bool
    STRING = str
    FLOAT = float
    INT = int
    LIST = List
    LIST_INT = List[int]
    LIST_FLOAT = List[float]
    LIST_STRING = List[str]
    LIST_LIST = List[List]
    LIST_TUPLE = List[Tuple]
    TUPLE = Tuple
    TUPLE_INT = Tuple[int]
    TUPLE_FLOAT = Tuple[float]
    TUPLE_STRING = Tuple[str]
    TUPLE_LIST = Tuple[List]
    TUPLE_TUPLE = Tuple[Tuple]


def _validate_subscripted_generic(_, attribute, value):
    """Validator for subscripted GenericAlias types

    Checks that the values set for the Attribute match the subscripted GenericAlias type

    Args:
        _: instance (unused)
        attribute: Attribute type
        value: current value

    Returns:

    """
    if not all([type(val).__name__ == attribute.metadata['type'] for val in value]):
        raise TypeError(f"Incorrect value subscript type passed to katra {attribute.name} of "
                        f"type {type(value).__name__}: Must be of type {attribute.metadata['type']}")


def _extract_base_type(typed):
    """Extracts the name of the type from a _GenericAlias

    *Args*:

        typed: the type of the parameter

    *Returns*:

        name of type
    """
    return typed.value.__args__[0].__name__


def _generic_alias_katra(typed: SpockTypes, default=None, optional=False):
    """Private interface to create a subscripted generic_alias katra

    A 'katra' is the basic functional unit of `spock`. It defines a parameter using attrs as the backend, type checks
    both simple types and subscripted GenericAlias types (e.g. lists and tuples), handles setting default parameters,
    and deals parameter optionality

    Handles: List[type] and Tuple[type]

    *Args*:

        typed: the type of the parameter to define
        default: the default value to assign if given
        optional: whether to make the parameter optional or not (thus allowing None)

    *Returns*:

        x: Attribute from attrs

    """
    base_typed = SpockTypes[typed.value._name.upper()].value
    if optional and default:
        x = attr.ib(validator=[attr.validators.optional(attr.validators.instance_of(base_typed)),
                               _validate_subscripted_generic], default=default, type=base_typed,
                    metadata={'type': _extract_base_type(typed)})
    elif optional:
        x = attr.ib(validator=[attr.validators.optional(attr.validators.instance_of(base_typed)),
                               _validate_subscripted_generic], type=base_typed,
                    metadata={'type': _extract_base_type(typed)})
    elif default:
        x = attr.ib(validator=[attr.validators.instance_of(base_typed), _validate_subscripted_generic],
                    default=default, type=base_typed, metadata={'type': _extract_base_type(typed)})
    else:
        x = attr.ib(validator=[attr.validators.instance_of(base_typed), _validate_subscripted_generic],
                    type=base_typed, metadata={'type': _extract_base_type(typed)})
    return x


def _type_katra(typed: SpockTypes, default=None, optional=False):
    """Private interface to create a simple typed katra

    A 'katra' is the basic functional unit of `spock`. It defines a parameter using attrs as the backend, type checks
    both simple types and subscripted GenericAlias types (e.g. lists and tuples), handles setting default parameters,
    and deals parameter optionality

    Handles: bool, string, float, int, List, and Tuple

    *Args*:

        typed: the type of the parameter to define
        default: the default value to assign if given
        optional: whether to make the parameter optional or not (thus allowing None)

    *Returns*:

        x: Attribute from attrs

    """
    # Default booleans to false and optional due to the nature of a boolean
    if type(typed.value) == type and typed.value.__name__ == "bool":
        optional = True
        default = False
    if optional and default is not None:
        x = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(typed.value)), default=default)
    elif optional:
        x = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(typed.value)))
    elif default is not None:
        x = attr.ib(validator=attr.validators.instance_of(typed.value), default=default)
    else:
        x = attr.ib(validator=attr.validators.instance_of(typed.value), type=typed.value)
    return x


def katra(typed: SpockTypes, default=None, optional=False):
    """Public interface to create a katra

    A 'katra' is the basic functional unit of `spock`. It defines a parameter using attrs as the backend, type checks
    both simple types and subscripted GenericAlias types (e.g. lists and tuples), handles setting default parameters,
    and deals parameter optionality

    *Args*:

        typed: the type of the parameter to define
        default: the default value to assign if given
        optional: whether to make the parameter optional or not (thus allowing None)

    Returns:

        x: Attribute from attrs

    """
    # We need to check if the type is a _GenericAlias so that we can handle subscripted general types
    # The second check is to see if the generic type is subscript typed
    # If it is typed it will not be T which python uses as a generic type name
    if type(typed.value).__name__ == '_GenericAlias' and typed.value.__args__[0].__name__ != "T":
        x = _generic_alias_katra(typed=typed, default=default, optional=optional)
    else:
        x = _type_katra(typed=typed, default=default, optional=optional)
    return x
