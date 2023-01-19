# -*- coding: utf-8 -*-

# Copyright FMR LLC <opensource@fidelity.com>
# SPDX-License-Identifier: Apache-2.0

"""Handles the building/saving of the configurations from the Spock config classes"""
import argparse
from abc import ABC, abstractmethod
from enum import EnumMeta
from typing import ByteString, Dict, List, Optional, Set, Tuple

import attr

from spock.args import SpockArguments
from spock.backend.field_handlers import RegisterSpockCls
from spock.backend.help import attrs_help
from spock.backend.resolvers import VarResolver
from spock.backend.spaces import BuilderSpace
from spock.backend.wrappers import Spockspace
from spock.exceptions import _SpockInstantiationError
from spock.graph import Graph, MergeGraph, SelfGraph, VarGraph
from spock.utils import (
    _C,
    _T,
    _is_spock_instance_type,
    _SpockVariadicGenericAlias,
    make_argument,
)


class BaseBuilder(ABC):  # pylint: disable=too-few-public-methods
    """Base class for building the backend specific builders

    This class handles the interface to the backend with the generic ConfigArgBuilder
    so that different backends can be used to handle processing

    Attributes

        _input_classes: list of input classes that link to a backend
        _graph: Graph, graph of the dependencies between spock classes
        _max_indent: maximum to indent between help prints
        _module_name: module name to register in the spock module space
        save_path: list of path(s) to save the configs to
        _lazy: attempts to lazily find @spock decorated classes registered within
        sys.modules["spock"].backend.config
        _salt: salt use for crypto purposes
        _key: key used for crypto purposes

    """

    def __init__(
        self,
        *args,
        max_indent: int = 4,
        module_name: str,
        lazy: bool,
        salt: str,
        key: ByteString,
        **kwargs,
    ):
        """Init call for BaseBuilder

        Args:
            *args: iterable of @spock decorated classes
            max_indent: max indent for pretty print of help
            module_name: module name to register in the spock module space
            lazy: lazily find @spock decorated classes
            salt: cryptographic salt
            key: cryptographic key
            **kwargs: keyword args
        """
        self._input_classes = args
        self._lazy = lazy
        self._salt = salt
        self._key = key
        self._graph = Graph(input_classes=self.input_classes, lazy=self._lazy)
        # Make sure the input classes are updated -- lazy evaluation
        self._input_classes = self._graph.nodes
        self._module_name = module_name
        self._max_indent = max_indent
        self.save_path = None

    @property
    def input_classes(self):
        """Returns the graph of dependencies between spock classes"""
        return self._input_classes

    @property
    def dag(self):
        """Returns the underlying graph DAG"""
        return self._graph.dag

    @property
    def graph(self):
        """Returns the underlying graph object"""
        return self._graph

    @staticmethod
    @abstractmethod
    def _make_group_override_parser(
        parser: argparse.ArgumentParser, class_obj: _C, class_name: str
    ) -> argparse.ArgumentParser:
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

    def handle_help_info(self) -> None:
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

    def generate(self, dict_args: Dict) -> Spockspace:
        """Method to auto-generate the actual class instances from the generated args

        Based on the generated arguments groups and the args read in from the config file(s)
        this function instantiates the classes with the necessary field or attr values

        Args:
            dict_args: dictionary of arguments from the configs

        Returns:
            namespace containing automatically generated instances of the classes
        """
        spock_space_kwargs = self.resolve_spock_space_kwargs(self._graph, dict_args)
        return Spockspace(**spock_space_kwargs)

    def resolve_spock_space_kwargs(self, graph: Graph, dict_args: Dict) -> Dict:
        """Build the dictionary that will define the spock space.

        This is essentially the meat of the builder. Handles both the cls dep graph
        and the ref def graph. Based on that merge of the two dependency graphs
        it cal traverse the dep structure correct to resolve both cls references and
        var refs

        Args:
            graph: Dependency graph of nested spock configurations
            dict_args: dictionary of arguments from the configs

        Returns:
            dictionary containing automatically generated instances of the classes
        """
        # Assemble the arguments dictionary and BuilderSpace
        builder_space = BuilderSpace(
            arguments=SpockArguments(dict_args, graph), spock_space={}
        )
        cls_fields_dict = {}
        # For each node in the cls dep graph step through in topological order
        # We must do this first so that we can resolve the fields dict for each class
        # so that we can figure out which variables we need to resolve prior to
        # instantiation
        for spock_name in graph.topological_order:
            spock_cls = graph.node_map[spock_name]
            # This generates the fields dict for each cls
            spock_cls, special_keys, fields = RegisterSpockCls.recurse_generate(
                spock_cls, builder_space, self._salt, self._key
            )
            cls_fields_dict.update(
                {spock_cls.__name__: {"cls": spock_cls, "fields": fields}}
            )
            # Push back special keys
            for special_key, value in special_keys.items():
                setattr(self, special_key, value)
        # Create the variable dependency graph -- this needs the fields dict to do so
        # as we need all the values that are current set for instantiation
        var_graph = VarGraph(
            [(v["cls"], v["fields"]) for v in cls_fields_dict.values()],
            self._input_classes,
        )
        # Merge the cls dependency graph and the variable dependency graph
        merged_graph = MergeGraph(
            graph.dag, var_graph.dag, input_classes=self._input_classes
        )
        # Iterate in merged topological order so that we can resolve both cls and ref
        # dependencies in the correct order
        for spock_name in merged_graph.topological_order:
            # First we check for any needed cls dependent variable resolution
            cls_fields, cls_changed_vars = var_graph.resolve(
                spock_name, builder_space.spock_space
            )
            # Then we map cls references to their instantiated version
            cls_fields = self._clean_up_cls_refs(cls_fields, builder_space.spock_space)
            # Lastly we have to check for self-resolution -- we do this w/ yet another
            # graph -- graphs FTW! -- this maps back to the fields dict in the tuple
            cls_fields, var_changed_vars = SelfGraph(
                cls_fields_dict[spock_name]["cls"], cls_fields
            ).resolve()
            # Get the actual underlying class
            spock_cls = merged_graph.node_map[spock_name]
            # Merge the changed sets -- then attempt to cast them all post resolution
            self._cast_all_maps(
                spock_cls, cls_fields, cls_changed_vars | var_changed_vars
            )
            # Once all resolution occurs we attempt to instantiate the cls
            try:
                spock_instance = spock_cls(**cls_fields)
            except Exception as e:
                raise _SpockInstantiationError(
                    f"Spock class `{spock_cls.__name__}` could not be instantiated "
                    f"-- attrs message: {e}"
                )
            # Push back into the builder_space
            builder_space.spock_space[spock_cls.__name__] = spock_instance
        return builder_space.spock_space

    @staticmethod
    def _cast_all_maps(cls, cls_fields: Dict, changed_vars: Set) -> None:
        """Casts all the resolved references to the requested type

        Args:
            cls: current spock class
            cls_fields: current fields dictionary to attempt cast within
            changed_vars: set of resolved variables that need to be cast

        Returns:

        """
        for val in changed_vars:
            cls_fields[val] = VarResolver._attempt_cast(
                maybe_env=cls_fields[val],
                value_type=getattr(cls.__attrs_attrs__, val).type,
                ref_value=val,
            )

    @staticmethod
    def _clean_up_cls_refs(fields: Dict, spock_space: Dict) -> Dict:
        """Swaps in the newly created cls if it hasn't been instantiated yet

        Args:
            fields: current field dictionary
            spock_space: current spock space dictionary

        Returns:
            updated fields dictionary

        """
        for k, v in fields.items():
            # If it is an uninstantiated spock instance then swap in the
            # instantiated class
            if _is_spock_instance_type(v):
                fields.update({k: spock_space[v.__name__]})
        return fields

    def build_override_parsers(
        self, parser: argparse.ArgumentParser
    ) -> argparse.ArgumentParser:
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

    def _extract_other_types(self, typed: _T, module_name: str) -> List:
        """Takes a high level type and recursively extracts any enum or class types

        Args:
            typed: highest level type
            module_name: name of module to match

        Returns:
            return_list: list of nums (dot notation of module_path.enum_name or module_path.class_name)

        """
        return_list = []
        if hasattr(typed, "__args__") and not isinstance(
            typed, _SpockVariadicGenericAlias
        ):
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
    def _make_group_override_parser(
        parser: argparse.ArgumentParser, class_obj: _C, class_name: str
    ) -> argparse.ArgumentParser:
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
            # Check if the val type has __args__ -- this catches GenericAlias classes
            # TODO (ncilfone): Fix up this super super ugly logic
            if (
                not isinstance(val_type, _SpockVariadicGenericAlias)
                and hasattr(val_type, "__args__")
                and ((list(set(val_type.__args__))[0]).__module__ == class_name)
                and attr.has((list(set(val_type.__args__))[0]))
            ):
                args = list(set(val_type.__args__))[0]
                for inner_val in args.__attrs_attrs__:
                    arg_name = f"--{str(attr_name)}.{val.name}.{args.__name__}.{inner_val.name}"
                    group_parser = make_argument(
                        arg_name, List[inner_val.type], group_parser
                    )
            # If it's a reference to a class it needs to be an arg of a simple string
            # as class matching will take care
            # of it later on
            elif val_type.__module__ == "spock.backend.config":
                arg_name = f"--{str(attr_name)}.{val.name}"
                val_type = str
                group_parser = make_argument(arg_name, val_type, group_parser)
            # This catches callables -- need to be of type str which will be use in
            # importlib
            elif isinstance(val.type, _SpockVariadicGenericAlias):
                arg_name = f"--{str(attr_name)}.{val.name}"
                group_parser = make_argument(arg_name, str, group_parser)
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
