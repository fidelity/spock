# -*- coding: utf-8 -*-

# Copyright FMR LLC <opensource@fidelity.com>
# SPDX-License-Identifier: Apache-2.0

"""Handles the definitions of arguments types for Spock (backend: attrs)"""

from enum import Enum, EnumMeta
from functools import partial
from typing import NewType, TypeVar, Union

import attr

from spock.backend.utils import _get_name_py_version
from spock.backend.validators import (
    _in_type,
    instance_of,
    is_len,
    ordered_is_instance_deep_iterable,
)
from spock.utils import _SpockGenericAlias, _SpockVariadicGenericAlias


class SavePath(str):
    """Spock special key for saving the Spock config to file

    Defines a special key use to save the current Spock config to file

    """

    def __new__(cls, x: str) -> str:
        return super().__new__(cls, x)


def _extract_base_type(typed):
    """Extracts the name of the type from a _GenericAlias

    Assumes that the derived types are only of length 1 as the __args__ are [0]
    recursed... this is not true for
    tuples

    Args:
        typed: the type of the parameter

    Returns:
        name of type
    """
    if hasattr(typed, "__args__") and not isinstance(typed, _SpockVariadicGenericAlias):
        name = _get_name_py_version(typed=typed)
        bracket_val = f"{name}[{_extract_base_type(typed.__args__[0])}]"
        return bracket_val
    else:
        bracket_value = _get_name_py_version(typed=typed)
    return bracket_value


def _recursive_generic_validator(typed):
    """Recursively assembles the validators for nested generic types

    Walks through the nested type structure and determines whether to recurse all the
    way to a base type. Once it
    hits the base type it bubbles up the correct validator that is nested within the
    upper validator

    Args:
        typed: input type

    Returns:
        return_type: recursively built deep_iterable validators

    """
    if hasattr(typed, "__args__") and not isinstance(typed, _SpockVariadicGenericAlias):
        # Iterate through since there might be multiple types?
        # Handle Tuple type
        if _get_name_py_version(typed) == "Tuple":

            # Tuples by def have len more than 1. We throw an exception if not since
            # a tuple is not necessary in that case. Tuples can also have mixed types,
            # thus we need to handle this oddity here -- we do this by passing each
            # of the types as the member validator and wrap it in an or

            # If there are more __args__ then we still need to recurse as it is still a
            # GenericAlias
            member_validator = (
                typed.__args__ if len(typed.__args__) > 1 else typed.__args__[0]
            )
            # Try to add the length validator
            try:
                set_len = len(member_validator)
            except Exception as e:
                raise TypeError(
                    f"Attempting to use a Tuple of length 1 -- don't use an "
                    f"iterable type as it seems it is not needed"
                )
            iterable_validator = attr.validators.and_(
                instance_of(typed.__origin__), is_len(set_len)
            )
            return_type = ordered_is_instance_deep_iterable(
                ordered_types=typed.__args__,
                recurse_callable=_recursive_generic_validator,
                iterable_validator=iterable_validator,
            )
            return return_type
        # Handle List type
        elif _get_name_py_version(typed) == "List":
            # Lists can only have one given type... thus pop off idx 0 for the member
            # validator
            member_validator = typed.__args__[0]
            iterable_validator = instance_of(typed.__origin__)
            return_type = attr.validators.deep_iterable(
                member_validator=_recursive_generic_validator(member_validator),
                iterable_validator=iterable_validator,
            )
            return return_type
        # Handle Dict types
        elif _get_name_py_version(typed) == "Dict":
            key_type, value_type = typed.__args__
            if key_type is not str:
                raise TypeError(
                    f"Unexpected key type of `{str(key_type.__name__)}` when attempting "
                    f"to handle GenericAlias type of Dict -- currently Spock only "
                    f"supports str as keys due to maintaining support for valid TOML "
                    f"and JSON files"
                )
            if hasattr(value_type, "__args__") and not isinstance(
                typed, _SpockVariadicGenericAlias
            ):
                return_type = attr.validators.deep_mapping(
                    value_validator=_recursive_generic_validator(value_type),
                    key_validator=instance_of(key_type),
                )
            else:
                return_type = attr.validators.deep_mapping(
                    value_validator=instance_of(value_type),
                    key_validator=instance_of(key_type),
                )
            return return_type
        else:
            raise TypeError(
                f"Unexpected type of `{str(typed)}` when attempting to handle "
                f"GenericAlias types"
            )
    else:
        # If no more __args__ then we are to the base type and need to bubble up the
        # type
        # But we need to check against base types and enums
        if isinstance(typed, EnumMeta):
            base_type, allowed = _check_enum_props(typed)
            return_type = attr.validators.and_(
                instance_of(base_type), attr.validators.in_(allowed)
            )
        else:
            return_type = instance_of(typed)
    return return_type


