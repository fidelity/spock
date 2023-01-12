# -*- coding: utf-8 -*-

# Copyright FMR LLC <opensource@fidelity.com>
# SPDX-License-Identifier: Apache-2.0

"""Handles registering field attributes for spock classes -- deals with the recursive nature of dependencies"""

import importlib
import sys
from abc import ABC, abstractmethod
from enum import EnumMeta
from typing import Any, ByteString, Callable, Dict, List, Tuple, Type

from attr import NOTHING, Attribute

from spock.backend.resolvers import CryptoResolver, EnvResolver, VarResolver
from spock.backend.spaces import AttributeSpace, BuilderSpace, ConfigSpace
from spock.backend.utils import (
    _get_name_py_version,
    _recurse_callables,
    _str_2_callable,
    encrypt_value,
)
from spock.exceptions import (
    _SpockFieldHandlerError,
    _SpockInstantiationError,
    _SpockNotOptionalError,
)
from spock.utils import (
    _C,
    _T,
    _check_iterable,
    _is_spock_instance,
    _is_spock_tune_instance,
    _SpockVariadicGenericAlias,
)


class RegisterFieldTemplate(ABC):
    """Base class for handing different field types

    Once the configuration dictionary has been assembled from the config file and the command line then we need to
    map these values to the correct spock classes -- seeing as different types need to be handled differently and
    recursive calls might be needed (when referencing other spock classes) classes derived from RegisterFieldTemplate
    handle the logic for making sure the argument dictionary passes to the instantiation of each spock class is
    correct

    Attributes:
        special_keys: dictionary to check special keys
        _salt: salt used for cryptograpy
        _key: key used for cryptography
        _env_resolver: class used to resolve environmental variables
        _crypto_resolver: class used to resolve cryptographic variables
    """

    # As these are un-parametrized we can make them class variables
    _env_resolver = EnvResolver()
    _var_resolver = VarResolver()

    def __init__(self, salt: str, key: ByteString):
        """Init call for RegisterFieldTemplate class

        Args:
            salt: salt used for cryptograpy
            key: key used for cryptography
        """
        self.special_keys = {}
        self._salt = salt
        self._key = key
        # self._env_resolver = EnvResolver()
        self._crypto_resolver = CryptoResolver(self._salt, self._key)

    def __call__(self, attr_space: AttributeSpace, builder_space: BuilderSpace):
        """Call method for RegisterFieldTemplate

        Handles calling the correct method for the type of the attribute

        Args:
            attr_space: holds information about a single attribute that is mapped to a ConfigSpace
            builder_space: named_tuple containing the arguments and spock_space

        Returns:
        """
        if self._is_attribute_in_config_arguments(attr_space, builder_space):
            self.handle_attribute_from_config(attr_space, builder_space)
        elif self._is_attribute_optional(attr_space.attribute):
            if isinstance(attr_space.attribute.default, type):
                self.handle_optional_attribute_type(attr_space, builder_space)
            else:
                self.handle_optional_attribute_value(attr_space, builder_space)

    def _is_attribute_in_config_arguments(
        self, attr_space: AttributeSpace, builder_space: BuilderSpace
    ):
        """Checks if an attribute is in the configuration file or keyword arguments dictionary

        Will recurse spock classes as dependencies might be defined in the configs class

        Args:
            attr_space: holds information about a single attribute that is mapped to a ConfigSpace
            builder_space: map of the read/cmd-line parameter dictionary to general or class level arguments

        Returns:
            boolean if in dictionary

        """
        # Instances might have other instances that might be defined in the configs
        # Recurse to try and catch all config defs
        # Only map if default is not None -- do so by evolving the attribute
        if (
            _is_spock_instance(attr_space.attribute.type)
            and attr_space.attribute.default is not None
        ):
            # fields, special_keys, annotations, crypto = RegisterSpockCls(
            #     self._salt, self._key
            # ).recurse_generate(
            #     attr_space.attribute.type, builder_space, self._salt, self._key
            # )

            attr_space.field, special_keys, _ = RegisterSpockCls(
                self._salt, self._key
            ).recurse_generate(
                attr_space.attribute.type, builder_space, self._salt, self._key
            )
            attr_space.attribute = attr_space.attribute.evolve(default=attr_space.field)
            # builder_space.spock_space[
            #     attr_space.attribute.type.__name__
            # ] = attr_space.field
            self.special_keys.update(special_keys)
        return (
            attr_space.config_space.name in builder_space.arguments
            and attr_space.attribute.name
            in builder_space.arguments[attr_space.config_space.name]
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

        value, env_annotation = self._env_resolver.resolve(
            attr_space.attribute.default, attr_space.attribute.type
        )
        if env_annotation is not None:
            self._handle_env_annotations(
                attr_space, env_annotation, value, attr_space.attribute.default
            )
        value, crypto_annotation = self._crypto_resolver.resolve(
            value, attr_space.attribute.type
        )
        if crypto_annotation is not None:
            self._handle_crypto_annotations(
                attr_space, crypto_annotation, attr_space.attribute.default
            )
        attr_space.field = value

    def _handle_env_annotations(
        self, attr_space: AttributeSpace, annotation: str, value: Any, og_value: Any
    ):
        if annotation == "crypto":
            # Take the current value to string and then encrypt
            attr_space.annotations = (
                f"${{spock.crypto:{encrypt_value(str(value), self._key, self._salt)}}}"
            )
            attr_space.crypto = True
        elif annotation == "inject":
            attr_space.annotations = og_value
        else:
            raise _SpockInstantiationError(f"Got unknown env annotation `{annotation}`")

    @staticmethod
    def _handle_crypto_annotations(
        attr_space: AttributeSpace, annotation: str, og_value: str
    ):
        if annotation == "crypto":
            attr_space.annotations = og_value
            attr_space.crypto = True
        else:
            raise _SpockInstantiationError(
                f"Got unknown crypto annotation `{annotation}`"
            )

    @abstractmethod
    def handle_optional_attribute_type(
        self, attr_space: AttributeSpace, builder_space: BuilderSpace
    ):
        pass

    @abstractmethod
    def handle_attribute_from_config(
        self, attr_space: AttributeSpace, builder_space: BuilderSpace
    ):
        pass


class RegisterEnum(RegisterFieldTemplate):
    """Class that registers enum types

    Attributes:
        special_keys: dictionary to check special keys
        _salt: salt used for cryptograpy
        _key: key used for cryptography
        _env_resolver: class used to resolve environmental variables
        _crypto_resolver: class used to resolve cryptographic variables

    """

    def __init__(self, salt: str, key: ByteString):
        """Init call to RegisterEnum

        Args:
            salt: salt used for cryptograpy
            key: key used for cryptography
        """
        super(RegisterEnum, self).__init__(salt, key)

    def handle_attribute_from_config(
        self, attr_space: AttributeSpace, builder_space: BuilderSpace
    ):
        """Handles getting the attribute set value when the Enum is made up of spock classes

        Args:
            attr_space: holds information about a single attribute that is mapped to a ConfigSpace
            builder_space: named_tuple containing the arguments and spock_space

        Returns:
        """
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
        """Handles falling back on the optional default for a type based attribute

        Args:
            attr_space: holds information about a single attribute that is mapped
                to a ConfigSpace
            builder_space: named_tuple containing the arguments and spock_space

        Returns:
        """
        self._handle_and_register_enum(
            attr_space.attribute.default, attr_space, builder_space
        )

    def handle_optional_attribute_value(
        self, attr_space: AttributeSpace, builder_space: BuilderSpace
    ):
        """Handles setting an optional value with its default

        Args:
            attr_space: holds information about a single attribute that is mapped
                to a ConfigSpace
            builder_space: named_tuple containing the arguments and spock_space

        Returns:
        """
        super().handle_optional_attribute_value(attr_space, builder_space)
        # if attr_space.field is not None:
        #     builder_space.spock_space[
        #         type(attr_space.field).__name__
        #     ] = attr_space.field

    def _handle_and_register_enum(
        self, enum_cls, attr_space: AttributeSpace, builder_space: BuilderSpace
    ):
        """Recurse the enum in case there are nested type definitions

        Args:
            enum_cls: current enum class
            attr_space: holds information about a single attribute that is mapped
                to a ConfigSpace
            builder_space: named_tuple containing the arguments and spock_space

        Returns:
        """
        attr_space.field, special_keys, _ = RegisterSpockCls.recurse_generate(
            enum_cls, builder_space, self._salt, self._key
        )
        self.special_keys.update(special_keys)
        # builder_space.spock_space[enum_cls.__name__] = attr_space.field


class RegisterCallableField(RegisterFieldTemplate):
    """Class that registers callable types

    Attributes:
        special_keys: dictionary to check special keys
        _salt: salt used for cryptograpy
        _key: key used for cryptography
        _env_resolver: class used to resolve environmental variables
        _crypto_resolver: class used to resolve cryptographic variables

    """

    def __init__(self, salt: str, key: ByteString):
        """Init call to RegisterSimpleField

        Args:
            salt: salt used for cryptograpy
            key: key used for cryptography
        """
        super(RegisterCallableField, self).__init__(salt, key)

    def handle_attribute_from_config(
        self, attr_space: AttributeSpace, builder_space: BuilderSpace
    ):
        """Handles setting a simple attribute when it is a spock class type

        Args:
            attr_space: holds information about a single attribute that is mapped to a ConfigSpace
            builder_space: named_tuple containing the arguments and spock_space

        Returns:
        """
        # These should always be strings
        str_field = builder_space.arguments[attr_space.config_space.name][
            attr_space.attribute.name
        ]
        call_ref = _str_2_callable(str_field)
        attr_space.field = call_ref

    def handle_optional_attribute_type(
        self, attr_space: AttributeSpace, builder_space: BuilderSpace
    ):
        """Not implemented for this type

        Args:
            attr_space: holds information about a single attribute that is mapped to a ConfigSpace
            builder_space: named_tuple containing the arguments and spock_space

        Raises:
            _SpockNotOptionalError

        """
        raise _SpockNotOptionalError(
            f"Parameter `{attr_space.attribute.name}` within `{attr_space.config_space.name}` is of "
            f"type `{type(attr_space.attribute.type)}` which seems to be unsupported -- "
            f"are you missing an @spock decorator on a base python class?"
        )


class RegisterGenericAliasCallableField(RegisterFieldTemplate):
    """Class that registers Dicts containing callable types

    Attributes:
        special_keys: dictionary to check special keys
        _salt: salt used for cryptograpy
        _key: key used for cryptography
        _env_resolver: class used to resolve environmental variables
        _crypto_resolver: class used to resolve cryptographic variables

    """

    def __init__(self, salt: str, key: ByteString):
        """Init call to RegisterSimpleField

        Args:
            salt: salt used for cryptograpy
            key: key used for cryptography
        """
        super(RegisterGenericAliasCallableField, self).__init__(salt, key)

    def handle_attribute_from_config(
        self, attr_space: AttributeSpace, builder_space: BuilderSpace
    ):
        """Handles setting a simple attribute when it is a spock class type

        Args:
            attr_space: holds information about a single attribute that is mapped to a ConfigSpace
            builder_space: named_tuple containing the arguments and spock_space

        Returns:
        """
        typed = attr_space.attribute.metadata["type"]
        out = None
        # Handle List Types
        if (
            _get_name_py_version(typed) == "List"
            or _get_name_py_version(typed) == "Tuple"
        ):
            out = []
            for v in builder_space.arguments[attr_space.config_space.name][
                attr_space.attribute.name
            ]:
                out.append(_recurse_callables(v, _str_2_callable))
        # Handle Dict Types
        elif _get_name_py_version(typed) == "Dict":
            out = {}
            for k, v in builder_space.arguments[attr_space.config_space.name][
                attr_space.attribute.name
            ].items():
                out.update({k: _recurse_callables(v, _str_2_callable)})
        attr_space.field = out

    def handle_optional_attribute_type(
        self, attr_space: AttributeSpace, builder_space: BuilderSpace
    ):
        """Not implemented for this type

        Args:
            attr_space: holds information about a single attribute that is mapped to a ConfigSpace
            builder_space: named_tuple containing the arguments and spock_space

        Raises:
            _SpockNotOptionalError

        """
        raise _SpockNotOptionalError(
            f"Parameter `{attr_space.attribute.name}` within `{attr_space.config_space.name}` is of "
            f"type `{type(attr_space.attribute.type)}` which seems to be unsupported -- "
            f"are you missing an @spock decorator on a base python class?"
        )


class RegisterSimpleField(RegisterFieldTemplate):
    """Class that registers basic python types

    Attributes:
        special_keys: dictionary to check special keys
        _salt: salt used for cryptograpy
        _key: key used for cryptography
        _env_resolver: class used to resolve environmental variables
        _crypto_resolver: class used to resolve cryptographic variables

    """

    def __init__(self, salt: str, key: ByteString):
        """Init call to RegisterSimpleField

        Args:
            salt: salt used for cryptograpy
            key: key used for cryptography
        """
        super(RegisterSimpleField, self).__init__(salt, key)

    def handle_attribute_from_config(
        self, attr_space: AttributeSpace, builder_space: BuilderSpace
    ):
        """Handles setting a simple attribute from a config file

        Args:
            attr_space: holds information about a single attribute that is mapped to a ConfigSpace
            builder_space: named_tuple containing the arguments and spock_space

        Returns:
        """
        og_value = builder_space.arguments[attr_space.config_space.name][
            attr_space.attribute.name
        ]
        value, env_annotation = self._env_resolver.resolve(
            og_value, attr_space.attribute.type
        )
        if env_annotation is not None:
            self._handle_env_annotations(attr_space, env_annotation, value, og_value)
        value, crypto_annotation = self._crypto_resolver.resolve(
            value, attr_space.attribute.type
        )
        if crypto_annotation is not None:
            self._handle_crypto_annotations(attr_space, crypto_annotation, og_value)
            attr_space.crypto = True
        attr_space.field = value
        self.register_special_key(attr_space)

    def handle_optional_attribute_type(
        self, attr_space: AttributeSpace, builder_space: BuilderSpace
    ):
        """Not implemented for this type

        Args:
            attr_space: holds information about a single attribute that is mapped to a ConfigSpace
            builder_space: named_tuple containing the arguments and spock_space

        Raises:
            _SpockNotOptionalError

        """
        raise _SpockNotOptionalError(
            f"Parameter `{attr_space.attribute.name}` within "
            f"`{attr_space.config_space.name}` is of "
            f"type `{type(attr_space.attribute.type)}` which seems to be "
            f"unsupported -- "
            f"are you missing an @spock decorator on a base python class?"
        )

    def handle_optional_attribute_value(
        self, attr_space: AttributeSpace, builder_space: BuilderSpace
    ):
        """Handles setting the attribute from default if optional

        Also checks for clashes with special keys

        Args:
            attr_space: holds information about a single attribute that is mapped to a ConfigSpace
            builder_space: named_tuple containing the arguments and spock_space

        Returns:
        """
        super().handle_optional_attribute_value(attr_space, builder_space)
        self.register_special_key(attr_space)

    def register_special_key(self, attr_space: AttributeSpace):
        """Registers a special key if it is found in the attribute metadata

        Args:
            attr_space: holds information about a single attribute that is mapped to a ConfigSpace

        Returns:
        """
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
        _salt: salt used for cryptograpy
        _key: key used for cryptography
        _env_resolver: class used to resolve environmental variables
        _crypto_resolver: class used to resolve cryptographic variables

    """

    def __init__(self, salt: str, key: ByteString):
        """Init call to RegisterTuneCls

        Args:
            salt: salt used for cryptograpy
            key: key used for cryptography
        """
        super(RegisterTuneCls, self).__init__(salt, key)

    @staticmethod
    def _attr_type(attr_space: AttributeSpace):
        """Gets the attribute type

        Args:
            attr_space: holds information about a single attribute that is mapped to a ConfigSpace

        Returns:
            the type of the attribute

        """
        return attr_space.attribute.type

    def handle_attribute_from_config(
        self, attr_space: AttributeSpace, builder_space: BuilderSpace
    ):
        """Handles when the spock tune class is made up of spock classes

        Args:
            attr_space: holds information about a single attribute that is mapped to a ConfigSpace
            builder_space: named_tuple containing the arguments and spock_space

        Returns:
        """
        attr_type = self._attr_type(attr_space)
        attr_space.field = attr_type(
            **builder_space.arguments[attr_space.config_space.name][
                attr_space.attribute.name
            ]
        )

    def handle_optional_attribute_value(
        self, attr_space: AttributeSpace, builder_space: BuilderSpace
    ):
        """Not implemented for this type

        Args:
            attr_space: holds information about a single attribute that is mapped to a ConfigSpace
            builder_space: named_tuple containing the arguments and spock_space

        Raises:
            _SpockNotOptionalError

        """
        raise _SpockNotOptionalError()

    def handle_optional_attribute_type(
        self, attr_space: AttributeSpace, builder_space: BuilderSpace
    ):
        """Not implemented for this type

        Args:
            attr_space: holds information about a single attribute that is mapped to a ConfigSpace
            builder_space: named_tuple containing the arguments and spock_space

        Raises:
            _SpockNotOptionalError

        """
        raise _SpockNotOptionalError()


class RegisterSpockCls(RegisterFieldTemplate):
    """Class that registers attributes within a spock class

    Might be called recursively so it has methods to deal with spock classes when
    invoked via the __call__ method

    Attributes:
        special_keys: dictionary to check special keys
        _salt: salt used for cryptograpy
        _key: key used for cryptography
        _env_resolver: class used to resolve environmental variables
        _crypto_resolver: class used to resolve cryptographic variables

    """

    def __init__(self, salt: str, key: ByteString):
        """Init call to RegisterSpockCls

        Args:
            salt: salt used for cryptograpy
            key: key used for cryptography
        """
        super(RegisterSpockCls, self).__init__(salt, key)

    @staticmethod
    def _attr_type(attr_space: AttributeSpace):
        """Gets the attribute type

        Args:
            attr_space: holds information about a single attribute that is mapped to a
            ConfigSpace

        Returns:
            the type of the attribute

        """
        return attr_space.attribute.type

    def handle_attribute_from_config(
        self, attr_space: AttributeSpace, builder_space: BuilderSpace
    ):
        """Handles when the attribute is made up of a spock class or classes

        Calls the recurse_generate function which handles nesting of spock classes

        Args:
            attr_space: holds information about a single attribute that is mapped to a
            ConfigSpace
            builder_space: named_tuple containing the arguments and spock_space

        Returns:
        """
        attr_type = self._attr_type(attr_space)
        attr_space.field, special_keys, _ = self.recurse_generate(
            attr_type, builder_space, self._salt, self._key
        )
        # builder_space.spock_space[attr_type.__name__] = attr_space.field
        self.special_keys.update(special_keys)

    def handle_optional_attribute_value(
        self, attr_space: AttributeSpace, builder_space: BuilderSpace
    ):
        """Handles when the falling back onto the default for the attribute of spock
        class type and the field value
        already exits within the attr_space

        Args:
            attr_space: holds information about a single attribute that is mapped
            to a ConfigSpace
            builder_space: named_tuple containing the arguments and spock_space

        Returns:
        """
        super().handle_optional_attribute_value(attr_space, builder_space)
        # if attr_space.field is None:
        #     return
        # builder_space.spock_space[
        #     self._attr_type(attr_space).__name__
        # ] = attr_space.field

    def handle_optional_attribute_type(
        self, attr_space: AttributeSpace, builder_space: BuilderSpace
    ):
        """Handles when the falling back onto the default for the attribute of spock class type

        Calls the recurse_generate function which handles nesting of spock classes
        -- to make sure the attr_space.field value is defined

        Args:
            attr_space: holds information about a single attribute that is mapped to a ConfigSpace
            builder_space: named_tuple containing the arguments and spock_space

        Returns:
        """
        attr_space.field, special_keys, _ = RegisterSpockCls.recurse_generate(
            self._attr_type(attr_space), builder_space, self._salt, self._key
        )
        self.special_keys.update(special_keys)

        # builder_space.spock_space[
        #     self._attr_type(attr_space).__name__
        # ] = attr_space.field

    @classmethod
    def _find_callables(cls, typed: _T):
        """Attempts to find callables nested in Lists, Tuples, or Dicts

        Args:
            typed: input type

        Returns:
            boolean if callables are found

        """
        out = False
        if hasattr(typed, "__args__"):
            if (
                _get_name_py_version(typed) == "List"
                or _get_name_py_version(typed) == "Tuple"
            ):
                # Possibly nested Callables
                if not isinstance(typed.__args__[0], _SpockVariadicGenericAlias):
                    out = cls._find_callables(typed.__args__[0])
                # Found callables
                elif isinstance(typed.__args__[0], _SpockVariadicGenericAlias):
                    out = True
            elif _get_name_py_version(typed) == "Dict":
                key_type, value_type = typed.__args__
                if not isinstance(value_type, _SpockVariadicGenericAlias):
                    out = cls._find_callables(value_type)
                elif isinstance(value_type, _SpockVariadicGenericAlias):
                    out = True
            else:
                raise TypeError(
                    f"Unexpected type of `{str(typed)}` when attempting to handle GenericAlias types"
                )
        return out

    @classmethod
    def recurse_generate(
        cls, spock_cls: _C, builder_space: BuilderSpace, salt: str, key: ByteString
    ):
        """Call on a spock classes to iterate through the attrs attributes and handle each based on type and optionality

        Triggers a recursive call when an attribute refers to another spock classes

        Args:
            spock_cls: current spock class that is being handled
            builder_space: named_tuple containing the arguments and spock_space
            salt: salt used for cryptograpy
            key: key used for cryptography

        Returns:
            tuple of the instantiated spock class, the dictionary of special keys,
            and the info tuple of the original class and attempted payload

        """
        # Empty dits for storing info
        special_keys = {}
        fields = {}
        annotations = {}
        crypto = False
        # Init the ConfigSpace for this spock class
        config_space = ConfigSpace(spock_cls, fields)
        # Iterate through the attrs within the spock class
        for attribute in spock_cls.__attrs_attrs__:
            attr_space = AttributeSpace(attribute, config_space)
            # Logic to handle the underlying type to call the correct Register* class
            # Lists of repeated values
            # if (
            #     (attribute.type is list) or (attribute.type is List)
            # ) and _is_spock_instance(attribute.metadata["type"].__args__[0]):
            #     handler = RegisterList(salt, key)
            # Wrap this in a try except to gracefully handle when a handler isn't
            # correct
            try:
                # Dict/List of Callables
                if (
                    (attribute.type is list)
                    or (attribute.type is List)
                    or (attribute.type is dict)
                    or (attribute.type is Dict)
                    or (attribute.type is tuple)
                    or (attribute.type is Tuple)
                ) and cls._find_callables(attribute.metadata["type"]):
                    handler = RegisterGenericAliasCallableField(salt, key)
                # Enums
                elif isinstance(attribute.type, EnumMeta) and _check_iterable(
                    attribute.type
                ):
                    handler = RegisterEnum(salt, key)
                # References to other spock classes
                elif _is_spock_instance(attribute.type):
                    handler = RegisterSpockCls(salt, key)
                # References to tuner classes
                elif _is_spock_tune_instance(attribute.type):
                    handler = RegisterTuneCls(salt, key)
                # References to callables
                elif isinstance(attribute.type, _SpockVariadicGenericAlias):
                    handler = RegisterCallableField(salt, key)
                # Basic field -- this might fail -- should we try catch here?
                else:
                    handler = RegisterSimpleField(salt, key)
                # Call the handler
                handler(attr_space, builder_space)
                # Update any special keys
                special_keys.update(handler.special_keys)
            except Exception as e:
                raise _SpockFieldHandlerError(
                    f"Could not handle attribute "
                    f"(name: `{attribute.name}`, type: `{attribute.type}`): "
                    f"{e}"
                )
            # Handle annotations by attaching them to a dictionary
            if attr_space.annotations is not None:
                annotations.update({attr_space.attribute.name: attr_space.annotations})
            if attr_space.crypto:
                crypto = True
        # If there are annotations attach them to the spock class
        # in the __resolver__ attribute
        if len(annotations) > 0:
            spock_cls.__resolver__ = annotations
        if crypto:
            spock_cls.__crypto__ = True
        return spock_cls, special_keys, fields
