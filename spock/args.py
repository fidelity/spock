# -*- coding: utf-8 -*-

# Copyright FMR LLC <opensource@fidelity.com>
# SPDX-License-Identifier: Apache-2.0

"""Handles mapping config arguments to a payload with both general and class specific sets"""


from _warnings import warn

from spock.graph import Graph


class SpockArguments:
    """Class that handles mapping the read parameter dictionary to general or class level arguments

    Attributes:
        _arguments: dictionary of arguments

    """
    def __init__(self, arguments: dict, config_dag: Graph):
        """Init call for SpockArguments class

        Handles creating a clean arguments dictionary that can be cleanly mapped to spock classes

        Args:
            arguments: dictionary of parameters from the config file(s)
            config_dag: graph of the dependencies between spock classes

        """
        general_arguments = self._get_general_arguments(arguments, config_dag)
        attribute_name_to_config_name_mapping = (
            self._attribute_name_to_config_name_mapping(config_dag, general_arguments)
        )
        self._arguments = self._clean_arguments(arguments, general_arguments)
        self._assign_general_arguments_to_config(
            general_arguments, attribute_name_to_config_name_mapping
        )

    def __getitem__(self, item: int):
        """Gets value at idx from the _arguments dictionary

        Args:
            item: idx

        Returns:
            argument at the specified index

        """
        return self._arguments[item]

    def __iter__(self):
        """Returns the next value of the keys within the _arguments dictionary

        Returns:
            current key for the _arguments dictionary

        """
        for key in self._arguments:
            yield key

    @property
    def items(self):
        """Returns the k,v tuple iterator for the _arguments dictionary"""
        return self._arguments.items()

    @property
    def keys(self):
        """Returns an iterator for the keys of the _arguments dictionary"""
        return self._arguments.keys()

    @property
    def values(self):
        """Returns an iterator for the values of the _arguments dictionary"""
        return self._arguments.values()

    def get(self, *args, **kwargs):
        return self._arguments.get(*args, **kwargs)

    @staticmethod
    def _get_general_arguments(arguments: dict, config_dag: Graph):
        """

        Args:
            arguments: dictionary of parameters from the config file(s)
            config_dag: graph of the dependencies between spock classes

        Returns:

        """
        config_names = {n.__name__ for n in config_dag.nodes}
        return {
            key: value
            for key, value in arguments.items()
            if key not in config_names and key != "config"
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
                self._arguments[config_name] = {arg: value}

    @staticmethod
    def _clean_arguments(arguments: dict, general_arguments: dict):
        clean_arguments = {}
        for arg, value in arguments.items():
            if arg not in general_arguments:
                clean_arguments[arg] = value
        return clean_arguments


class SpockDuplicateArgumentError(Exception):
    pass
