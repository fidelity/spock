# -*- coding: utf-8 -*-

# Copyright 2019 FMR LLC <opensource@fidelity.com>
# SPDX-License-Identifier: Apache-2.0

"""Handles the definitions of arguments types for Spock (backend: attrs)"""

import attr
from enum import EnumMeta
from typing import _GenericAlias
from typing import Union


def _validate_subscripted_generic(_, attribute, value):
    """Validator for subscripted GenericAlias types

    Checks that the values set for the Attribute match the subscripted GenericAlias type

    Args:
        _: instance (unused)
        attribute: Attribute type
        value: current value

    Returns:

    """
    if 'optional' not in attribute.metadata and value is not None:
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
    return typed.__args__[0].__name__


def _generic_alias_katra(typed, default=None, optional=False):
    """Private interface to create a subscripted generic_alias katra

    A 'katra' is the basic functional unit of `spock`. It defines a parameter using attrs as the backend, type checks
    both simple types and subscripted GenericAlias types (e.g. lists and tuples), handles setting default parameters,
    and deals with parameter optionality

    Handles: List[type] and Tuple[type]

    *Args*:

        typed: the type of the parameter to define
        default: the default value to assign if given
        optional: whether to make the parameter optional or not (thus allowing None)

    *Returns*:

        x: Attribute from attrs

    """
    # base python class from which a GenericAlias is derived
    base_typed = typed.__origin__
    if default is not None:
        x = attr.ib(validator=attr.validators.deep_iterable(
            member_validator=attr.validators.instance_of(typed.__args__[0]),
            iterable_validator=attr.validators.instance_of(base_typed)
        ), type=base_typed, default=default, metadata={'type': _extract_base_type(typed), 'base': typed._name})
    elif optional:
        # if there's no default, but marked as optional, then set the default to None
        x = attr.ib(validator=attr.validators.optional(attr.validators.deep_iterable(
            member_validator=attr.validators.instance_of(typed.__args__[0]),
            iterable_validator=attr.validators.instance_of(base_typed)
        )), type=base_typed, default=default,
            metadata={'type': _extract_base_type(typed), 'optional': True, 'base': typed._name})
    else:
        x = attr.ib(validator=attr.validators.deep_iterable(
            member_validator=attr.validators.instance_of(typed.__args__[0]),
            iterable_validator=attr.validators.instance_of(base_typed)
        ), type=base_typed, metadata={'type': _extract_base_type(typed), 'base': typed._name})
    return x


def _enum_katra(typed, default=None, optional=False):
    """Private interface to create a Enum typed katra

    A 'katra' is the basic functional unit of `spock`. It defines a parameter using attrs as the backend, type checks
    both simple types and subscripted GenericAlias types (e.g. lists and tuples), handles setting default parameters,
    and deals with parameter optionality

    *Args*:

        typed: the type of the parameter to define
        default: the default value to assign if given
        optional: whether to make the parameter optional or not (thus allowing None)

    *Returns*:

        x: Attribute from attrs

    """
    # First check if the types of Enum are the same
    type_set = {type(val.value) for val in typed}
    if len(type_set) > 1:
        raise TypeError(f"Enum cannot be defined with multiple types: {type_set}")
    base_type = list(type_set)[-1]
    allowed = [val.value for val in typed]
    if default is not None:
        x = attr.ib(
            validator=[attr.validators.instance_of(base_type), attr.validators.in_(allowed)],
            default=default, type=base_type, metadata={'base': typed.__name__})
    elif optional:
        x = attr.ib(
            validator=attr.validators.optional([attr.validators.instance_of(base_type), attr.validators.in_(allowed)]),
            default=default, type=base_type, metadata={'base': typed.__name__})
    else:
        x = attr.ib(validator=[attr.validators.instance_of(base_type), attr.validators.in_(allowed)], type=typed,
                    metadata={'base': typed.__name__})
    return x


def _type_katra(typed, default=None, optional=False):
    """Private interface to create a simple typed katra

    A 'katra' is the basic functional unit of `spock`. It defines a parameter using attrs as the backend, type checks
    both simple types and subscripted GenericAlias types (e.g. lists and tuples), handles setting default parameters,
    and deals with parameter optionality

    Handles: bool, string, float, int, List, and Tuple

    *Args*:

        typed: the type of the parameter to define
        default: the default value to assign if given
        optional: whether to make the parameter optional or not (thus allowing None)

    *Returns*:

        x: Attribute from attrs

    """
    # Default booleans to false and optional due to the nature of a boolean
    if isinstance(typed, type) and typed.__name__ == "bool":
        optional = True
        default = False
    if default is not None:
        # if a default is provided, that takes precedence
        x = attr.ib(validator=attr.validators.instance_of(typed), default=default, type=typed,
                    metadata={'base': typed.__name__})
    elif optional:
        x = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(typed)), default=default, type=typed,
                    metadata={'optional': True, 'base': typed.__name__})
    else:
        x = attr.ib(validator=attr.validators.instance_of(typed), type=typed, metadata={'base': typed.__name__})
    return x


def _handle_optional_typing(typed):
    """Handles when a type hint is Optional

    Handles Optional[type] typing and strips out the base type to pass back to the creation of a katra which needs base
    typing

    *Args*:

        typed: type

    *Returns*:

        typed: type (modified if Optional)
        optional: boolean for katra creation
    """
    # Set optional to false
    optional = False
    # Check if it has __args__ to look for optionality as it is a GenericAlias
    if hasattr(typed, '__args__'):
        # If it is more than one than it is most likely optional but check against NoneType in the tuple to verify
        # Check the length of type __args__
        type_args = typed.__args__
        # Optional[X] has type_args = (X, None) and is equal to Union[X, None]
        if (len(type_args) == 2) and (typed == Union[type_args[0], None]):
            # Since this is true we need to strip out the OG type
            # Grab all the types that are not NoneType and collapse to a list
            type_list = [val for val in type_args if val is not type(None)]
            if len(type_list) > 1:
                raise TypeError(f"Passing multiple subscript types to GenericAlias is not supported: {type_list}")
            else:
                typed = type_list[0]
            # Set the optional flag to true
            optional = True
    return typed, optional


def katra(typed, default=None):
    """Public interface to create a katra

    A 'katra' is the basic functional unit of `spock`. It defines a parameter using attrs as the backend, type checks
    both simple types and subscripted GenericAlias types (e.g. lists and tuples), handles setting default parameters,
    and deals with parameter optionality

    *Args*:

        typed: the type of the parameter to define
        default: the default value to assign if given
        optional: whether to make the parameter optional or not (thus allowing None)

    Returns:

        x: Attribute from attrs

    """
    # Handle optionals
    typed, optional = _handle_optional_typing(typed)
    # We need to check if the type is a _GenericAlias so that we can handle subscripted general types
    # If it is subscript typed it will not be T which python uses as a generic type name
    if isinstance(typed, _GenericAlias) and typed.__args__[0].__name__ != "T":
        x = _generic_alias_katra(typed=typed, default=default, optional=optional)
    elif isinstance(typed, EnumMeta):
        x = _enum_katra(typed=typed, default=default, optional=optional)
    else:
        x = _type_katra(typed=typed, default=default, optional=optional)
    return x