def _generic_alias_katra(typed, default=None, optional=False):
    """Private interface to create a subscripted generic_alias katra

    A 'katra' is the basic functional unit of `spock`. It defines a parameter using
    attrs as the backend, type checks
    both simple types and subscripted GenericAlias types (e.g. lists and tuples),
    handles setting default parameters,
    and deals with parameter optionality

    Handles: List[type], Tuple[type], Dict[type]

    Args:
        typed: the type of the parameter to define
        default: the default value to assign if given
        optional: whether to make the parameter optional or not (thus allowing None)

    Returns:
        x: Attribute from attrs

    """
    # base python class from which a GenericAlias is derived
    base_typed = typed.__origin__
    if default is not None and optional:
        # if there's no default, but marked as optional, then set the default to None
        x = attr.ib(
            validator=attr.validators.optional(_recursive_generic_validator(typed)),
            type=base_typed,
            default=default,
            metadata={
                "optional": True,
                "base": _extract_base_type(typed),
                "type": typed,
            },
        )
    elif default is not None:
        x = attr.ib(
            validator=_recursive_generic_validator(typed),
            default=default,
            type=base_typed,
            metadata={"base": _extract_base_type(typed), "type": typed},
        )
    elif optional:
        # if there's no default, but marked as optional, then set the default to None
        x = attr.ib(
            validator=attr.validators.optional(_recursive_generic_validator(typed)),
            type=base_typed,
            default=default,
            metadata={
                "optional": True,
                "base": _extract_base_type(typed),
                "type": typed,
            },
        )
    else:
        x = attr.ib(
            validator=_recursive_generic_validator(typed),
            type=base_typed,
            metadata={"base": _extract_base_type(typed), "type": typed},
        )
    return x


def _check_enum_props(typed):
    """Handles properties of enums

    Checks if all types of the enum are the same and assembles a list of allowed values

    Args:
        typed: the type of parameter (Enum)

    Returns:
        base_type: the base type of the Enum
        allowed: List of allowed values of the Enum

    """
    # First check if the types of Enum are the same
    type_set = {type(val.value) for val in typed}
    if len(type_set) > 1:
        raise TypeError(f"Enum cannot be defined with multiple types: {type_set}")
    base_type = list(type_set)[-1]
    allowed = [val.value for val in typed]
    return base_type, allowed


def _enum_katra(typed, default=None, optional=False):
    """Private interface to create a Enum typed katra

    A 'katra' is the basic functional unit of `spock`. It defines a parameter using
    attrs as the backend, type checks
    both simple types and subscripted GenericAlias types (e.g. lists and tuples),
    handles setting default parameters,
    and deals with parameter optionality

    Args:
        typed: the type of the parameter to define
        default: the default value to assign if given
        optional: whether to make the parameter optional or not (thus allowing None)

    Returns:
        x: Attribute from attrs

    """
    # First check if the types of Enum are the same
    base_type, allowed = _check_enum_props(typed)
    if base_type.__name__ == "type":
        x = _enum_class_katra(
            typed=typed, allowed=allowed, default=default, optional=optional
        )
    else:
        x = _enum_base_katra(
            typed=typed,
            base_type=base_type,
            allowed=allowed,
            default=default,
            optional=optional,
        )
    return x


def _cast_enum_default(default):
    """Allows the enum default to be the specific value or the Enum structured value

    Checks if enum type and extracts the value from the Enum

    Args:
        default: the default value to assign if given

    Returns:
        default value or the Enum extracted value

    """
    if isinstance(default, Enum):
        return default.value
    else:
        return default


