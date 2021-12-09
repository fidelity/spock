# -*- coding: utf-8 -*-

# Copyright FMR LLC <opensource@fidelity.com>
# SPDX-License-Identifier: Apache-2.0

"""Handles the building/saving of the configurations from the Spock config classes"""

import re
import sys
from abc import ABC, abstractmethod
from enum import EnumMeta
from typing import List

import attr
from attr import NOTHING

from spock.args import SpockArguments
from spock.backend.field_handlers import RegisterSpockCls
from spock.backend.spaces import BuilderSpace
from spock.backend.wrappers import Spockspace
from spock.graph import Graph
from spock.utils import make_argument


class BaseBuilder(ABC):  # pylint: disable=too-few-public-methods
    """Base class for building the backend specific builders

    This class handles the interface to the backend with the generic ConfigArgBuilder so that different
    backends can be used to handle processing

    *Attributes*

        _input_classes: list of input classes that link to a backend
        _graph: Graph, graph of the dependencies between spock classes
        _max_indent: maximum to indent between help prints
        _module_name: module name to register in the spock module space
        save_path: list of path(s) to save the configs to

    """

    def __init__(self, *args, max_indent: int = 4, module_name: str, **kwargs):
        """Init call for BaseBuilder

        Args:
            *args: iterable of @spock decorated classes
            max_indent: max indent for pretty print of help
            module_name: module name to register in the spock module space
            **kwargs: keyword args
        """
        self._input_classes = args
        self._graph = Graph(input_classes=self.input_classes)
        self._module_name = module_name
        self._max_indent = max_indent
        self.save_path = None

    @property
    def input_classes(self):
        """Returns the graph of dependencies between spock classes"""
        return self._input_classes

    @staticmethod
    @abstractmethod
    def _make_group_override_parser(parser, class_obj, class_name):
        """Makes a name specific override parser for a given class obj

        Takes a class object of the backend and adds a new argument group with argument names given with name
        Class.name so that individual parameters specific to a class can be overridden.

        *Args*:

            parser: argument parser
            class_obj: instance of a backend class
            class_name: used for module matching

        *Returns*:

            parser: argument parser with new class specific overrides

        """

    def handle_help_info(self):
        """Handles walking through classes to get help info

        For each class this function will search __doc__ and attempt to pull out help information for both the class
        itself and each attribute within the class

        *Returns*:

            None

        """
        self._attrs_help(self.input_classes, self._module_name)

    def generate(self, dict_args):
        """Method to auto-generate the actual class instances from the generated args

        Based on the generated arguments groups and the args read in from the config file(s)
        this function instantiates the classes with the necessary field or attr values

        *Args*:

            dict_args: dictionary of arguments from the configs

        *Returns*:

            namespace containing automatically generated instances of the classes
        """
        graph = Graph(input_classes=self.input_classes)
        spock_space_kwargs = self.resolve_spock_space_kwargs(graph, dict_args)
        return Spockspace(**spock_space_kwargs)

    def resolve_spock_space_kwargs(self, graph: Graph, dict_args: dict) -> dict:
        """Build the dictionary that will define the spock space.

        *Args*:

            graph: Dependency graph of nested spock configurations
            dict_args: dictionary of arguments from the configs

        *Returns*:

            dictionary containing automatically generated instances of the classes
        """

        spock_space = {}
        arguments = SpockArguments(dict_args, graph)
        builder_space = BuilderSpace(arguments=arguments, spock_space=spock_space)

        for spock_cls in graph.roots:
            spock_instance, special_keys = RegisterSpockCls.recurse_generate(
                spock_cls, builder_space
            )
            builder_space.spock_space[spock_cls.__name__] = spock_instance

            for special_key, value in special_keys.items():
                setattr(self, special_key, value)

        return spock_space

    def build_override_parsers(self, parser):
        """Creates parsers for command-line overrides

        Builds the basic command line parser for configs and help then iterates through each attr instance to make
        namespace specific cmd line override parsers

        *Args*:

            parser: argument parser

        *Returns*:

            parser: argument parser with new class specific overrides

        """
        # Build out each class override specific parser
        for val in self.input_classes:
            parser = self._make_group_override_parser(
                parser=parser, class_obj=val, class_name=self._module_name
            )
        return parser

    @staticmethod
    def _find_attribute_idx(newline_split_docs):
        """Finds the possible split between the header and Attribute annotations

        *Args*:

            newline_split_docs: new line split text

        Returns:

            idx: -1 if none or the idx of Attributes

        """
        for idx, val in enumerate(newline_split_docs):
            re_check = re.search(r"(?i)Attribute?s?:", val)
            if re_check is not None:
                return idx
        return -1

    def _split_docs(self, obj):
        """Possibly splits head class doc string from attribute docstrings

        Attempts to find the first contiguous line within the Google style docstring to use as the class docstring.
        Splits the docs base on the Attributes tag if present.

        *Args*:

            obj: class object to rip info from

        *Returns*:

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
        attr_idx = self._find_attribute_idx(newline_split_docs)
        head_docs = (
            newline_split_docs[:attr_idx] if attr_idx != -1 else newline_split_docs
        )
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

    @staticmethod
    def _match_attribute_docs(
        attr_name, attr_docs, attr_type_str, attr_default=NOTHING
    ):
        """Matches class attributes with attribute docstrings via regex

        *Args*:

            attr_name: attribute name
            attr_docs: list of attribute docstrings
            attr_type_str: str representation of the attribute type
            attr_default: str representation of a possible default value

        *Returns*:

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

    def _handle_attributes_print(self, info_dict):
        """Prints attribute information in an argparser style format

        *Args*:

            info_dict: packed attribute info dictionary to print

        """
        # Figure out indents
        max_param_length = max([len(k) for k in info_dict.keys()])
        max_type_length = max([v["len"]["type"] for v in info_dict.values()])
        # Print akin to the argparser
        for k, v in info_dict.items():
            print(
                f"    {k}"
                + (" " * (max_param_length - v["len"]["name"] + self._max_indent))
                + f'{v["type"]}'
                + (" " * (max_type_length - v["len"]["type"] + self._max_indent))
                + f'{v["desc"]} {v["default"]}'
            )
        # Blank for spacing :-/
        print("")

    def _extract_other_types(self, typed, module_name):
        """Takes a high level type and recursively extracts any enum or class types

        *Args*:

            typed: highest level type
            module_name: name of module to match

        *Returns*:

            return_list: list of nums (dot notation of module_path.enum_name or module_path.class_name)

        """
        return_list = []
        if hasattr(typed, "__args__"):
            for val in typed.__args__:
                recurse_return = self._extract_other_types(val, module_name)
                if isinstance(recurse_return, list):
                    return_list.extend(recurse_return)
                else:
                    return_list.append(self._extract_other_types(val, module_name))
        elif isinstance(typed, EnumMeta) or (typed.__module__ == module_name):
            return [f"{typed.__module__}.{typed.__name__}"]
        return return_list

    def _attrs_help(self, input_classes, module_name):
        """Handles walking through a list classes to get help info

        For each class this function will search __doc__ and attempt to pull out help information for both the class
        itself and each attribute within the class. If it finds a repeated class in a iterable object it will
        recursively call self to handle information

        *Args*:

            input_classes: list of attr classes
            module_name: name of module to match

        *Returns*:

            None

        """
        # Handle the main loop
        other_list = self._handle_help_main(input_classes, module_name)
        self._handle_help_enums(other_list=other_list, module_name=module_name)

    @staticmethod
    def _get_type_string(val, nested_others):
        """Gets the type of the attr val as a string

        *Args*:

            val: current attr being processed
            nested_others: list of nested others to deal with that might have module path info in the string

        *Returns*:

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

    def _handle_help_main(self, input_classes, module_name):
        """Handles the print of the main class types

        *Args*:

            input_classes: current set of input classes
            module_name: module name to match

        *Returns*:

            other_list: extended list of other classes/enums to process

        """
        # List to catch Enums and classes and handle post spock wrapped attr classes
        other_list = []
        covered_set = set()
        for attrs_class in input_classes:
            # Split the docs into class docs and any attribute docs
            class_doc, attr_docs = self._split_docs(attrs_class)
            print("  " + attrs_class.__name__ + f" {class_doc}")
            # Keep a running info_dict of all the attribute level info
            info_dict = {}
            for val in attrs_class.__attrs_attrs__:
                # If the type is an enum we need to handle it outside of this attr loop
                # Match the style of nested enums and return a string of module.name notation
                if isinstance(val.type, EnumMeta):
                    other_list.append(f"{val.type.__module__}.{val.type.__name__}")
                # if there is a type (implied Iterable) -- check it for nested Enums or classes
                nested_others = self._extract_fnc(val, module_name)
                if len(nested_others) > 0:
                    other_list.extend(nested_others)
                # Get the type represented as a string
                type_string = self._get_type_string(val, nested_others)
                info_dict.update(
                    self._match_attribute_docs(
                        val.name, attr_docs, type_string, val.default
                    )
                )
            # Add to covered so we don't print help twice in the case of some recursive nesting
            covered_set.add(f"{attrs_class.__module__}.{attrs_class.__name__}")
            self._handle_attributes_print(info_dict=info_dict)
        # Convert the enum list to a set to remove dupes and then back to a list so it is iterable -- set diff to not
        # repeat
        return list(set(other_list) - covered_set)

    def _handle_help_enums(self, other_list, module_name):
        """Handles any extra enums from non main args

        *Args*:

            other_list: extended list of other classes/enums to process
            module_name: module name to match

        *Returns*:

            None

        """
        # Iterate any Enum type classes
        for other in other_list:
            # if it's longer than 2 then it's an embedded Spock class
            if ".".join(other.split(".")[:-1]) == module_name:
                class_type = self._get_from_sys_modules(other)
                # Invoke recursive call for the class
                self._attrs_help([class_type], module_name)
            # Fall back to enum style
            else:
                enum = self._get_from_sys_modules(other)
                # Split the docs into class docs and any attribute docs
                class_doc, attr_docs = self._split_docs(enum)
                print("  " + enum.__name__ + f" ({class_doc})")
                info_dict = {}
                for val in enum:
                    info_dict.update(
                        self._match_attribute_docs(
                            attr_name=val.name,
                            attr_docs=attr_docs,
                            attr_type_str=type(val.value).__name__,
                        )
                    )
                self._handle_attributes_print(info_dict=info_dict)

    @abstractmethod
    def _extract_fnc(self, val, module_name):
        """Function that gets the nested lists within classes

        *Args*:

            val: current attr
            module_name: matching module name

        *Returns*:

            list of any nested classes/enums

        """

    @staticmethod
    def _get_from_sys_modules(cls_name):
        """Gets the class from a dot notation name

        *Args*:

            cls_name: dot notation enum name

        *Returns*:

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


