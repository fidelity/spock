# -*- coding: utf-8 -*-

# Copyright 2019 FMR LLC <opensource@fidelity.com>
# SPDX-License-Identifier: Apache-2.0

"""Handles the definitions of arguments types for Spock (backend: attrs)"""

import attr
from typing import Union
from typing import _GenericAlias



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
    return typed.__args__[0].__name__


def _generic_alias_katra(typed, default=None, optional=False):
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
    base_typed = typed.__origin__ # base python class from which a GenericAlias is derived
    if default is not None:
        # if a default is provided, that takes precedence
        x = attr.ib(validator=[attr.validators.instance_of(base_typed), _validate_subscripted_generic],
                    default=default, type=base_typed, metadata={'type': _extract_base_type(typed)})
    elif optional:
        # if there's no default, but marked as optional, then set the default to None
        x = attr.ib(validator=[attr.validators.optional(attr.validators.instance_of(base_typed)),
                               _validate_subscripted_generic], type=base_typed,
                    metadata={'type': _extract_base_type(typed)})
    else:
        x = attr.ib(validator=[attr.validators.instance_of(base_typed), _validate_subscripted_generic],
                    type=base_typed, metadata={'type': _extract_base_type(typed)})
    return x


def _type_katra(typed, default=None, optional=False):
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
    if isinstance(typed, type) and typed.__name__ == "bool":
        optional = True
        default = False
    if default is not None:
        # if a default is provided, that takes precedence
        x = attr.ib(validator=attr.validators.instance_of(typed), default=default)
    elif optional:
        # if no default is provided, but it's marked as optional, set default=None
        x = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(typed)), default=None)
    else:
        x = attr.ib(validator=attr.validators.instance_of(typed), type=typed)
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
    type_args = typed.__args__ 
    # Optional[X] has type_args = (X, None) and is equal to Union[X, None]
    if (len(type_args) == 2) and (typed == Union[type_args[0], None]):
        # this is truly an Optional type
        # Since this is true we need to strip out the OG type
        # Grab all the types that are not NoneType and collapse to a list
        type_list = [val for val in type_args if val is not type(None)]
        if len(type_list) > 1:
            raise TypeError(f"Passing multiple subscript types to GenericAlias is not supported: {type_list}")
        else:
            typed = type_list[0]
        # Set the optional flag to true
        optional = True
    else:
        # Untrue so it's not optional
        optional = False
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
    # We need to check if the type is a _GenericAlias so that we can handle subscripted general types
    is_generic_alias = isinstance(typed, _GenericAlias)
    # Handle optional typing
    if is_generic_alias:
        typed, optional = _handle_optional_typing(typed)
    else:
        optional = False
    # The second check is to see if the generic type is subscript typed
    # If it is subscript typed it will not be T which python uses as a generic type name
    if is_generic_alias and typed.__args__[0].__name__ != "T":
        x = _generic_alias_katra(typed=typed, default=default, optional=optional)
    else:
        x = _type_katra(typed=typed, default=default, optional=optional)
    return x
