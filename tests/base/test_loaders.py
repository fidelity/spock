# -*- coding: utf-8 -*-
from tests.base.base_asserts_test import *
import pytest
from spock.builder import ConfigArgBuilder
from tests.base.attr_configs_test import *
import sys


# YAML Tests
class TestAllTypesYAML(AllTypes):
    """Check all required types work as expected """
    @staticmethod
    @pytest.fixture
    def arg_builder(monkeypatch):
        with monkeypatch.context() as m:
            m.setattr(sys, 'argv', ['', '--config',
                                    './tests/conf/yaml/test.yaml'])
            config = ConfigArgBuilder(TypeConfig, NestedStuff, NestedListStuff, TypeOptConfig, desc='Test Builder')
            return config.generate()


class TestAllDefaultsYAML(AllDefaults):
    """Check all required types falling back to default work as expected """
    @staticmethod
    @pytest.fixture
    def arg_builder(monkeypatch):
        with monkeypatch.context() as m:
            m.setattr(sys, 'argv', ['', '--config',
                                    './tests/conf/yaml/test.yaml'])
            config = ConfigArgBuilder(TypeConfig, NestedStuff, NestedListStuff, NestedStuffDefault, TypeOptConfig,
                                      TypeDefaultConfig, TypeDefaultOptConfig,
                                      desc='Test Builder')
            return config.generate()


class TestInheritance(AllInherited):
    """Check that inheritance between classes works correctly"""
    @staticmethod
    @pytest.fixture
    def arg_builder(monkeypatch):
        with monkeypatch.context() as m:
            m.setattr(sys, 'argv', ['', '--config',
                                    './tests/conf/yaml/inherited.yaml'])
            config = ConfigArgBuilder(TypeInherited, NestedStuff, NestedListStuff, desc='Test Builder')
            return config.generate()


# TOML TESTS
class TestAllTypesTOML(AllTypes):
    """Check all required types work as expected """
    @staticmethod
    @pytest.fixture
    def arg_builder(monkeypatch):
        with monkeypatch.context() as m:
            m.setattr(sys, 'argv', ['', '--config',
                                    './tests/conf/toml/test.toml'])
            config = ConfigArgBuilder(TypeConfig, NestedStuff, NestedListStuff, TypeOptConfig, desc='Test Builder')
            return config.generate()


class TestAllDefaultsTOML(AllDefaults):
    """Check all required types falling back to default work as expected """
    @staticmethod
    @pytest.fixture
    def arg_builder(monkeypatch):
        with monkeypatch.context() as m:
            m.setattr(sys, 'argv', ['', '--config',
                                    './tests/conf/toml/test.toml'])
            config = ConfigArgBuilder(TypeConfig, NestedStuff, NestedListStuff, NestedStuffDefault, TypeOptConfig,
                                      TypeDefaultConfig, TypeDefaultOptConfig,
                                      desc='Test Builder')
            return config.generate()


# JSON TESTS
class TestAllTypesJSON(AllTypes):
    """Check all required types work as expected """
    @staticmethod
    @pytest.fixture
    def arg_builder(monkeypatch):
        with monkeypatch.context() as m:
            m.setattr(sys, 'argv', ['', '--config',
                                    './tests/conf/json/test.json'])
            config = ConfigArgBuilder(TypeConfig, NestedStuff, NestedListStuff, TypeOptConfig, desc='Test Builder')
            return config.generate()


class TestAllDefaultsJSON(AllDefaults):
    """Check all required types falling back to default work as expected """
    @staticmethod
    @pytest.fixture
    def arg_builder(monkeypatch):
        with monkeypatch.context() as m:
            m.setattr(sys, 'argv', ['', '--config',
                                    './tests/conf/json/test.json'])
            config = ConfigArgBuilder(TypeConfig, NestedStuff, NestedListStuff, NestedStuffDefault, TypeOptConfig,
                                      TypeDefaultConfig, TypeDefaultOptConfig,
                                      desc='Test Builder')
            return config.generate()


class TestComposition:
    """Check all composed files work as expected """
    @staticmethod
    @pytest.fixture
    def arg_builder(monkeypatch):
        with monkeypatch.context() as m:
            m.setattr(sys, 'argv', ['', '--config',
                                    './tests/conf/yaml/test_include.yaml'])
            config = ConfigArgBuilder(TypeConfig, NestedStuff, NestedListStuff, TypeOptConfig, desc='Test Builder')
            return config.generate()

    def test_req_int(self, arg_builder):
        assert arg_builder.TypeConfig.int_p == 9


class TestConfigCycles:
    """Checks the raise for cyclical dependencies"""
    def test_config_cycles(self, monkeypatch):
        with monkeypatch.context() as m:
            m.setattr(sys, 'argv', ['', '--config',
                                    './tests/conf/yaml/test_cycle.yaml'])
            with pytest.raises(ValueError):
                ConfigArgBuilder(TypeConfig, NestedStuff, NestedListStuff, desc='Test Builder')


class TestConfigIncludeRaise:
    """Checks the raise for include fail"""
    def test_config_cycles(self, monkeypatch):
        with monkeypatch.context() as m:
            m.setattr(sys, 'argv', ['', '--config',
                                    './tests/conf/yaml/test_include_fail.yaml'])
            with pytest.raises(ValueError):
                ConfigArgBuilder(TypeConfig, NestedStuff, NestedListStuff, desc='Test Builder')


class TestConfigDuplicate:
    """Checks the raise for duplicate reads"""
    def test_config_duplicate(self, monkeypatch):
        with monkeypatch.context() as m:
            m.setattr(sys, 'argv', ['', '--config',
                                    './tests/conf/yaml/test_duplicate.yaml', './tests/conf/yaml/test.yaml'])
            with pytest.raises(ValueError):
                ConfigArgBuilder(TypeConfig, NestedStuff, NestedListStuff, desc='Test Builder')


