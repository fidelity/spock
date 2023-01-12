# -*- coding: utf-8 -*-
import sys

import pytest
from attr.exceptions import FrozenInstanceError

from spock.builder import ConfigArgBuilder
from spock.exceptions import _SpockValueError
from tests.base.attr_configs_test import *


class TestHelp:
    def test_help(self, monkeypatch):
        with monkeypatch.context() as m:
            m.setattr(
                sys, "argv", ["", "--config", "./tests/conf/yaml/test.yaml", "--help"]
            )
            with pytest.raises(SystemExit):
                config = ConfigArgBuilder(
                    *all_configs,
                    desc="Test Builder",
                )
                return config.generate()


class TestSpockspaceRepr:
    def test_repr(self, monkeypatch, capsys):
        with monkeypatch.context() as m:
            m.setattr(sys, "argv", ["", "--config", "./tests/conf/yaml/test.yaml"])
            config = ConfigArgBuilder(
                *all_configs,
                desc="Test Builder",
            )
            print(config.generate())
            out, _ = capsys.readouterr()
            assert ("NestedListStuff" in out) and "TypeConfig" in out


class TestToDict:
    def test_2_dict(self, monkeypatch):
        with monkeypatch.context() as m:
            m.setattr(sys, "argv", ["", "--config", "./tests/conf/yaml/test.yaml"])
            config = ConfigArgBuilder(
                *all_configs,
                desc="Test Builder",
            )
            configs = config.generate()
            config_dict = config.spockspace_2_dict(configs)
            assert isinstance(config_dict, dict) is True


class TestClassToDict:
    def test_class_2_dict(self, monkeypatch):
        with monkeypatch.context() as m:
            m.setattr(sys, "argv", ["", "--config", "./tests/conf/yaml/test.yaml"])
            config = ConfigArgBuilder(
                *all_configs,
                desc="Test Builder",
            )
            configs = config.generate()
            config_dict = config.obj_2_dict(configs.TypeConfig)
            assert isinstance(config_dict, dict) is True
            assert isinstance(config_dict["TypeConfig"], dict) is True
            configs_dicts = config.obj_2_dict((configs.TypeConfig, configs.NestedStuff))
            assert isinstance(configs_dicts["TypeConfig"], dict) is True
            assert isinstance(configs_dicts["NestedStuff"], dict) is True

    def test_raise_incorrect_type(self, monkeypatch):
        with monkeypatch.context() as m:
            m.setattr(sys, "argv", ["", "--config", "./tests/conf/yaml/test.yaml"])
            config = ConfigArgBuilder(
                *all_configs,
                desc="Test Builder",
            )
            configs = config.generate()
            with pytest.raises(_SpockValueError):
                config_dict = config.obj_2_dict("foo")
            with pytest.raises(_SpockValueError):
                config_dict = config.obj_2_dict(("foo", 10))


class TestFrozen:
    """Testing the frozen state of the spock config object"""

    @staticmethod
    @pytest.fixture
    def arg_builder(monkeypatch):
        with monkeypatch.context() as m:
            m.setattr(sys, "argv", ["", "--config", "./tests/conf/yaml/test.yaml"])
            config = ConfigArgBuilder(
                *all_configs,
                desc="Test Builder",
            )
            return config.generate()

    # Check frozen state works
    def test_frozen_state(self, arg_builder):
        with pytest.raises(FrozenInstanceError):
            arg_builder.TypeConfig.float_p = 1.0
        with pytest.raises(FrozenInstanceError):
            arg_builder.TypeOptConfig.int_p_opt_def = 1
        with pytest.raises(FrozenInstanceError):
            arg_builder.TypeConfig.list_p_float = [1.0, 2.0]
        with pytest.raises(FrozenInstanceError):
            arg_builder.TypeOptConfig.tuple_p_opt_no_def_float = (1.0, 2.0)
