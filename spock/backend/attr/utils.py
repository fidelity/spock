# -*- coding: utf-8 -*-

# Copyright 2019 FMR LLC <opensource@fidelity.com>
# SPDX-License-Identifier: Apache-2.0

"""Attr utility functions for Spock"""


def get_type_fields(input_classes):
    """Creates a dictionary of names and types

    *Args*:

        input_classes: list of input classes

    *Returns*:

        type_fields: dictionary of names and types

    """
    # Parse out the types if generic
    type_fields = {}
    for attr in input_classes:
        input_attr = {}
        for val in attr.__attrs_attrs__:
            if 'type' in val.metadata:
                input_attr.update({val.name: val.metadata['type']})
            else:
                input_attr.update({val.name: None})
        type_fields.update({attr.__name__: input_attr})
    return type_fields


def flatten_type_dict(type_dict):
    """Flattens a nested dictionary

    *Args*:

        type_dict: dictionary of types that are generic

    *Returns*:

        flat_dict: flatten dictionary to a single level

    """
    flat_dict = {}
    for k, v in type_dict.items():
        if isinstance(v, dict):
            return_dict = flatten_type_dict(v)
            flat_dict.update(return_dict)
        else:
            flat_dict[k] = v
    return flat_dict


def convert_to_tuples(input_dict, named_type_dict):
    """Convert lists to tuples

    Payloads from markup come in as Lists and not Tuples. This function turns lists in to tuples for the payloads
    so the attr values are set correctly. Will call itself recursively if a dictionary is present for class specific
    values

    *Args*:

        input_dict: input dictionary
        named_type_dict: dictionary of names with generic types

    *Returns*:

        updated_dict: a dictionary with lists converted to tuples

    """
    updated_dict = {}
    all_typed_dict = flatten_type_dict(named_type_dict)
    for k, v in input_dict.items():
        if k != 'config':
            if isinstance(v, dict):
                updated = convert_to_tuples(v, named_type_dict.get(k))
                if updated:
                    updated_dict.update({k: updated})
            elif all_typed_dict[k] is not None:
                updated = _recursive_list_to_tuple(v, all_typed_dict[k])
                updated_dict.update({k: updated})
    return updated_dict


def _recursive_list_to_tuple(value, typed):
    """Recursively turn lists into tuples

    Recursively looks through a pair of value and type and sets any of the possibly nested type of value to tuple
    if tuple is the specified type

    *Args*:

        value: value to check and set typ if necessary
        typed: type of the generic alias to check against

    *Returns*:

        value: updated value with correct type casts

    """
    # Check for __args__ as it signifies a generic and make sure it's not already been cast as a tuple
    # from a composed payload
    if hasattr(typed, '__args__') and not isinstance(value, tuple):
        # need to recurse before casting as we can't set values in a tuple with idx
        # Since it's generic it should be iterable to recurse and check it's children
        for idx, val in enumerate(value):
            value[idx] = _recursive_list_to_tuple(val, typed.__args__[0])
        # First check if list and then swap to tuple if the origin is tuple
        if isinstance(value, list) and typed.__origin__.__name__.lower() == 'tuple':
            value = tuple(value)
    else:
        return value
    return value
