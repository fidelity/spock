# -*- coding: utf-8 -*-
import sys

import pytest
from attr.exceptions import FrozenInstanceError

from spock.builder import ConfigArgBuilder
from tests.base.attr_configs_test import *


class TestHelp:
    def test_help(self, monkeypatch):
        with monkeypatch.context() as m:
            m.setattr(
                sys, "argv", ["", "--config", "./tests/conf/yaml/test.yaml", "--help"]
            )
            with pytest.raises(SystemExit):
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


class TestSpockspaceRepr:
    def test_repr(self, monkeypatch, capsys):
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
            print(config.generate())
            out, _ = capsys.readouterr()
            assert ("NestedListStuff" in out) and "TypeConfig" in out


class TestFrozen:
    """Testing the frozen state of the spock config object"""

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
