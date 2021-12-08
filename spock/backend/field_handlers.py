from abc import ABC, abstractmethod
from enum import EnumMeta

from attr import NOTHING

from spock.args import SpockArguments
from spock.backend.spaces import AttributeSpace, BuilderSpace, ConfigSpace
from spock.utils import _check_iterable, _is_spock_instance, _is_spock_tune_instance


class SpockNotOptionalError(Exception):
    pass


class RegisterFieldTemplate(ABC):
    def __init__(self):
        self.special_keys = {}

    def __call__(self, attr_space: AttributeSpace, builder_space: BuilderSpace):
        if self._is_attribute_in_config_arguments(attr_space, builder_space.arguments):
            self.handle_attribute_from_config(attr_space, builder_space)
        elif self._is_attribute_optional(attr_space.attribute):
            if isinstance(attr_space.attribute.default, type):
                self.handle_optional_attribute_type(attr_space, builder_space)
            else:
                self.handle_optional_attribute_value(attr_space, builder_space)
        else:
            self.other(attr_space, builder_space)

    @staticmethod
    def _is_attribute_in_config_arguments(
        attr_space: AttributeSpace, arguments: SpockArguments
    ):
        return (
            attr_space.config_space.name in arguments
            and attr_space.attribute.name in arguments[attr_space.config_space.name]
        )

    @staticmethod
    def _is_attribute_optional(attribute):
        return (
            "optional" not in attribute.metadata and not attribute.default is NOTHING
        ) or ("optional" in attribute.metadata and attribute.metadata["optional"])

    def other(self, attr_space: AttributeSpace, builder_space: BuilderSpace):
        raise SpockNotOptionalError(
            f"Attribute `{attr_space.attribute.name}` is not provided in "
            f"config arguments and is not optional."
        )

    def handle_optional_attribute_value(
        self, attr_space: AttributeSpace, builder_space: BuilderSpace
    ):
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

        special_keys, fields = {}, {}
        config_space = ConfigSpace(spock_cls, fields)

        for attribute in spock_cls.__attrs_attrs__:
            attr_space = AttributeSpace(attribute, config_space)

            if attribute.type is list and _is_spock_instance(
                attribute.metadata["type"].__args__[0]
            ):
                handler = RegisterList()
            elif isinstance(attribute.type, EnumMeta) and _check_iterable(
                attribute.type
            ):
                handler = RegisterEnum()
            elif _is_spock_instance(attribute.type):
                handler = RegisterSpockCls()
            elif _is_spock_tune_instance(attribute.type):
                handler = RegisterTuneCls()
            else:
                handler = RegisterSimpleField()

            handler(attr_space, builder_space)
            special_keys.update(handler.special_keys)

        spock_instance = spock_cls(**fields)

        return spock_instance, special_keys
