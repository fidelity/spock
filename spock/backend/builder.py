# -*- coding: utf-8 -*-

# Copyright FMR LLC <opensource@fidelity.com>
# SPDX-License-Identifier: Apache-2.0

"""Handles the building/saving of the configurations from the Spock config classes"""

from abc import ABC, abstractmethod
from enum import EnumMeta
from typing import List

import attr

from spock.args import SpockArguments
from spock.backend.field_handlers import RegisterSpockCls
from spock.backend.help import attrs_help
from spock.backend.spaces import BuilderSpace
from spock.backend.wrappers import Spockspace
from spock.graph import Graph
from spock.utils import make_argument


class BaseBuilder(ABC):  # pylint: disable=too-few-public-methods
    """Base class for building the backend specific builders

    This class handles the interface to the backend with the generic ConfigArgBuilder so that different
    backends can be used to handle processing

    Attributes

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

        Args:
            parser: argument parser
            class_obj: instance of a backend class
            class_name: used for module matching

        Returns:
            parser: argument parser with new class specific overrides

        """

    def handle_help_info(self):
        """Handles walking through classes to get help info

        For each class this function will search __doc__ and attempt to pull out help information for both the class
        itself and each attribute within the class

        Returns:
            None

        """
        attrs_help(
            input_classes=self.input_classes,
            module_name=self._module_name,
            extract_fnc=self._extract_fnc,
            max_indent=self._max_indent,
        )

    def generate(self, dict_args):
        """Method to auto-generate the actual class instances from the generated args

        Based on the generated arguments groups and the args read in from the config file(s)
        this function instantiates the classes with the necessary field or attr values

        Args:
            dict_args: dictionary of arguments from the configs

        Returns:
            namespace containing automatically generated instances of the classes
        """
        graph = Graph(input_classes=self.input_classes)
        spock_space_kwargs = self.resolve_spock_space_kwargs(graph, dict_args)
        return Spockspace(**spock_space_kwargs)

    def resolve_spock_space_kwargs(self, graph: Graph, dict_args: dict) -> dict:
        """Build the dictionary that will define the spock space.

        Args:
            graph: Dependency graph of nested spock configurations
            dict_args: dictionary of arguments from the configs

        Returns:
            dictionary containing automatically generated instances of the classes
        """
        # Empty dictionary that will be mapped to a SpockSpace via spock classes
        spock_space = {}
        # Assemble the arguments dictionary and BuilderSpace
        builder_space = BuilderSpace(
            arguments=SpockArguments(dict_args, graph), spock_space=spock_space
        )
        # For each root recursively step through the definitions
        for spock_cls in graph.roots:
            # Initial call to the RegisterSpockCls generate function (which will handle recursing if needed)
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

        Args:
            parser: argument parser

        Returns:
            parser: argument parser with new class specific overrides

        """
        # Build out each class override specific parser
        for val in self.input_classes:
            parser = self._make_group_override_parser(
                parser=parser, class_obj=val, class_name=self._module_name
            )
        return parser

    def _extract_other_types(self, typed, module_name):
        """Takes a high level type and recursively extracts any enum or class types

        Args:
            typed: highest level type
            module_name: name of module to match

        Returns:
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

    @abstractmethod
    def _extract_fnc(self, val, module_name):
        """Function that gets the nested lists within classes

        Args:
            val: current attr
            module_name: matching module name

        Returns:
            list of any nested classes/enums

        """


class AttrBuilder(BaseBuilder):
    """Attr specific builder

    Class that handles building for the attr backend

    Attributes

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

        Args:
            parser: argument parser
            class_obj: instance of a backend class
            class_name: used for module matching

        Returns:
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

        Args:
            val: current attr
            module_name: matching module name

        Returns:
            list of any nested classes/enums

        """
        return (
            self._extract_other_types(val.metadata["type"], module_name)
            if "type" in val.metadata
            else []
        )
