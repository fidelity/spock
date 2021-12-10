# -*- coding: utf-8 -*-

# Copyright FMR LLC <opensource@fidelity.com>
# SPDX-License-Identifier: Apache-2.0

"""Handles registering field attributes for spock classes -- deals with the recursive nature of dependencies"""

from abc import ABC, abstractmethod
from enum import EnumMeta

from attr import Attribute
from attr import NOTHING

from spock.args import SpockArguments
from spock.backend.spaces import AttributeSpace, BuilderSpace, ConfigSpace
from spock.utils import _check_iterable, _is_spock_instance, _is_spock_tune_instance

from typing import Type


class SpockNotOptionalError(Exception):
    """Custom exception for missing value"""
    pass


class RegisterFieldTemplate(ABC):
    """Base class for handing different field types

    Once the configuration dictionary has been assembled from the config file and the command line then we need to
    map these values to the correct spock classes -- seeing as different types need to be handled differently and
    recursive calls might be needed (when referencing other spock classes) classes derived from RegisterFieldTemplate
    handle the logic for making sure the argument dictionary passes to the instantiation of each spock class is
    correct

    Attributes:
        special_keys: dictionary to check special keys

    """
    def __init__(self):
        """Init call for RegisterFieldTemplate class

        Args:

        """
        self.special_keys = {}

    def __call__(self, attr_space: AttributeSpace, builder_space: BuilderSpace):
        if self._is_attribute_in_config_arguments(attr_space, builder_space.arguments):
            self.handle_attribute_from_config(attr_space, builder_space)
        elif self._is_attribute_optional(attr_space.attribute):
            if isinstance(attr_space.attribute.default, type):
                self.handle_optional_attribute_type(attr_space, builder_space)
            else:
                self.handle_optional_attribute_value(attr_space, builder_space)

    @staticmethod
    def _is_attribute_in_config_arguments(
        attr_space: AttributeSpace, arguments: SpockArguments
    ):
        """Checks if an attribute is in the configuration file or keyword arguments dictionary

        Args:
            attr_space: holds information about a single attribute that is mapped to a ConfigSpace
            arguments: map of the read/cmd-line parameter dictionary to general or class level arguments

        Returns:
            boolean if in dictionary

        """
        return (
            attr_space.config_space.name in arguments
            and attr_space.attribute.name in arguments[attr_space.config_space.name]
        )

    @staticmethod
    def _is_attribute_optional(attribute: Type[Attribute]):
        """Checks if an attribute is allowed to be optional

        Args:
            attribute: current attribute class

        Returns:
            boolean if the optional state is allowed

        """
        return (
            "optional" not in attribute.metadata and attribute.default is not NOTHING
        ) or ("optional" in attribute.metadata and attribute.metadata["optional"])

    def handle_optional_attribute_value(
        self, attr_space: AttributeSpace, builder_space: BuilderSpace
    ):
        """Handles setting an optional value with its default

        Args:
            attr_space: holds information about a single attribute that is mapped to a ConfigSpace
            builder_space: named_tuple containing the arguments and spock_space

        Returns:

        """
        attr_space.field = attr_space.attribute.default

    def handle_optional_attribute_type(
        self, attr_space: AttributeSpace, builder_space: BuilderSpace
    ):
        raise NotImplementedError

    @abstractmethod
    def handle_attribute_from_config(
        self, attr_space: AttributeSpace, builder_space: BuilderSpace
    ):
        pass


class RegisterList(RegisterFieldTemplate):
    """Class that registers list types

    Attributes:
        special_keys: dictionary to check special keys

    """
    def __init__(self):
        """Init call to RegisterList

        Args:

        """
        super(RegisterList, self).__init__()

    def handle_attribute_from_config(
        self, attr_space: AttributeSpace, builder_space: BuilderSpace
    ):
        list_item_spock_class = attr_space.attribute.metadata["type"].__args__[0]

        attr_space.field = self._process_list(list_item_spock_class, builder_space)

        builder_space.spock_space[list_item_spock_class.__name__] = attr_space.field

    def handle_optional_attribute_type(
        self, attr_space: AttributeSpace, builder_space: BuilderSpace
    ):
        list_item_spock_class = attr_space.attribute.default
        attr_space.field = self._process_list(list_item_spock_class, builder_space)
        builder_space.spock_space[list_item_spock_class.__name__] = attr_space.field

    def handle_optional_attribute_value(
        self, attr_space: AttributeSpace, builder_space: BuilderSpace
    ):
        super().handle_optional_attribute_value(attr_space, builder_space)
        if attr_space.field is not None:
            list_item_spock_class = attr_space.field
            builder_space.spock_space[list_item_spock_class.__name__] = attr_space.field

    @staticmethod
    def _process_list(spock_cls, builder_space: BuilderSpace):
        return [
            spock_cls(**fields)
            for fields in builder_space.arguments[spock_cls.__name__]
        ]


class RegisterEnum(RegisterFieldTemplate):
    """Class that registers enum types

    Attributes:
        special_keys: dictionary to check special keys

    """
    def __init__(self):
        """Init call to RegisterEnum

        Args:

        """
        super(RegisterEnum, self).__init__()

    def handle_attribute_from_config(
        self, attr_space: AttributeSpace, builder_space: BuilderSpace
    ):

        possible_enum_classes = {
            c.value.__name__: c.value for c in attr_space.attribute.type
        }

        enum_cls_name = builder_space.arguments[attr_space.config_space.name][
            attr_space.attribute.name
        ]
        enum_cls = possible_enum_classes[enum_cls_name]

        self._handle_and_register_enum(enum_cls, attr_space, builder_space)

    def handle_optional_attribute_type(
        self, attr_space: AttributeSpace, builder_space: BuilderSpace
    ):

        self._handle_and_register_enum(
            attr_space.attribute.default, attr_space, builder_space
        )

    def _handle_and_register_enum(
        self, enum_cls, attr_space: AttributeSpace, builder_space: BuilderSpace
    ):
        attr_space.field, special_keys = RegisterSpockCls.recurse_generate(
            enum_cls, builder_space
        )
        self.special_keys.update(special_keys)
        builder_space.spock_space[enum_cls.__name__] = attr_space.field


