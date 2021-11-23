from dataclasses import dataclass

from spock.args import SpockArguments
from spock.graph import Graph


class ConfigSpace:
    def __init__(self, spock_cls, fields: dict):
        self.spock_cls = spock_cls
        self.fields = fields

    @property
    def name(self) -> str:
        return self.spock_cls.__name__


class AttributeSpace:
    def __init__(self, attribute, config_space: ConfigSpace):
        self.config_space = config_space
        self.attribute = attribute

    @property
    def field(self):
        return self.config_space.fields[self.attribute.name]

    @field.setter
    def field(self, value):
        if isinstance(self.attribute.name, str):
            self.config_space.fields[self.attribute.name] = value
        else:
            raise ValueError


@dataclass
class BuilderSpace:
    spock_space: dict
    arguments: SpockArguments
    graph: Graph