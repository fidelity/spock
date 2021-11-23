# -*- coding: utf-8 -*-
import sys

import pytest

from spock.builder import ConfigArgBuilder
from spock.config import spock
from tests.base.attr_configs_test import *
from tests.base.base_asserts_test import *


# YAML Tests
class TestAllTypesYAML(AllTypes):
    """Check all required types work as expected"""

    @staticmethod
    @pytest.fixture
    def arg_builder(monkeypatch):
        with monkeypatch.context() as m:
            m.setattr(sys, "argv", ["", "--config", "./tests/conf/yaml/test.yaml"])
            config = ConfigArgBuilder(
                TypeConfig,
                NestedStuff,
                NestedListStuff,
                TypeOptConfig,
                SingleNestedConfig,
                FirstDoubleNestedConfig,
                SecondDoubleNestedConfig,
                desc="Test Builder",
            )
            return config.generate()


class TestAllDefaultsYAML(AllDefaults):
    """Check all required types falling back to default work as expected"""

    @staticmethod
    @pytest.fixture
    def arg_builder(monkeypatch):
        with monkeypatch.context() as m:
            m.setattr(sys, "argv", ["", "--config", "./tests/conf/yaml/test.yaml"])
            config = ConfigArgBuilder(
                TypeConfig,
                NestedStuff,
                NestedListStuff,
                NestedStuffDefault,
                TypeDefaultConfig,
                TypeDefaultOptConfig,
                SingleNestedConfig,
                FirstDoubleNestedConfig,
                SecondDoubleNestedConfig,
                desc="Test Builder",
            )
            return config.generate()


class TestInheritance(AllInherited):
    """Check that inheritance between classes works correctly"""

    @staticmethod
    @pytest.fixture
    def arg_builder(monkeypatch):
        with monkeypatch.context() as m:
            m.setattr(sys, "argv", ["", "--config", "./tests/conf/yaml/inherited.yaml"])
            config = ConfigArgBuilder(
                TypeInherited, NestedStuff, NestedListStuff, SingleNestedConfig,
                FirstDoubleNestedConfig, SecondDoubleNestedConfig, desc="Test Builder"
            )
            return config.generate()


# TOML TESTS
class TestAllTypesTOML(AllTypes):
    """Check all required types work as expected"""

    @staticmethod
    @pytest.fixture
    def arg_builder(monkeypatch):
        with monkeypatch.context() as m:
            m.setattr(sys, "argv", ["", "--config", "./tests/conf/toml/test.toml"])
            config = ConfigArgBuilder(
                TypeConfig,
                NestedStuff,
                NestedListStuff,
                TypeOptConfig,
                SingleNestedConfig,
                FirstDoubleNestedConfig,
                SecondDoubleNestedConfig,
                desc="Test Builder",
            )
            return config.generate()


class TestAllDefaultsTOML(AllDefaults):
    """Check all required types falling back to default work as expected"""

    @staticmethod
    @pytest.fixture
    def arg_builder(monkeypatch):
        with monkeypatch.context() as m:
            m.setattr(sys, "argv", ["", "--config", "./tests/conf/toml/test.toml"])
            config = ConfigArgBuilder(
                TypeConfig,
                NestedStuff,
                NestedListStuff,
                NestedStuffDefault,
                TypeOptConfig,
                TypeDefaultConfig,
                TypeDefaultOptConfig,
                SingleNestedConfig,
                FirstDoubleNestedConfig,
                SecondDoubleNestedConfig,
                desc="Test Builder",
            )
            return config.generate()


# JSON TESTS
class TestAllTypesJSON(AllTypes):
    """Check all required types work as expected"""

    @staticmethod
    @pytest.fixture
    def arg_builder(monkeypatch):
        with monkeypatch.context() as m:
            m.setattr(sys, "argv", ["", "--config", "./tests/conf/json/test.json"])
            config = ConfigArgBuilder(
                TypeConfig,
                NestedStuff,
                NestedListStuff,
                TypeOptConfig,
                SingleNestedConfig,
                FirstDoubleNestedConfig,
                SecondDoubleNestedConfig,
                desc="Test Builder",
            )
            return config.generate()


class TestAllDefaultsJSON(AllDefaults):
    """Check all required types falling back to default work as expected"""

    @staticmethod
    @pytest.fixture
    def arg_builder(monkeypatch):
        with monkeypatch.context() as m:
            m.setattr(sys, "argv", ["", "--config", "./tests/conf/json/test.json"])
            config = ConfigArgBuilder(
                TypeConfig,
                NestedStuff,
                NestedListStuff,
                NestedStuffDefault,
                TypeOptConfig,
                TypeDefaultConfig,
                TypeDefaultOptConfig,
                SingleNestedConfig,
                FirstDoubleNestedConfig,
                SecondDoubleNestedConfig,
                desc="Test Builder",
            )
            return config.generate()


