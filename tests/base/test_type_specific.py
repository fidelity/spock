# -*- coding: utf-8 -*-
import sys

import pytest

from spock.builder import ConfigArgBuilder
from spock.backend.field_handlers import SpockInstantiationError
from tests.base.attr_configs_test import *


class TestChoiceRaises:
    """Check choice raises correctly"""

    def test_choice_raise(self, monkeypatch):
        with monkeypatch.context() as m:
            m.setattr(sys, "argv", ["", "--config", "./tests/conf/yaml/choice.yaml"])
            with pytest.raises(SpockInstantiationError):
                ConfigArgBuilder(ChoiceFail, desc="Test Builder")


class TestOptionalRaises:
    """Check choice raises correctly"""
    def test_coptional_raise(self, monkeypatch):
        with monkeypatch.context() as m:
            # m.setattr(sys, "argv", ["", "--config", "./tests/conf/yaml/empty.yaml"])
            with pytest.raises(SpockInstantiationError):
                ConfigArgBuilder(OptionalFail, desc="Test Builder", configs=[], no_cmd_line=True)


class TestTupleRaises:
    """Check that Tuple lengths are being enforced correctly"""

    def test_tuple_raise(self, monkeypatch):
        with monkeypatch.context() as m:
            m.setattr(sys, "argv", ["", "--config", "./tests/conf/yaml/tuple.yaml"])
            with pytest.raises(ValueError):
                ConfigArgBuilder(
                    TypeConfig,
                    NestedStuff,
                    NestedListStuff,
                    TypeOptConfig,
                    SingleNestedConfig,
                    FirstDoubleNestedConfig,
                    SecondDoubleNestedConfig,
                    desc="Test Builder")


class TestOverrideRaise:
    """Checks that override of a specific class variable is failing gracefully"""

    def test_override_raise(self, monkeypatch):
        with monkeypatch.context() as m:
            m.setattr(sys, "argv", ["", "--config", "./tests/conf/yaml/test.yaml"])
            with pytest.raises(TypeError):
                ConfigArgBuilder(
                    TypeInherited,
                    NestedStuff,
                    NestedListStuff,
                    TypeOptConfig,
                    SingleNestedConfig,
                    FirstDoubleNestedConfig,
                    SecondDoubleNestedConfig,
                    desc="Test Builder"
                )


class TestEnumMixedFail:
    def test_enum_mixed_fail(self, monkeypatch):
        with monkeypatch.context() as m:
            with pytest.raises(TypeError):

                @spock
                class EnumFail:
                    choice_mixed: FailedEnum


class TestIncorrectType:
    def test_incorrect_type(self, monkeypatch):
        with monkeypatch.context() as m:
            with pytest.raises(TypeError):

                @spock
                class TypeFail:
                    weird_type: lambda x: x


class TestEnumClassMissing:
    def test_enum_class_missing(self, monkeypatch):
        with monkeypatch.context() as m:
            m.setattr(
                sys,
                "argv",
                ["", "--config", "./tests/conf/yaml/test_wrong_class_enum.yaml"],
            )
            with pytest.raises(KeyError):
                ConfigArgBuilder(
                    TypeConfig,
                    NestedStuff,
                    NestedListStuff,
                    TypeOptConfig,
                    SingleNestedConfig,
                    FirstDoubleNestedConfig,
                    SecondDoubleNestedConfig,
                    desc="Test Builder"
                )


@spock
class RepeatedDefsFailConfig:
    # Nested list configuration
    nested_list_def: List[NestedListStuff] = [NestedListStuff]


class TestMissingRepeatedDefs:
    def test_repeated_defs_fail(self, monkeypatch):
        with monkeypatch.context() as m:
            m.setattr(
                sys,
                "argv",
                [""],
            )
            with pytest.raises(SpockInstantiationError):
                config = ConfigArgBuilder(RepeatedDefsFailConfig, NestedListStuff, desc="Test Builder")
                config.generate()
