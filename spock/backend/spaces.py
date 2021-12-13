# -*- coding: utf-8 -*-

# Copyright FMR LLC <opensource@fidelity.com>
# SPDX-License-Identifier: Apache-2.0

"""Handles classes/named tuples for holding class, field, and attribute value(s)"""

from collections import namedtuple
from typing import Type

from attr import Attribute


class ConfigSpace:
    """Class that holds information about the final values of spock class attributes

    Attributes:
        spock_cls: reference to spock class to store information
        fields: dictionary of the current value of attributes

    """

    def __init__(self, spock_cls: Type, fields: dict):
        """Init call for ConfigSpace class

        Args:
            spock_cls: reference to spock class to store information
            fields: dictionary of the current value of attributes

        """
        self.spock_cls = spock_cls
        self.fields = fields

    @property
    def name(self) -> str:
        """Returns the name of the spock class associated with ConfigSpace"""
        return self.spock_cls.__name__


class AttributeSpace:
    """Class that holds information about a single attribute that is mapped to a ConfigSpace

    Attributes:
        config_space: ConfigSpace that the attribute is contained in
        attribute: current Attribute class

    """

    def __init__(self, attribute: Type[Attribute], config_space: ConfigSpace):
        """Init call for AttributeSpace class

        Args:
            config_space: ConfigSpace that the attribute is contained in
            attribute: current Attribute class
        """
        self.config_space = config_space
        self.attribute = attribute

    @property
    def field(self):
        """Returns the field value from the ConfigSpace based on the attribute name"""
        return self.config_space.fields[self.attribute.name]

    @field.setter
    def field(self, value):
        """Setter for the field value from the ConfigSpace based on the attribute name"""
        if isinstance(self.attribute.name, str):
            self.config_space.fields[self.attribute.name] = value
        else:
            raise ValueError


BuilderSpace = namedtuple("BuilderSpace", ["arguments", "spock_space"])