class RegisterSimpleField(RegisterFieldTemplate):
    """Class that registers basic python types

    Attributes:
        special_keys: dictionary to check special keys

    """
    def __init__(self):
        """Init call to RegisterSimpleField

        Args:

        """
        super(RegisterSimpleField, self).__init__()

    def handle_attribute_from_config(
        self, attr_space: AttributeSpace, builder_space: BuilderSpace
    ):
        attr_space.field = builder_space.arguments[attr_space.config_space.name][
            attr_space.attribute.name
        ]

        self.register_special_key(attr_space)

    def handle_optional_attribute_value(
        self, attr_space: AttributeSpace, builder_space: BuilderSpace
    ):
        super().handle_optional_attribute_value(attr_space, builder_space)
        self.register_special_key(attr_space)

    def register_special_key(self, attr_space: AttributeSpace):
        if (
            "special_key" in attr_space.attribute.metadata
            and attr_space.attribute.metadata["special_key"] is not None
        ):
            if attr_space.field is not None:
                self.special_keys["save_path"] = attr_space.field


class RegisterTuneCls(RegisterFieldTemplate):
    """Class that registers spock tune classes

    Attributes:
        special_keys: dictionary to check special keys

    """
    def __init__(self):
        """Init call to RegisterTuneCls

        Args:

        """
        super(RegisterTuneCls, self).__init__()

    @staticmethod
    def _attr_type(attr_space: AttributeSpace):
        return attr_space.attribute.type

    def handle_attribute_from_config(
        self, attr_space: AttributeSpace, builder_space: BuilderSpace
    ):
        attr_type = self._attr_type(attr_space)
        attr_space.field = attr_type(
            **builder_space.arguments[attr_space.config_space.name][
                attr_space.attribute.name
            ]
        )

    def handle_optional_attribute_value(
        self, attr_space: AttributeSpace, builder_space: BuilderSpace
    ):
        raise SpockNotOptionalError()

    def handle_optional_attribute_type(
        self, attr_space: AttributeSpace, builder_space: BuilderSpace
    ):
        raise SpockNotOptionalError()


class RegisterSpockCls(RegisterFieldTemplate):
    """Class that registers attributes within a spock class

    Might be called recursively so it has methods to deal with spock classes

    Attributes:
        special_keys: dictionary to check special keys

    """
    def __init__(self):
        """Init call to RegisterSpockCls

        Args:

        """
        super(RegisterSpockCls, self).__init__()

    @staticmethod
    def _attr_type(attr_space: AttributeSpace):
        return attr_space.attribute.type

    def handle_attribute_from_config(
        self, attr_space: AttributeSpace, builder_space: BuilderSpace
    ):
        attr_type = self._attr_type(attr_space)
        attr_space.field, special_keys = self.recurse_generate(attr_type, builder_space)
        builder_space.spock_space[attr_type.__name__] = attr_space.field
        self.special_keys.update(special_keys)

    def handle_optional_attribute_value(
        self, attr_space: AttributeSpace, builder_space: BuilderSpace
    ):
        super().handle_optional_attribute_value(attr_space, builder_space)

        if attr_space.field is None:
            return

        builder_space.spock_space[
            self._attr_type(attr_space).__name__
        ] = attr_space.field

    def handle_optional_attribute_type(
        self, attr_space: AttributeSpace, builder_space: BuilderSpace
    ):
        attr_space.field, special_keys = RegisterSpockCls.recurse_generate(
            self._attr_type(attr_space), builder_space
        )
        self.special_keys.update(special_keys)

        builder_space.spock_space[
            self._attr_type(attr_space).__name__
        ] = attr_space.field

    @classmethod
    def recurse_generate(cls, spock_cls, builder_space: BuilderSpace):
        special_keys = {}
        fields = {}
        # Init the ConfigSpace for this spock class
        config_space = ConfigSpace(spock_cls, fields)
        # Iterate through the attrs within the spock class
        for attribute in spock_cls.__attrs_attrs__:
            attr_space = AttributeSpace(attribute, config_space)
            # Logic to handle the underlying type to call the correct Register* class
            # Lists of repeated values
            if attribute.type is list and _is_spock_instance(
                attribute.metadata["type"].__args__[0]
            ):
                handler = RegisterList()
            # Enums
            elif isinstance(attribute.type, EnumMeta) and _check_iterable(
                attribute.type
            ):
                handler = RegisterEnum()
            # References to other spock classes
            elif _is_spock_instance(attribute.type):
                handler = RegisterSpockCls()
            # References to tuner classes
            elif _is_spock_tune_instance(attribute.type):
                handler = RegisterTuneCls()
            # Basic field
            else:
                handler = RegisterSimpleField()

            handler(attr_space, builder_space)
            special_keys.update(handler.special_keys)

        # Try except on the class since it might not be successful
        try:
            spock_instance = spock_cls(**fields)
        except Exception as e:
            raise SpockNotOptionalError(
                f"Attribute `{attr_space.attribute.name}` within `{attr_space.config_space.name}` is not optional "
                f"and is not defined in a configuration file or via command-line arguments. -- attrs: {e}")

        return spock_instance, special_keys