def _enum_base_katra(typed, base_type, allowed, default=None, optional=False):
    """Private interface to create a base Enum typed katra

    Here we handle the base types of enums that allows us to force a type check on
    the instance

    A 'katra' is the basic functional unit of `spock`. It defines a parameter using
    attrs as the backend, type checks
    both simple types and subscripted GenericAlias types (e.g. lists and tuples),
    handles setting default parameters,
    and deals with parameter optionality

    Args:
        typed: the type of the parameter to define
        base_type: underlying base type
        allowed: set of allowed values
        default: the default value to assign if given
        optional: whether to make the parameter optional or not (thus allowing None)

    Returns:
        x: Attribute from attrs

    """
    if default is not None and optional:
        x = attr.ib(
            validator=attr.validators.optional(
                [instance_of(base_type), attr.validators.in_(allowed)]
            ),
            default=_cast_enum_default(default),
            type=typed,
            metadata={"base": typed.__name__, "optional": True},
        )
    elif default is not None:
        x = attr.ib(
            validator=[
                instance_of(base_type),
                attr.validators.in_(allowed),
            ],
            default=_cast_enum_default(default),
            type=typed,
            metadata={"base": typed.__name__},
        )
    elif optional:
        x = attr.ib(
            validator=attr.validators.optional(
                [instance_of(base_type), attr.validators.in_(allowed)]
            ),
            default=_cast_enum_default(default),
            type=typed,
            metadata={"base": typed.__name__, "optional": True},
        )
    else:
        x = attr.ib(
            validator=[
                instance_of(base_type),
                attr.validators.in_(allowed),
            ],
            type=typed,
            metadata={"base": typed.__name__},
        )
    return x


def _enum_class_katra(typed, allowed, default=None, optional=False):
    """Private interface to create a base Enum typed katra

    Here we handle the class based types of enums. Seeing as these classes are
    generated dynamically we cannot
    force type checking of a specific instance however the in_ validator will
    catch an incorrect instance type

    A 'katra' is the basic functional unit of `spock`. It defines a parameter using
    attrs as the backend, type checks
    both simple types and subscripted GenericAlias types (e.g. lists and tuples),
    handles setting default parameters,
    and deals with parameter optionality

    Args:
        typed: the type of the parameter to define
        allowed: set of allowed values
        default: the default value to assign if given
        optional: whether to make the parameter optional or not (thus allowing None)

    Returns:
        x: Attribute from attrs

    """
    if default is not None and optional:
        x = attr.ib(
            validator=attr.validators.optional([partial(_in_type, options=allowed)]),
            default=_cast_enum_default(default),
            type=typed,
            metadata={"base": typed.__name__, "optional": True},
        )
    elif default is not None:
        x = attr.ib(
            validator=[partial(_in_type, options=allowed)],
            default=_cast_enum_default(default),
            type=typed,
            metadata={"base": typed.__name__},
        )
    elif optional:
        x = attr.ib(
            validator=attr.validators.optional([partial(_in_type, options=allowed)]),
            default=_cast_enum_default(default),
            type=typed,
            metadata={"base": typed.__name__, "optional": True},
        )
    else:
        x = attr.ib(
            validator=[partial(_in_type, options=allowed)],
            type=typed,
            metadata={"base": typed.__name__},
        )
    return x


def _type_katra(typed, default=None, optional=False):
    """Private interface to create a simple typed katra

    A 'katra' is the basic functional unit of `spock`. It defines a parameter using
    attrs as the backend, type checks
    both simple types and subscripted GenericAlias types (e.g. lists and tuples),
    handles setting default parameters,
    and deals with parameter optionality

    Handles: bool, string, float, int, List, and Tuple

    Args:
        typed: the type of the parameter to define
        default: the default value to assign if given
        optional: whether to make the parameter optional or not (thus allowing None)

    Returns:
        x: Attribute from attrs

    """
    # Grab the name first based on if it is a base type, NewType, or GenericAlias
    # if isinstance(typed, (type, NewType)):
    if isinstance(typed, type):
        name = typed.__name__
    elif isinstance(typed, _SpockGenericAlias):
        name = _get_name_py_version(typed=typed)
    else:
        raise TypeError(f"Encountered an unexpected type in _type_katra: {typed}")
    special_key = None
    # Default booleans to false and optional due to the nature of a boolean
    if isinstance(typed, type) and name == "bool":
        optional = True
        # if it's a string -- it could be an env resolver -- pass it through
        if (not isinstance(default, str)) and (default is not True):
            default = False
    # For the save path type we need to swap the type back to it's base class (str)
    elif isinstance(typed, type) and name == "SavePath":
        optional = True
        special_key = name
        typed = str

    if default is not None and optional:
        # if a default is provided, that takes precedence
        x = attr.ib(
            validator=attr.validators.optional(instance_of(typed)),
            default=default,
            type=typed,
            metadata={"optional": True, "base": name, "special_key": special_key},
        )
    elif default is not None:
        # if a default is provided, that takes precedence
        x = attr.ib(
            validator=instance_of(typed),
            default=default,
            type=typed,
            metadata={"base": name, "special_key": special_key},
        )
    elif optional:
        x = attr.ib(
            validator=attr.validators.optional(instance_of(typed)),
            default=default,
            type=typed,
            metadata={"optional": True, "base": name, "special_key": special_key},
        )
    else:
        x = attr.ib(
            validator=instance_of(typed),
            type=typed,
            metadata={"base": name, "special_key": special_key},
        )
    return x


