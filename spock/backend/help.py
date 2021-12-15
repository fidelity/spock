# -*- coding: utf-8 -*-

# Copyright FMR LLC <opensource@fidelity.com>
# SPDX-License-Identifier: Apache-2.0

"""Handles all ops for assembling and pretty printing help info"""

import re
import sys
from enum import EnumMeta
from typing import Callable, Union

from attr import NOTHING


def find_attribute_idx(newline_split_docs):
    """Finds the possible split between the header and Attribute annotations

    Args:
        newline_split_docs: new line split text

    Returns:
        idx: -1 if none or the idx of Attributes

    """
    for idx, val in enumerate(newline_split_docs):
        re_check = re.search(r"(?i)Attribute?s?:", val)
        if re_check is not None:
            return idx
    return -1


def split_docs(obj):
    """Possibly splits head class doc string from attribute docstrings

    Attempts to find the first contiguous line within the Google style docstring to use as the class docstring.
    Splits the docs base on the Attributes tag if present.

    Args:
        obj: class object to rip info from

    Returns:
        class_doc: class docstring if present or blank str
        attr_doc: list of attribute doc strings

    """
    if obj.__doc__ is not None:
        # Split by new line
        newline_split_docs = obj.__doc__.split("\n")
        # Cleanup l/t whitespace
        newline_split_docs = [val.strip() for val in newline_split_docs]
    else:
        newline_split_docs = []
    # Find the break between the class docs and the Attribute section -- if this returns -1 then there is no
    # Attributes section
    attr_idx = find_attribute_idx(newline_split_docs)
    head_docs = newline_split_docs[:attr_idx] if attr_idx != -1 else newline_split_docs
    attr_docs = newline_split_docs[attr_idx:] if attr_idx != -1 else []
    # Grab only the first contiguous line as everything else will probably be too verbose (e.g. the
    # mid-level docstring that has detailed descriptions
    class_doc = ""
    for idx, val in enumerate(head_docs):
        class_doc += f" {val}"
        if idx + 1 != len(head_docs) and head_docs[idx + 1] == "":
            break
    # Clean up any l/t whitespace
    class_doc = class_doc.strip()
    if len(class_doc) > 0:
        class_doc = f"-- {class_doc}"
    return class_doc, attr_docs


def match_attribute_docs(attr_name, attr_docs, attr_type_str, attr_default=NOTHING):
    """Matches class attributes with attribute docstrings via regex

    Args:
        attr_name: attribute name
        attr_docs: list of attribute docstrings
        attr_type_str: str representation of the attribute type
        attr_default: str representation of a possible default value

    Returns:
        dictionary of packed attribute information

    """
    # Regex match each value
    a_str = None
    for a_doc in attr_docs:
        match_re = re.search(r"(?i)^" + attr_name + "?:", a_doc)
        # Find only the first match -- if more than one than ignore
        if match_re:
            a_str = a_doc[match_re.end() :].strip()
    return {
        attr_name: {
            "type": attr_type_str,
            "desc": a_str if a_str is not None else "",
            "default": "(default: " + repr(attr_default) + ")"
            if type(attr_default).__name__ != "_Nothing"
            else "",
            "len": {"name": len(attr_name), "type": len(attr_type_str)},
        }
    }


def handle_attributes_print(info_dict, max_indent: int):
    """Prints attribute information in an argparser style format

    Args:
        info_dict: packed attribute info dictionary to print
        max_indent: max indent for pretty print of help

    """
    # Figure out indents
    max_param_length = max([len(k) for k in info_dict.keys()])
    max_type_length = max([v["len"]["type"] for v in info_dict.values()])
    # Print akin to the argparser
    for k, v in info_dict.items():
        print(
            f"    {k}"
            + (" " * (max_param_length - v["len"]["name"] + max_indent))
            + f'{v["type"]}'
            + (" " * (max_type_length - v["len"]["type"] + max_indent))
            + f'{v["desc"]} {v["default"]}'
        )
    # Blank for spacing :-/
    print("")


def get_type_string(val, nested_others):
    """Gets the type of the attr val as a string

    Args:
        val: current attr being processed
        nested_others: list of nested others to deal with that might have module path info in the string

    Returns:
        type_string: type of the attr as a str

    """
    # Grab the base or type info depending on what is provided
    if "type" in val.metadata:
        type_string = repr(val.metadata["type"])
    elif "base" in val.metadata:
        type_string = val.metadata["base"]
    elif hasattr(val.type, "__name__"):
        type_string = val.type.__name__
    else:
        type_string = str(val.type)
    # Regex out the typing info if present
    type_string = re.sub(r"typing.", "", type_string)
    # Regex out any nested_others that have module path information
    for other_val in nested_others:
        split_other = f"{'.'.join(other_val.split('.')[:-1])}."
        type_string = re.sub(split_other, "", type_string)
    # Regex the string to see if it matches any Enums in the __main__ module space
    # Construct the type with the metadata
    if "optional" in val.metadata:
        type_string = f"Optional[{type_string}]"
    return type_string