class TestComposition:
    """Check all composed files work as expected"""

    @staticmethod
    @pytest.fixture
    def arg_builder(monkeypatch):
        with monkeypatch.context() as m:
            m.setattr(
                sys, "argv", ["", "--config", "./tests/conf/yaml/test_include.yaml"]
            )
            config = ConfigArgBuilder(
                TypeConfig,
                NestedStuff,
                NestedListStuff,
                TypeOptConfig,
                SingleNestedConfig,
                FirstDoubleNestedConfig,
                SecondDoubleNestedConfig,
                desc="Test Builder",
            )
            return config.generate()

    def test_req_int(self, arg_builder):
        assert arg_builder.TypeConfig.int_p == 9


class TestConfigCycles:
    """Checks the raise for cyclical dependencies"""

    def test_config_cycles(self, monkeypatch):
        with monkeypatch.context() as m:
            m.setattr(
                sys, "argv", ["", "--config", "./tests/conf/yaml/test_cycle.yaml"]
            )
            with pytest.raises(ValueError):
                ConfigArgBuilder(
                    TypeConfig, NestedStuff, NestedListStuff, SingleNestedConfig,
                    FirstDoubleNestedConfig, SecondDoubleNestedConfig, desc="Test Builder"
                )


class TestConfigIncludeRaise:
    """Checks the raise for include fail"""

    def test_config_cycles(self, monkeypatch):
        with monkeypatch.context() as m:
            m.setattr(
                sys,
                "argv",
                ["", "--config", "./tests/conf/yaml/test_include_fail.yaml"],
            )
            with pytest.raises(FileNotFoundError):
                ConfigArgBuilder(
                    TypeConfig, NestedStuff, NestedListStuff, SingleNestedConfig,
                    FirstDoubleNestedConfig, SecondDoubleNestedConfig, desc="Test Builder"
                )


class TestConfigDuplicate:
    """Checks the raise for duplicate reads"""

    def test_config_duplicate(self, monkeypatch):
        with monkeypatch.context() as m:
            m.setattr(
                sys,
                "argv",
                [
                    "",
                    "--config",
                    "./tests/conf/yaml/test_duplicate.yaml",
                    "./tests/conf/yaml/test.yaml",
                ],
            )
            with pytest.raises(ValueError):
                ConfigArgBuilder(
                    TypeConfig, NestedStuff, NestedListStuff, SingleNestedConfig,
                    FirstDoubleNestedConfig, SecondDoubleNestedConfig, desc="Test Builder"
                )


@spock
class AnotherNested:
    something: int = 5


@spock
class TrainProcess:
    epochs: int = 100
    nest: AnotherNested = AnotherNested


@spock
class Train:
    train_process: TrainProcess = TrainProcess


class TestNestedDefaultFromConfig:
    @staticmethod
    @pytest.fixture
    def arg_builder(monkeypatch):
        with monkeypatch.context() as m:
            m.setattr(sys, "argv", ["", "--config", "./tests/conf/yaml/test_nested.yaml"])
            config = ConfigArgBuilder(
                Train, TrainProcess, AnotherNested, desc="Test Builder"
            )
            return config.generate()

    def test_default_nesting(self, arg_builder):
        assert arg_builder.Train.train_process.nest.something == 1
        assert arg_builder.Train.train_process.epochs == 5


class MyEnum(Enum):
    value_1 = "value_1"
    value_2 = "value_2"


@spock
class AnotherNestedConfig:
    something: int = 5


@spock
class NestedConfig:
    integer: int = 1
    my_enum: MyEnum = "value_1"
    other_nest: AnotherNestedConfig = AnotherNestedConfig


@spock
class DuplicatedConfig:
    flag_3: bool = False


@spock
class MakeDatasetConfig:
    flag1: bool = False
    flag_2: bool = False
    nested_config: NestedConfig = NestedConfig
    duplicated_config: DuplicatedConfig = DuplicatedConfig


@spock
class BuildFeatureConfig:
    duplicated_config: DuplicatedConfig = DuplicatedConfig


class TestTripleNestedDefaultFromConfig:
    @staticmethod
    @pytest.fixture
    def arg_builder(monkeypatch):
        with monkeypatch.context() as m:
            m.setattr(
                sys,
                "argv",
                ["", "--config", "./tests/conf/yaml/test_double_nested.yaml"],
            )
            config = ConfigArgBuilder(
                BuildFeatureConfig,
                MakeDatasetConfig,
                DuplicatedConfig,
                NestedConfig,
                AnotherNestedConfig,
                desc="",
            )
            return config.generate()

    def test_default_nesting(self, arg_builder):
        assert arg_builder.MakeDatasetConfig.nested_config.other_nest.something == 1