def _handle_optional_typing(typed):
    """Handles when a type hint is Optional

    Handles Optional[type] typing and strips out the base type to pass back to the creation of a katra which needs base
    typing

    Args:
        typed: type

    Returns:
        typed: type (modified if Optional)
        optional: boolean for katra creation
    """
    # Set optional to false
    optional = False
    # Check if it has __args__ to look for optionality as it is a GenericAlias -- also make sure it is not
    # callable as that also has __args__
    if hasattr(typed, "__args__") and not isinstance(typed, _SpockVariadicGenericAlias):
        # If it is more than one than it is most likely optional but check against NoneType in the tuple to verify
        # Check the length of type __args__
        type_args = typed.__args__
        # Optional[X] has type_args = (X, None) and is equal to Union[X, None]
        if (len(type_args) == 2) and (typed == Union[type_args[0], None]):
            typed = type_args[0]
            # Set the optional flag to true
            optional = True
    return typed, optional


def _callable_katra(typed, default=None, optional=False):
    """Private interface to create a Callable katra

    Here we handle the callable type katra that allows us to force a callable check on the value provided

    A 'katra' is the basic functional unit of `spock`. It defines a parameter using attrs as the backend, type checks
    both simple types and subscripted GenericAlias types (e.g. lists and tuples), handles setting default parameters,
    and deals with parameter optionality

    Handles: callable

    Args:
        typed: the type of the parameter to define
        default: the default value to assign if given
        optional: whether to make the parameter optional or not (thus allowing None)

    Returns:
        x: Attribute from attrs

    """
    if default is not None and optional:
        x = attr.ib(
            validator=attr.validators.optional(attr.validators.is_callable()),
            default=default,
            type=typed,
            metadata={"optional": True, "base": _get_name_py_version(typed)},
        )
    elif default is not None:
        # if a default is provided, that takes precedence
        x = attr.ib(
            validator=attr.validators.is_callable(),
            default=default,
            type=typed,
            metadata={"base": _get_name_py_version(typed)},
        )
    elif optional:
        x = attr.ib(
            validator=attr.validators.optional(attr.validators.is_callable()),
            default=default,
            type=typed,
            metadata={"optional": True, "base": _get_name_py_version(typed)},
        )
    else:
        x = attr.ib(
            validator=attr.validators.is_callable(),
            type=typed,
            metadata={"base": _get_name_py_version(typed)},
        )
    return x


def katra(typed, default=None, inherit_optional=False):
    """Public interface to create a katra

    A 'katra' is the basic functional unit of `spock`. It defines a parameter using
    attrs as the backend, type checks both simple types and subscripted GenericAlias
    types (e.g. lists and tuples), handles setting default parameters,
    and deals with parameter optionality

    Args:
        typed: the type of the parameter to define
        default: the default value to assign if given
        inherit_optional: optionality from inheritance

    Returns:
        x: Attribute from attrs

    """
    # Handle optionals
    typed, optional = _handle_optional_typing(typed)
    # Since we strip away the optional typing notation for Generics -- we need to
    # override with optional coming from the parent
    optional = True if (optional or inherit_optional) else False
    # Checks for callables via the different Variadic types across versions
    if isinstance(typed, _SpockVariadicGenericAlias):
        x = _callable_katra(typed=typed, default=default, optional=optional)
    # We need to check if the type is a _GenericAlias so that we can handle subscripted general types
    # If it is subscript typed it will not be T which python uses as a generic type name
    elif isinstance(typed, _SpockGenericAlias) and (
        not isinstance(typed.__args__[0], TypeVar)
    ):
        x = _generic_alias_katra(typed=typed, default=default, optional=optional)
    # Catch the Enum type
    elif isinstance(typed, EnumMeta):
        x = _enum_katra(typed=typed, default=default, optional=optional)
    # Else fall back on the basic type
    else:
        x = _type_katra(typed=typed, default=default, optional=optional)
    # Add back in the OG type as part of the metadata
    x.metadata.update({"og_type": typed})
    return x
