# -*- coding: utf-8 -*-

# Copyright FMR LLC <opensource@fidelity.com>
# SPDX-License-Identifier: Apache-2.0

"""Attr utility functions for Spock"""

import importlib
from typing import Any, ByteString, Callable, Dict, List, Tuple, Type, Union

from cryptography.fernet import Fernet

from spock.exceptions import _SpockValueError
from spock.utils import _C, _T, _SpockVariadicGenericAlias


def encrypt_value(value: Any, key: Union[str, ByteString, bytes], salt: str):
    """Encrypts a given value with a key and salt

    Args:
        value: current value to encrypt
        key: A URL-safe base64-encoded 32-byte key.
        salt: salt to add to value

    Returns:
        encrypted value

    """
    # Make the class to encrypt
    encrypt = Fernet(key=key)
    # Encrypt the plaintext value
    salted_password = value + salt
    # encode to utf-8 -> encrypt -> decode from utf-8
    return encrypt.encrypt(str.encode(salted_password)).decode()


def decrypt_value(value: Any, key: Union[str, ByteString, bytes], salt: str):
    """Decrypts a given value from a key and salt

    Args:
        value: current value to decrypt
        key: A URL-safe base64-encoded 32-byte key.
        salt: salt to add to value

    Returns:
        decrypted value

    """
    # Make the class to encrypt
    decrypt = Fernet(key=key)
    # Decrypt back to plaintext value
    salted_password = decrypt.decrypt(str.encode(value)).decode()
    return salted_password[: -len(salt)]


def _str_2_callable(val: str, **kwargs):
    """Tries to convert a string representation of a module and callable to the reference to the callable

    If the module of callable cannot be found on the PYTHONPATH then an exception is raised

    Args:
        val: string rep of a module and callable
        **kwargs: in case additional keyword args are passed

    Returns:
        reference to a callable

    Raises:
        _SpockValueError

    """
    str_field = str(val)
    module, fn = str_field.rsplit(".", 1)
    try:
        call_ref = getattr(importlib.import_module(module), fn)
    except Exception as e:
        raise _SpockValueError(
            f"Attempted to import module {module} and callable {fn} however it could not be found on the current "
            f"python path: {e}"
        )
    return call_ref


def _callable_2_str(val: Callable, **kwargs):
    """Converts a callable to a str based on the module and name

    Args:
        val: callable object
        **kwargs: in case additional keyword args are passed

    Returns:
        string of module.name

    """
    return f"{val.__module__}.{val.__name__}"


def _recurse_callables(val: _T, fnc: Callable, check_type: Type = str):
    """Recurses through objects casting any callables to the correct format

    Handles both strings to callables and callables to strings depending on the function passed in

    Args:
        val: current object
        fnc: callable
        check_type: type to check against to verify conversion

    Returns:
        object with mapped callables/strings

    """
    if isinstance(val, (list, List, tuple, Tuple)):
        out = []
        for v in val:
            if isinstance(val, (list, List, tuple, Tuple, dict, Dict)):
                out.append(_recurse_callables(v, fnc, check_type))
            else:
                out.append(fnc(v))
        out = type(val)(out)
    elif isinstance(val, (dict, Dict)):
        out = {}
        for k, v in val.items():
            if isinstance(val, (list, List, tuple, Tuple, dict, Dict)):
                out.update({k: _recurse_callables(v, fnc, check_type)})
            else:
                out.update({k: fnc(v)})
    elif isinstance(val, check_type):
        out = fnc(val)
    # Fall back to just passing the unmodified value back
    else:
        out = val
    return out


def _get_name_py_version(typed: _T):
    """Gets the name of the type depending on the python version

    Args:
        typed: the type of the parameter

    Returns:
        name of the type

    """
    return typed._name if hasattr(typed, "_name") else typed.__name__


def get_attr_fields(input_classes: List):
    """Gets the attribute fields from all classes

    Args:
        input_classes: current list of input classes

    Returns:
        dictionary of all attrs attribute fields

    """
    return {
        attr.__name__: [val.name for val in attr.__attrs_attrs__]
        for attr in input_classes
    }


def get_type_fields(input_classes: List):
    """Creates a dictionary of names and types

    Args:
        input_classes: list of input classes

    Returns:
        type_fields: dictionary of names and types

    """
    # Parse out the types if generic
    type_fields = {}
    for attr in input_classes:
        input_attr = {}
        for val in attr.__attrs_attrs__:
            if "type" in val.metadata:
                input_attr.update({val.name: val.metadata["type"]})
            else:
                input_attr.update({val.name: None})
        type_fields.update({attr.__name__: input_attr})
    return type_fields


def flatten_type_dict(type_dict: Dict):
    """Flattens a nested dictionary

    Args:
        type_dict: dictionary of types that are generic

    Returns:
        flat_dict: flatten dictionary to a single level

    """
    flat_dict = {}
    for k, v in type_dict.items():
        if isinstance(v, dict):
            # return_dict = flatten_type_dict(v, input_dict)
            return_dict = flatten_type_dict(
                v,
            )
            flat_dict.update(return_dict)
        else:
            flat_dict[k] = v
    return flat_dict