def get_from_sys_modules(cls_name):
    """Gets the class from a dot notation name

    Args:
        cls_name: dot notation enum name

    Returns:
        module: enum class

    """
    # Split on dot notation
    split_string = cls_name.split(".")
    module = None
    for idx, val in enumerate(split_string):
        # idx = 0 will always be a call to the sys.modules dict
        if idx == 0:
            module = sys.modules[val]
        # all other idx are paths along the module that need to be traversed
        # idx = -1 will always be the final Enum object name we want to grab (final getattr call)
        else:
            module = getattr(module, val)
    return module


def handle_help_main(
    input_classes: list, module_name: str, extract_fnc: Callable, max_indent: int
):
    """Handles the print of the main class types

    Args:
        input_classes: current set of input classes
        module_name: module name to match
        extract_fnc: function that gets the nested lists within classes
        max_indent: max indent for pretty print of help

    Returns:
        other_list: extended list of other classes/enums to process

    """
    # List to catch Enums and classes and handle post spock wrapped attr classes
    other_list = []
    covered_set = set()
    for attrs_class in input_classes:
        # Split the docs into class docs and any attribute docs
        class_doc, attr_docs = split_docs(attrs_class)
        print("  " + attrs_class.__name__ + f" {class_doc}")
        # Keep a running info_dict of all the attribute level info
        info_dict = {}
        for val in attrs_class.__attrs_attrs__:
            # If the type is an enum we need to handle it outside of this attr loop
            # Match the style of nested enums and return a string of module.name notation
            if isinstance(val.type, EnumMeta):
                other_list.append(f"{val.type.__module__}.{val.type.__name__}")
            # if there is a type (implied Iterable) -- check it for nested Enums or classes
            nested_others = extract_fnc(val, module_name)
            if len(nested_others) > 0:
                other_list.extend(nested_others)
            # Get the type represented as a string
            type_string = get_type_string(val, nested_others)
            info_dict.update(
                match_attribute_docs(val.name, attr_docs, type_string, val.default)
            )
        # Add to covered so we don't print help twice in the case of some recursive nesting
        covered_set.add(f"{attrs_class.__module__}.{attrs_class.__name__}")
        handle_attributes_print(info_dict=info_dict, max_indent=max_indent)
    # Convert the enum list to a set to remove dupes and then back to a list so it is iterable -- set diff to not
    # repeat
    return list(set(other_list) - covered_set)


def handle_help_enums(
    other_list: list, module_name: str, extract_fnc: Callable, max_indent: int
):
    """Handles any extra enums from non main args

    Args:
        other_list: extended list of other classes/enums to process
        module_name: module name to match
        extract_fnc: function that gets the nested lists within classes
        max_indent: max indent for pretty print of help

    Returns:
        None

    """
    # Iterate any Enum type classes
    for other in other_list:
        # if it's longer than 2 then it's an embedded Spock class
        if ".".join(other.split(".")[:-1]) == module_name:
            class_type = get_from_sys_modules(other)
            # Invoke recursive call for the class
            attrs_help(
                [class_type],
                module_name,
                extract_fnc=extract_fnc,
                max_indent=max_indent,
            )
        # Fall back to enum style
        else:
            enum = get_from_sys_modules(other)
            # Split the docs into class docs and any attribute docs
            class_doc, attr_docs = split_docs(enum)
            print("  " + enum.__name__ + f" ({class_doc})")
            info_dict = {}
            for val in enum:
                info_dict.update(
                    match_attribute_docs(
                        attr_name=val.name,
                        attr_docs=attr_docs,
                        attr_type_str=type(val.value).__name__,
                    )
                )
            handle_attributes_print(info_dict=info_dict, max_indent=max_indent)


def attrs_help(
    input_classes: Union[list, tuple],
    module_name: str,
    extract_fnc: Callable,
    max_indent: int,
):
    """Handles walking through a list classes to get help info

    For each class this function will search __doc__ and attempt to pull out help information for both the class
    itself and each attribute within the class. If it finds a repeated class in a iterable object it will
    recursively call self to handle information

    Args:
        input_classes: list of attr classes
        module_name: name of module to match
        extract_fnc: function that gets the nested lists within classes
        max_indent: max indent for pretty print of help

    Returns:
        None

    """
    # Handle the main loop
    other_list = handle_help_main(input_classes, module_name, extract_fnc, max_indent)
    handle_help_enums(
        other_list=other_list,
        module_name=module_name,
        extract_fnc=extract_fnc,
        max_indent=max_indent,
    )
