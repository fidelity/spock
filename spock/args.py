# -*- coding: utf-8 -*-

# Copyright FMR LLC <opensource@fidelity.com>
# SPDX-License-Identifier: Apache-2.0

"""Handles import aliases to allow backwards compat with backends"""

# from spock.backend.dataclass.args import *
from _warnings import warn

from spock.backend.typed import SavePath
from spock.graph import Graph


class SpockArguments:
    def __init__(self, arguments: dict, config_dag: Graph):

        general_arguments = self._get_arguments_to_infer(arguments, config_dag)
        attribute_name_to_config_name_mapping = self._attribute_name_to_config_name_mapping(
            config_dag, general_arguments
        )
        self._arguments = self._clean_arguments(arguments, general_arguments)
        self._assign_general_arguments_to_config(
            general_arguments, attribute_name_to_config_name_mapping
        )

    def __getitem__(self, item):
        return self._arguments[item]

    def __iter__(self):
        for key in self._arguments:
            yield key

    def items(self):
        return self._arguments.items()

    def keys(self):
        return self._arguments.keys()

    def values(self):
        return self._arguments.values()

    def get(self, *args, **kwargs):
        return self._arguments.get(*args, **kwargs)

    @staticmethod
    def _get_arguments_to_infer(arguments: dict, config_dag: Graph):
        config_names = {n.__name__ for n in config_dag.nodes}
        return {
            key: value for key, value in arguments.items() if key not in config_names
        }

    def _attribute_name_to_config_name_mapping(
        self, config_dag: Graph, general_arguments: dict
    ):
        attribute_name_to_config_name_mapping = {}
        for n in config_dag.nodes:
            for attr in n.__attrs_attrs__:
                if attr.name in general_arguments:
                    if self._is_duplicated_key(
                        attribute_name_to_config_name_mapping, attr.name, n.__name__
                    ):
                        raise SpockDuplicateArgumentError(
                            f"`{attr.name}` key is located in more than one config and cannot be resolved automatically."
                            f"Either specify the config name (`<config>.{attr.name}`) or change the key name in the config."
                        )
                    attribute_name_to_config_name_mapping[attr.name] = n.__name__

        return attribute_name_to_config_name_mapping

    @staticmethod
    def _is_duplicated_key(
        attribute_name_to_config_name_mapping: dict, attr_name: str, config_name: str
    ):
        return (
            attr_name in attribute_name_to_config_name_mapping
            and attribute_name_to_config_name_mapping[attr_name] != config_name
        )

    def _assign_general_arguments_to_config(
        self, general_arguments: dict, attribute_name_to_config_name_mapping: dict
    ):
        for arg, value in general_arguments.items():
            config_name = attribute_name_to_config_name_mapping[arg]
            if config_name in self._arguments:
                # Specific arguments supersede general arguments
                if arg not in self._arguments[config_name]:
                    self._arguments[config_name][arg] = value
                else:
                    warn(
                        f"Ignoring general argument `{arg}` for config `{config_name}`\n"
                        f"Specific argument value preceded general arguments.",
                        SyntaxWarning,
                    )
            else:
                self._arguments[config_name] = {arg, value}

    @staticmethod
    def _clean_arguments(arguments: dict, general_arguments: dict):
        clean_arguments = {}
        for arg, value in arguments.items():
            if arg not in general_arguments:
                clean_arguments[arg] = value
        return clean_arguments


class SpockDuplicateArgumentError(Exception):
    pass