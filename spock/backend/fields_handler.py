from abc import ABC, abstractmethod

from attr import NOTHING

from spock.backend.spaces import AttributeSpace, ConfigSpace, BuilderSpace
from spock.args import SpockArguments
from enum import EnumMeta
from spock.utils import _is_spock_instance, _check_iterable


class SpockNotOptionalError(Exception):
    pass


class RegisterFieldTemplate(ABC):
    def __init__(self):
        self.special_keys = {}

    def __call__(self, attr_space: AttributeSpace, builder_state: BuilderSpace):
        if self._is_attribute_in_config_arguments(attr_space, builder_state.arguments):
            self.handle_attribute_from_config(attr_space, builder_state)
        elif self._is_attribute_optional(attr_space.attribute):
            self.handle_optional_attribute(attr_space, builder_state)
        else:
            self.other(attr_space, builder_state)

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

    def other(self, attr_space: AttributeSpace, builder_state: BuilderSpace):
        raise SpockNotOptionalError(
            f"Attribute `{attr_space.attribute.name}` is not provided in "
            f"config arguments and is not optional."
        )

    def handle_optional_attribute(
        self, attr_space: AttributeSpace, builder_state: BuilderSpace
    ):
        attr_space.field = attr_space.attribute.default

    @abstractmethod
    def handle_attribute_from_config(
        self, attr_space: AttributeSpace, builder_state: BuilderSpace
    ):
        pass


class RegisterList(RegisterFieldTemplate):
    def handle_attribute_from_config(
        self, attr_space: AttributeSpace, builder_state: BuilderSpace
    ):
        list_item_spock_class = attr_space.attribute.metadata["type"].__args__[0]

        attr_space.field = self._process_list(list_item_spock_class, builder_state)

        builder_state.spock_space[list_item_spock_class.__name__] = attr_space.field

    @staticmethod
    def _process_list(spock_cls, builder_state: BuilderSpace):
        return [
            spock_cls(**fields)
            for fields in builder_state.arguments[spock_cls.__name__]
        ]


class RegisterEnum(RegisterFieldTemplate):
    def handle_attribute_from_config(
        self, attr_space: AttributeSpace, builder_state: BuilderSpace
    ):

        possible_enum_classes = {
            c.value.__name__: c.value for c in attr_space.attribute.type
        }

        enum_cls_name = builder_state.arguments[attr_space.config_space.name][
            attr_space.attribute.name
        ]
        enum_cls = possible_enum_classes[enum_cls_name]

        attr_space.field = enum_cls(**builder_state.arguments[enum_cls_name])
        builder_state.spock_space[enum_cls_name] = attr_space.field


class RegisterSimpleField(RegisterFieldTemplate):
    def handle_attribute_from_config(
        self, attr_space: AttributeSpace, builder_state: BuilderSpace
    ):
        attr_space.field = builder_state.arguments[attr_space.config_space.name][
            attr_space.attribute.name
        ]

        self.register_special_key(attr_space)

    def handle_optional_attribute(
        self, attr_space: AttributeSpace, builder_state: BuilderSpace
    ):
        super().handle_optional_attribute(attr_space, builder_state)
        self.register_special_key(attr_space)

    def register_special_key(self, attr_space: AttributeSpace):
        if (
            "special_key" in attr_space.attribute.metadata
            and attr_space.attribute.metadata["special_key"] is not None
        ):
            if attr_space.field is not None:
                self.special_keys["save_path"] = attr_space.field


class RegisterSpockCls(RegisterFieldTemplate):
    @staticmethod
    def _attr_type(attr_space: AttributeSpace):
        return attr_space.attribute.type

    def handle_attribute_from_config(
        self, attr_space: AttributeSpace, builder_state: BuilderSpace
    ):
        attr_type = self._attr_type(attr_space)
        attr_space.field, special_keys = self.recurse_generate(attr_type, builder_state)
        builder_state.spock_space[attr_type.__name__] = attr_space.field
        self.special_keys.update(special_keys)

    def handle_optional_attribute(
        self, attr_space: AttributeSpace, builder_state: BuilderSpace
    ):
        super().handle_optional_attribute(attr_space, builder_state)
        builder_state.spock_space[
            self._attr_type(attr_space).__name__
        ] = attr_space.field

    @classmethod
    def recurse_generate(cls, spock_cls, builder_state: BuilderSpace):
        children = set(e[1] for e in builder_state.graph.out_edges(spock_cls))
        special_keys, fields = {}, {}
        config_space = ConfigSpace(spock_cls, fields)

        for val in spock_cls.__attrs_attrs__:
            attr_space = AttributeSpace(val, config_space)

            if val.type is list and _is_spock_instance(
                val.metadata["type"].__args__[0]
            ):
                handler = RegisterList()
            elif isinstance(val.type, EnumMeta) and _check_iterable(val.type):
                handler = RegisterEnum()
            elif val.type in children:
                handler = RegisterSpockCls()
            else:
                handler = RegisterSimpleField()

            handler(attr_space, builder_state)
            special_keys.update(handler.special_keys)

        spock_instance = spock_cls(**fields)

        return spock_instance, special_keys