class AttrBuilder(BaseBuilder):
    """Attr specific builder

    Class that handles building for the attr backend

    *Attributes*

        input_classes: list of input classes that link to a backend
        _configs: None or List of configs to read from
        _create_save_path: boolean to make the path to save to
        _desc: description for the arg parser
        _no_cmd_line: flag to force no command line reads
        save_path: list of path(s) to save the configs to

    """

    def __init__(self, *args, **kwargs):
        """AttrBuilder init

        Args:
            *args: list of input classes that link to a backend
            **kwargs: any extra keyword args
        """
        super().__init__(*args, module_name="spock.backend.config", **kwargs)

    @staticmethod
    def _make_group_override_parser(parser, class_obj, class_name):
        """Makes a name specific override parser for a given class obj

        Takes a class object of the backend and adds a new argument group with argument names given with name
        Class.name so that individual parameters specific to a class can be overridden.

        *Args*:

            parser: argument parser
            class_obj: instance of a backend class
            class_name: used for module matching

        *Returns*:

            parser: argument parser with new class specific overrides

        """
        attr_name = class_obj.__name__
        group_parser = parser.add_argument_group(
            title=str(attr_name) + " Specific Overrides"
        )
        for val in class_obj.__attrs_attrs__:
            val_type = val.metadata["type"] if "type" in val.metadata else val.type
            # Check if the val type has __args__ -- this catches lists?
            # TODO (ncilfone): Fix up this super super ugly logic
            if (
                hasattr(val_type, "__args__")
                and ((list(set(val_type.__args__))[0]).__module__ == class_name)
                and attr.has((list(set(val_type.__args__))[0]))
            ):
                args = list(set(val_type.__args__))[0]
                for inner_val in args.__attrs_attrs__:
                    arg_name = f"--{str(attr_name)}.{val.name}.{args.__name__}.{inner_val.name}"
                    group_parser = make_argument(
                        arg_name, List[inner_val.type], group_parser
                    )
            # If it's a reference to a class it needs to be an arg of a simple string as class matching will take care
            # of it later on
            elif val_type.__module__ == "spock.backend.config":
                arg_name = f"--{str(attr_name)}.{val.name}"
                val_type = str
                group_parser = make_argument(arg_name, val_type, group_parser)
            else:
                arg_name = f"--{str(attr_name)}.{val.name}"
                group_parser = make_argument(arg_name, val_type, group_parser)
        return parser

    def _extract_fnc(self, val, module_name):
        """Function that gets the nested lists within classes

        *Args*:

            val: current attr
            module_name: matching module name

        *Returns*:

            list of any nested classes/enums

        """
        return (
            self._extract_other_types(val.metadata["type"], module_name)
            if "type" in val.metadata
            else []
        )
