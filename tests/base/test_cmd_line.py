# -*- coding: utf-8 -*-
import sys

import pytest

from spock.builder import ConfigArgBuilder
from tests.base.attr_configs_test import *


class TestClassCmdLineOverride:
    """Testing command line overrides"""

    @staticmethod
    @pytest.fixture
    def arg_builder(monkeypatch):
        with monkeypatch.context() as m:
            m.setattr(
                sys,
                "argv",
                [
                    "",
                    "--config",
                    "./tests/conf/yaml/test_class.yaml",
                    "--TypeConfig.bool_p",
                    "--TypeConfig.int_p",
                    "11",
                    "--TypeConfig.float_p",
                    "11.0",
                    "--TypeConfig.string_p",
                    "Hooray",
                    "--TypeConfig.list_p_float",
                    "[11.0,21.0]",
                    "--TypeConfig.list_p_int",
                    "[11, 21]",
                    "--TypeConfig.list_p_str",
                    "['Hooray', 'Working']",
                    "--TypeConfig.list_p_bool",
                    "[False, True]",
                    "--TypeConfig.tuple_p_float",
                    "(11.0, 21.0)",
                    "--TypeConfig.tuple_p_int",
                    "(11, 21)",
                    "--TypeConfig.tuple_p_str",
                    "('Hooray', 'Working')",
                    "--TypeConfig.tuple_p_bool",
                    "(False, True)",
                    "--TypeConfig.tuple_p_mixed",
                    "(5, 11.5)",
                    "--TypeConfig.list_list_p_int",
                    "[[11, 21], [11, 21]]",
                    "--TypeConfig.choice_p_str",
                    "option_2",
                    "--TypeConfig.choice_p_int",
                    "20",
                    "--TypeConfig.choice_p_float",
                    "20.0",
                    "--TypeConfig.list_choice_p_str",
                    "['option_2']",
                    "--TypeConfig.list_list_choice_p_str",
                    "[['option_2'], ['option_2']]",
                    "--TypeConfig.list_choice_p_int",
                    "[20]",
                    "--TypeConfig.list_choice_p_float",
                    "[20.0]",
                    "--TypeConfig.class_enum",
                    "NestedStuff",
                    "--NestedStuff.one",
                    "12",
                    "--NestedStuff.two",
                    "ancora",
                    "--TypeConfig.nested_list.NestedListStuff.one",
                    "[11, 21]",
                    "--TypeConfig.nested_list.NestedListStuff.two",
                    "['Hooray', 'Working']",
                    "--TypeConfig.high_config",
                    "SingleNestedConfig",
                    "--SingleNestedConfig.double_nested_config",
                    "SecondDoubleNestedConfig",
                    "--SecondDoubleNestedConfig.morph_tolerance",
                    "0.2",
                    "--TypeConfig.call_me",
                    "'tests.base.attr_configs_test.foo'"
                ],
            )
            config = ConfigArgBuilder(
                TypeConfig, NestedStuff, NestedListStuff, SingleNestedConfig,
                FirstDoubleNestedConfig, SecondDoubleNestedConfig,desc="Test Builder"
            )
            return config.generate()

    def test_class_overrides(self, arg_builder):
        assert arg_builder.TypeConfig.bool_p is True
        assert arg_builder.TypeConfig.int_p == 11
        assert arg_builder.TypeConfig.float_p == 11.0
        assert arg_builder.TypeConfig.string_p == "Hooray"
        assert arg_builder.TypeConfig.list_p_float == [11.0, 21.0]
        assert arg_builder.TypeConfig.list_p_int == [11, 21]
        assert arg_builder.TypeConfig.list_p_str == ["Hooray", "Working"]
        assert arg_builder.TypeConfig.list_p_bool == [False, True]
        assert arg_builder.TypeConfig.tuple_p_float == (11.0, 21.0)
        assert arg_builder.TypeConfig.tuple_p_int == (11, 21)
        assert arg_builder.TypeConfig.tuple_p_str == ("Hooray", "Working")
        assert arg_builder.TypeConfig.tuple_p_bool == (False, True)
        assert arg_builder.TypeConfig.tuple_p_mixed == (5, 11.5)
        assert arg_builder.TypeConfig.choice_p_str == "option_2"
        assert arg_builder.TypeConfig.choice_p_int == 20
        assert arg_builder.TypeConfig.choice_p_float == 20.0
        assert arg_builder.TypeConfig.list_list_p_int == [[11, 21], [11, 21]]
        assert arg_builder.TypeConfig.list_choice_p_str == ["option_2"]
        assert arg_builder.TypeConfig.list_list_choice_p_str == [
            ["option_2"],
            ["option_2"],
        ]
        assert arg_builder.TypeConfig.list_choice_p_int == [20]
        assert arg_builder.TypeConfig.list_choice_p_float == [20.0]
        assert arg_builder.TypeConfig.class_enum.one == 12
        assert arg_builder.TypeConfig.class_enum.two == "ancora"
        assert arg_builder.NestedListStuff[0].one == 11
        assert arg_builder.NestedListStuff[0].two == "Hooray"
        assert arg_builder.NestedListStuff[1].one == 21
        assert arg_builder.NestedListStuff[1].two == "Working"
        assert isinstance(arg_builder.SingleNestedConfig.double_nested_config, SecondDoubleNestedConfig) is True
        assert arg_builder.SecondDoubleNestedConfig.morph_tolerance == 0.2
        assert arg_builder.TypeConfig.call_me == foo


