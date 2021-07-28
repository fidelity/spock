# -*- coding: utf-8 -*-
import pytest
from spock.builder import ConfigArgBuilder
from tests.base.attr_configs_test import *
import sys


class TestChoiceRaises:
    """Check choice raises correctly"""
    def test_choice_raise(self, monkeypatch):
        with monkeypatch.context() as m:
            m.setattr(sys, 'argv', ['', '--config',
                                    './tests/conf/yaml/choice.yaml'])
            with pytest.raises(ValueError):
                ConfigArgBuilder(ChoiceFail, desc='Test Builder')


class TestTupleRaises:
    """Check that Tuple lengths are being enforced correctly"""
    def test_tuple_raise(self, monkeypatch):
        with monkeypatch.context() as m:
            m.setattr(sys, 'argv', ['', '--config',
                                    './tests/conf/yaml/tuple.yaml'])
            with pytest.raises(ValueError):
                ConfigArgBuilder(TypeConfig, desc='Test Builder')


class TestOverrideRaise:
    """Checks that override of a specific class variable is failing gracefully"""
    def test_override_raise(self, monkeypatch):
        with monkeypatch.context() as m:
            m.setattr(sys, 'argv', ['', '--config',
                                    './tests/conf/yaml/test.yaml'])
            with pytest.raises(ValueError):
                ConfigArgBuilder(TypeInherited, NestedStuff, NestedListStuff, desc='Test Builder')


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
            m.setattr(sys, 'argv', ['', '--config',
                                    './tests/conf/yaml/test_wrong_class_enum.yaml'])
            with pytest.raises(ValueError):
                ConfigArgBuilder(TypeConfig, NestedStuff, NestedListStuff, desc='Test Builder')


# class TestMixedGeneric:
#     def test_mixed_generic(self, monkeypatch):
#         with monkeypatch.context() as m:
#             with pytest.raises(TypeError):
#                 @spock
#                 class GenericFail:
#                     generic_fail: Tuple[List[int], List[int], int]