def _get_iter(value: Union[List, Dict]):
    """Returns the iterator for the type

    Args:
        value: instance of type List or Dict

    Returns:
        iterator

    """
    if isinstance(value, (list, List)):
        return enumerate(value)
    elif isinstance(value, (dict, Dict)):
        return value.items()
    else:
        raise ValueError(f"Cannot get iterator for type `{type(value)}`")


def convert_to_tuples(
    input_dict: Dict, base_type_dict: Dict, flat_type_dict: Dict, class_names: List
):
    """Convert lists to tuples

    Payloads from markup come in as Lists and not Tuples. This function turns lists in to tuples for the payloads
    so the attr values are set correctly. Will call itself recursively if it is iterable. Handles list of classes
    specifically

    Args:
        input_dict: input dictionary
        base_type_dict: dictionary of nested types
        flat_type_dict: dictionary of names with generic types
        class_names: List of base spock class names

    Returns:
        updated_dict: a dictionary with lists converted to tuples

    """
    updated_dict = {}
    for k, v in input_dict.items():
        if k != "config":
            # If v is any iterable we need to step into the nested structure
            if isinstance(v, (dict, Dict, list, List, tuple, Tuple)):
                # We've hit a fundamental declared type -- recurse via type checking
                if k in flat_type_dict:
                    updated = _recursive_list_to_tuple(
                        k, v, flat_type_dict[k], class_names
                    )
                    if updated:
                        updated_dict.update({k: updated})
                # Have to handle this specifically -- this is lists of spock classes
                # here we need to update a list instead of the dict directly
                elif isinstance(v, (list, List)) and k in class_names:
                    updated_list = []
                    # Iterate over list of classes
                    for _, val in _get_iter(v):
                        updated = convert_to_tuples(
                            val, base_type_dict, flat_type_dict, class_names
                        )
                        updated_list.append(updated)
                    updated_dict.update({k: updated_list})
                # Keep recursing through the structure
                else:
                    updated = convert_to_tuples(
                        v, base_type_dict, flat_type_dict, class_names
                    )
                    if updated:
                        updated_dict.update({k: updated})
            # If there is no nested structure then just map
            else:
                updated_dict.update({k: v})
    return updated_dict


def deep_update(source: Dict, updates: Dict):
    """Deeply updates a dictionary

    Iterates through a dictionary recursively to update individual values within a possibly nested dictionary
    of dictionaries

    Args:
        source: source dictionary
        updates: updates to the dictionary

    Returns:
        source: updated version of the source dictionary

    """
    for k, v in updates.items():
        if isinstance(v, (dict, Dict)) and v:
            updated_dict = deep_update(source.get(k), v)
            if updated_dict:
                source[k] = updated_dict
        else:
            source[k] = v
    return source


def _recursive_list_to_tuple(key: str, value: Any, typed: _T, class_names: List):
    """Recursively turn lists into tuples

    Recursively looks through a pair of value and type and sets any of the possibly nested type of value to tuple
    if tuple is the specified type

    Args:
        key: name of parameter
        value: value to check and set type if necessary
        typed: type of the generic alias to check against
        class_names: list of all spock class names

    Returns:
        value: updated value with correct type casts

    """
    # Check for __args__ as it signifies a generic and make sure it's not already
    # been cast as a tuple from a composed payload
    if (
        hasattr(typed, "__args__")
        and not isinstance(value, tuple)
        and not (isinstance(value, str) and value in class_names)
        and not isinstance(typed, _SpockVariadicGenericAlias)
    ):
        # Force those with origin tuple types to be of the defined length
        # Here check for tuple and check length
        if (typed.__origin__ in (tuple, Tuple)) and len(value) != len(typed.__args__):
            raise ValueError(
                f"Tuple(s) are of a defined length -- For parameter {key} the length of the provided argument "
                f"({len(value)}) does not match the length of the defined argument ({len(typed.__args__)})"
            )
        # need to recurse before casting as we can't set values in a tuple with idx
        # Since it's generic it should be iterable  -- thus recurse and check its children
        if isinstance(value, (list, List)):
            # Then we continue to recurse
            # Iterate the list type and recurse call
            for idx, val in _get_iter(value):
                value[idx] = _recursive_list_to_tuple(
                    key, val, typed.__args__[0], class_names
                )
        elif isinstance(value, (dict, Dict)):
            # Iterate the dict type and recurse call
            for k, v in _get_iter(value):
                key_type, val_type = typed.__args__
                value[k] = _recursive_list_to_tuple(key, v, val_type, class_names)
        # We need to catch the mismatch if the current type is list and the given type is Tuple
        # First check if list and then swap to tuple if the origin is tuple -- only do this on the bubble up since
        # we can't assign by idx once we change to Tuple
        if isinstance(value, (list, List)) and typed.__origin__ in (tuple, Tuple):
            value = tuple(value)
    else:
        return value
    return value