class TestClassOnlyCmdLine:
    """Testing command line overrides"""

    @staticmethod
    @pytest.fixture
    def arg_builder(monkeypatch):
        with monkeypatch.context() as m:
            m.setattr(
                sys,
                "argv",
                [
                    "",
                    "--TypeConfig.bool_p",
                    "--TypeConfig.int_p",
                    "11",
                    "--TypeConfig.float_p",
                    "11.0",
                    "--TypeConfig.string_p",
                    "Hooray",
                    "--TypeConfig.list_p_float",
                    "[11.0, 21.0]",
                    "--TypeConfig.list_p_int",
                    "[11, 21]",
                    "--TypeConfig.list_p_str",
                    "['Hooray', 'Working']",
                    "--TypeConfig.list_p_bool",
                    "[False, True]",
                    "--TypeConfig.tuple_p_float",
                    "(11.0, 21.0)",
                    "--TypeConfig.tuple_p_int",
                    "(11, 21)",
                    "--TypeConfig.tuple_p_str",
                    "('Hooray', 'Working')",
                    "--TypeConfig.tuple_p_bool",
                    "(False, True)",
                    "--TypeConfig.tuple_p_mixed",
                    "(5, 11.5)",
                    "--TypeConfig.list_list_p_int",
                    "[[11, 21], [11, 21]]",
                    "--TypeConfig.choice_p_str",
                    "option_2",
                    "--TypeConfig.choice_p_int",
                    "20",
                    "--TypeConfig.choice_p_float",
                    "20.0",
                    "--TypeConfig.list_choice_p_str",
                    "['option_2']",
                    "--TypeConfig.list_list_choice_p_str",
                    "[['option_2'], ['option_2']]",
                    "--TypeConfig.list_choice_p_int",
                    "[20]",
                    "--TypeConfig.list_choice_p_float",
                    "[20.0]",
                    "--TypeConfig.class_enum",
                    "NestedStuff",
                    "--TypeConfig.nested",
                    "NestedStuff",
                    "--NestedStuff.one",
                    "12",
                    "--NestedStuff.two",
                    "ancora",
                    "--TypeConfig.nested_list.NestedListStuff.one",
                    "[11, 21]",
                    "--TypeConfig.nested_list.NestedListStuff.two",
                    "['Hooray', 'Working']",
                    "--TypeConfig.high_config",
                    "SingleNestedConfig",
                    "--TypeConfig.call_me",
                    "'tests.base.attr_configs_test.foo'"
                ],
            )
            config = ConfigArgBuilder(
                TypeConfig, NestedStuff, NestedListStuff, SingleNestedConfig,
                FirstDoubleNestedConfig, SecondDoubleNestedConfig, desc="Test Builder"
            )
            return config.generate()

    def test_class_overrides(self, arg_builder):
        assert arg_builder.TypeConfig.bool_p is True
        assert arg_builder.TypeConfig.int_p == 11
        assert arg_builder.TypeConfig.float_p == 11.0
        assert arg_builder.TypeConfig.string_p == "Hooray"
        assert arg_builder.TypeConfig.list_p_float == [11.0, 21.0]
        assert arg_builder.TypeConfig.list_p_int == [11, 21]
        assert arg_builder.TypeConfig.list_p_str == ["Hooray", "Working"]
        assert arg_builder.TypeConfig.list_p_bool == [False, True]
        assert arg_builder.TypeConfig.tuple_p_float == (11.0, 21.0)
        assert arg_builder.TypeConfig.tuple_p_int == (11, 21)
        assert arg_builder.TypeConfig.tuple_p_str == ("Hooray", "Working")
        assert arg_builder.TypeConfig.tuple_p_bool == (False, True)
        assert arg_builder.TypeConfig.tuple_p_mixed == (5, 11.5)
        assert arg_builder.TypeConfig.choice_p_str == "option_2"
        assert arg_builder.TypeConfig.choice_p_int == 20
        assert arg_builder.TypeConfig.choice_p_float == 20.0
        assert arg_builder.TypeConfig.list_list_p_int == [[11, 21], [11, 21]]
        assert arg_builder.TypeConfig.list_choice_p_str == ["option_2"]
        assert arg_builder.TypeConfig.list_list_choice_p_str == [
            ["option_2"],
            ["option_2"],
        ]
        assert arg_builder.TypeConfig.list_choice_p_int == [20]
        assert arg_builder.TypeConfig.list_choice_p_float == [20.0]
        assert arg_builder.TypeConfig.class_enum.one == 12
        assert arg_builder.TypeConfig.class_enum.two == "ancora"
        assert isinstance(arg_builder.TypeConfig.high_config.double_nested_config,
                          SecondDoubleNestedConfig) is True
        assert arg_builder.TypeConfig.high_config.double_nested_config.morph_kernels_thickness == 1
        assert arg_builder.TypeConfig.high_config.double_nested_config.morph_tolerance == 0.1
        assert arg_builder.NestedListStuff[0].one == 11
        assert arg_builder.NestedListStuff[0].two == "Hooray"
        assert arg_builder.NestedListStuff[1].one == 21
        assert arg_builder.NestedListStuff[1].two == "Working"
        assert arg_builder.TypeConfig.call_me == foo


