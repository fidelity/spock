# -*- coding: utf-8 -*-
from tests.base.base_asserts_test import *
import pytest
from spock.builder import ConfigArgBuilder
from tests.base.attr_configs_test import *
import sys


class TestNoCmdLineKwarg(AllTypes):
    """Testing to see that the kwarg no cmd line works"""
    @staticmethod
    @pytest.fixture
    def arg_builder(monkeypatch):
        with monkeypatch.context() as m:
            config = ConfigArgBuilder(TypeConfig, NestedStuff, NestedListStuff, TypeOptConfig, no_cmd_line=True,
                                      configs=['./tests/conf/yaml/test.yaml'])
            return config.generate()


class TestNoCmdLineKwargRaise:
    """Testing to see that the kwarg no cmd line works"""
    def test_cmd_line_kwarg_raise(self, monkeypatch):
        with monkeypatch.context() as m:
            with pytest.raises(ValueError):
                config = ConfigArgBuilder(TypeConfig, NestedStuff, NestedListStuff, TypeOptConfig, no_cmd_line=True,
                                          configs='./tests/conf/yaml/test.yaml')
                return config.generate()


class TestNoCmdLineRaise:
    """Check raise when no cmd line and no configs works as expected """
    def test_choice_raise(self, monkeypatch):
        with monkeypatch.context() as m:
            with pytest.raises(ValueError):
                ConfigArgBuilder(TypeConfig, NestedStuff, NestedListStuff, TypeOptConfig, no_cmd_line=True)


class TestConfigKwarg(AllTypes):
    """Testing to see that the kwarg overload path works"""
    @staticmethod
    @pytest.fixture
    def arg_builder(monkeypatch):
        with monkeypatch.context() as m:
            m.setattr(sys, 'argv', [''])
            config = ConfigArgBuilder(TypeConfig, NestedStuff, NestedListStuff, TypeOptConfig, desc='Test Builder',
                                      configs=['./tests/conf/yaml/test.yaml'])
            return config.generate()


class TestConfigArgType:
    """Test functions related to the argument builder"""
    def test_type_arg_builder(self, monkeypatch):
        with monkeypatch.context() as m:
            m.setattr(sys, 'argv', ['', '--config',
                                    './tests/conf/yaml/test.yaml'])
            with pytest.raises(TypeError):
                ConfigArgBuilder(['Names'], desc='Test Builder')


class TestNonAttrs:
    def test_non_attrs_fail(self, monkeypatch):
        with monkeypatch.context() as m:
            with pytest.raises(TypeError):
                class AttrFail:
                    failed_attr: int
                config = ConfigArgBuilder(TypeConfig, NestedStuff, NestedListStuff, TypeOptConfig, AttrFail,
                                          configs=['./tests/conf/yaml/test.yaml'])
                return config.generate()


class TestRaiseWrongInputType:
    """Check all required types work as expected """
    def test_wrong_input_raise(self, monkeypatch):
        with monkeypatch.context() as m:
            m.setattr(sys, 'argv', ['', '--config',
                                    './tests/conf/yaml/test.foo'])
            with pytest.raises(ValueError):
                config = ConfigArgBuilder(TypeConfig, NestedStuff, NestedListStuff, TypeOptConfig, desc='Test Builder')
                return config.generate()


class TestUnknownArg:
    def test_type_unknown(self, monkeypatch):
        with monkeypatch.context() as m:
            m.setattr(sys, 'argv', ['', '--config',
                                    './tests/conf/yaml/test_incorrect.yaml'])
            with pytest.raises(ValueError):
                ConfigArgBuilder(TypeConfig, NestedStuff, NestedListStuff, desc='Test Builder')


class TestUnknownClassParameterArg:
    def test_class_parameter_unknown(self, monkeypatch):
        with monkeypatch.context() as m:
            m.setattr(sys, 'argv', ['', '--config',
                                    './tests/conf/yaml/test_class_incorrect.yaml'])
            with pytest.raises(ValueError):
                ConfigArgBuilder(TypeConfig, NestedStuff, NestedListStuff, desc='Test Builder')


class TestUnknownClassArg:
    def test_class_unknown(self, monkeypatch):
        with monkeypatch.context() as m:
            m.setattr(sys, 'argv', ['', '--config',
                                    './tests/conf/yaml/test_missing_class.yaml'])
            with pytest.raises(ValueError):
                ConfigArgBuilder(TypeConfig, NestedStuff, NestedListStuff, desc='Test Builder')


class TestWrongRepeatedClass:
    def test_class_unknown(self, monkeypatch):
        with monkeypatch.context() as m:
            m.setattr(sys, 'argv', ['', '--config',
                                    './tests/conf/yaml/test_incorrect_repeated_class.yaml'])
            with pytest.raises(ValueError):
                ConfigArgBuilder(TypeConfig, NestedStuff, NestedListStuff, desc='Test Builder')