class TestRaiseCmdLineNoKey:
    """Testing command line overrides"""

    def test_cmd_line_no_key(self, monkeypatch):
        with monkeypatch.context() as m:
            m.setattr(
                sys,
                "argv",
                [
                    "",
                    "--config",
                    "./tests/conf/yaml/test.yaml",
                    "--TypeConfig.foo_bar_stuff",
                    "11",
                ],
            )
            with pytest.raises(SystemExit):
                config = ConfigArgBuilder(
                    TypeConfig, NestedStuff, NestedListStuff, SingleNestedConfig,
                    FirstDoubleNestedConfig, SecondDoubleNestedConfig, desc="Test Builder"
                )
                return config.generate()


class TestRaiseCmdLineListLen:
    """Testing command line overrides"""

    def test_cmd_line_list_len(self, monkeypatch):
        with monkeypatch.context() as m:
            m.setattr(
                sys,
                "argv",
                [
                    "",
                    "--config",
                    "./tests/conf/yaml/test.yaml",
                    "--TypeConfig.nested_list.NestedListStuff.one",
                    "[11]",
                ],
            )
            with pytest.raises(ValueError):
                config = ConfigArgBuilder(
                    TypeConfig, NestedStuff, NestedListStuff, SingleNestedConfig,
                    FirstDoubleNestedConfig, SecondDoubleNestedConfig, desc="Test Builder"
                )
                return config.generate()
