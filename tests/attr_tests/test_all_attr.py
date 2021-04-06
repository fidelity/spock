# -*- coding: utf-8 -*-

# Copyright 2019 FMR LLC <opensource@fidelity.com>
# SPDX-License-Identifier: Apache-2.0

from attr.exceptions import FrozenInstanceError
import glob
import os
import pytest
from spock.builder import ConfigArgBuilder
from spock.config import isinstance_spock
from tests.attr_tests.attr_configs_test import *
import sys


class AllTypes:
    # Required #
    def test_all_set(self, arg_builder):
        # Required #
        assert arg_builder.TypeConfig.bool_p_set is True
        assert arg_builder.TypeConfig.bool_p is False
        assert arg_builder.TypeConfig.int_p == 10
        assert arg_builder.TypeConfig.float_p == 12.0
        assert arg_builder.TypeConfig.string_p == 'Spock'
        assert arg_builder.TypeConfig.list_p_float == [10.0, 20.0]
        assert arg_builder.TypeConfig.list_p_int == [10, 20]
        assert arg_builder.TypeConfig.list_p_str == ['Spock', 'Package']
        assert arg_builder.TypeConfig.list_p_bool == [True, False]
        assert arg_builder.TypeConfig.tuple_p_float == (10.0, 20.0)
        assert arg_builder.TypeConfig.tuple_p_int == (10, 20)
        assert arg_builder.TypeConfig.tuple_p_str == ('Spock', 'Package')
        assert arg_builder.TypeConfig.tuple_p_bool == (True, False)
        assert arg_builder.TypeConfig.choice_p_str == 'option_1'
        assert arg_builder.TypeConfig.choice_p_int == 10
        assert arg_builder.TypeConfig.choice_p_float == 10.0
        assert arg_builder.TypeConfig.list_list_p_int == [[10, 20], [10, 20]]
        assert arg_builder.TypeConfig.list_choice_p_str == ['option_1']
        assert arg_builder.TypeConfig.list_list_choice_p_str == [['option_1'], ['option_1']]
        assert arg_builder.TypeConfig.list_choice_p_int == [10]
        assert arg_builder.TypeConfig.list_choice_p_float == [10.0]
        assert arg_builder.TypeConfig.nested.one == 11
        assert arg_builder.TypeConfig.nested.two == 'ciao'
        assert arg_builder.TypeConfig.nested_list[0].one == 10
        assert arg_builder.TypeConfig.nested_list[0].two == 'hello'
        assert arg_builder.TypeConfig.nested_list[1].one == 20
        assert arg_builder.TypeConfig.nested_list[1].two == 'bye'
        assert arg_builder.TypeConfig.class_enum.one == 11
        assert arg_builder.TypeConfig.class_enum.two == 'ciao'
        # Optional #
        assert arg_builder.TypeOptConfig.int_p_opt_no_def is None
        assert arg_builder.TypeOptConfig.float_p_opt_no_def is None
        assert arg_builder.TypeOptConfig.string_p_opt_no_def is None
        assert arg_builder.TypeOptConfig.list_p_opt_no_def_float is None
        assert arg_builder.TypeOptConfig.list_p_opt_no_def_int is None
        assert arg_builder.TypeOptConfig.list_p_opt_no_def_str is None
        assert arg_builder.TypeOptConfig.list_p_opt_no_def_bool is None
        assert arg_builder.TypeOptConfig.tuple_p_opt_no_def_float is None
        assert arg_builder.TypeOptConfig.tuple_p_opt_no_def_int is None
        assert arg_builder.TypeOptConfig.tuple_p_opt_no_def_str is None
        assert arg_builder.TypeOptConfig.tuple_p_opt_no_def_bool is None
        assert arg_builder.TypeOptConfig.choice_p_opt_no_def_str is None
        assert arg_builder.TypeOptConfig.list_choice_p_opt_no_def_str is None
        assert arg_builder.TypeOptConfig.list_list_choice_p_opt_no_def_str is None
        assert arg_builder.TypeOptConfig.nested_opt_no_def is None
        assert arg_builder.TypeOptConfig.nested_list_opt_no_def is None
        assert arg_builder.TypeOptConfig.class_enum_opt_no_def is None


class AllDefaults:
    def test_all_defaults(self, arg_builder):
        # Defaults #
        assert arg_builder.TypeDefaultConfig.bool_p_set_def is True
        assert arg_builder.TypeDefaultConfig.int_p_def == 10
        assert arg_builder.TypeDefaultConfig.float_p_def == 10.0
        assert arg_builder.TypeDefaultConfig.string_p_def == 'Spock'
        assert arg_builder.TypeDefaultConfig.list_p_float_def == [10.0, 20.0]
        assert arg_builder.TypeDefaultConfig.list_p_int_def == [10, 20]
        assert arg_builder.TypeDefaultConfig.list_p_str_def == ['Spock', 'Package']
        assert arg_builder.TypeDefaultConfig.list_p_bool_def == [True, False]
        assert arg_builder.TypeDefaultConfig.tuple_p_float_def == (10.0, 20.0)
        assert arg_builder.TypeDefaultConfig.tuple_p_int_def == (10, 20)
        assert arg_builder.TypeDefaultConfig.tuple_p_str_def == ('Spock', 'Package')
        assert arg_builder.TypeDefaultConfig.tuple_p_bool_def == (True, False)
        assert arg_builder.TypeDefaultConfig.choice_p_str_def == 'option_2'
        assert arg_builder.TypeDefaultConfig.list_choice_p_str_def == ['option_1']
        assert arg_builder.TypeDefaultConfig.list_list_choice_p_str_def == [['option_1'], ['option_1']]
        assert arg_builder.TypeDefaultConfig.nested_def.one == 11
        assert arg_builder.TypeDefaultConfig.nested_def.two == 'ciao'
        assert arg_builder.TypeDefaultConfig.nested_list_def[0].one == 10
        assert arg_builder.TypeDefaultConfig.nested_list_def[0].two == 'hello'
        assert arg_builder.TypeDefaultConfig.nested_list_def[1].one == 20
        assert arg_builder.TypeDefaultConfig.nested_list_def[1].two == 'bye'
        assert arg_builder.TypeDefaultConfig.class_enum_def.one == 11
        assert arg_builder.TypeDefaultConfig.class_enum_def.two == 'ciao'
        # Optional w/ Defaults #
        assert arg_builder.TypeDefaultOptConfig.int_p_opt_def == 10
        assert arg_builder.TypeDefaultOptConfig.float_p_opt_def == 10.0
        assert arg_builder.TypeDefaultOptConfig.string_p_opt_def == 'Spock'
        assert arg_builder.TypeDefaultOptConfig.list_p_opt_def_float == [10.0, 20.0]
        assert arg_builder.TypeDefaultOptConfig.list_p_opt_def_int == [10, 20]
        assert arg_builder.TypeDefaultOptConfig.list_p_opt_def_str == ['Spock', 'Package']
        assert arg_builder.TypeDefaultOptConfig.list_p_opt_def_bool == [True, False]
        assert arg_builder.TypeDefaultOptConfig.tuple_p_opt_def_float == (10.0, 20.0)
        assert arg_builder.TypeDefaultOptConfig.tuple_p_opt_def_int == (10, 20)
        assert arg_builder.TypeDefaultOptConfig.tuple_p_opt_def_str == ('Spock', 'Package')
        assert arg_builder.TypeDefaultOptConfig.tuple_p_opt_def_bool == (True, False)
        assert arg_builder.TypeDefaultOptConfig.choice_p_str_opt_def == 'option_2'
        assert arg_builder.TypeDefaultOptConfig.list_choice_p_str_opt_def == ['option_1']
        assert arg_builder.TypeDefaultOptConfig.list_list_choice_p_str_opt_def == [['option_1'], ['option_1']]
        assert arg_builder.TypeDefaultOptConfig.nested_opt_def.one == 11
        assert arg_builder.TypeDefaultOptConfig.nested_opt_def.two == 'ciao'
        assert arg_builder.TypeDefaultOptConfig.nested_list_opt_def[0].one == 10
        assert arg_builder.TypeDefaultOptConfig.nested_list_opt_def[0].two == 'hello'
        assert arg_builder.TypeDefaultOptConfig.nested_list_opt_def[1].one == 20
        assert arg_builder.TypeDefaultOptConfig.nested_list_opt_def[1].two == 'bye'
        assert arg_builder.TypeDefaultOptConfig.class_enum_opt_def.one == 11
        assert arg_builder.TypeDefaultOptConfig.class_enum_opt_def.two == 'ciao'


class AllInherited:
    def test_all_inherited(self, arg_builder):
        # Required #
        assert arg_builder.TypeInherited.bool_p_set is True
        assert arg_builder.TypeInherited.bool_p is False
        assert arg_builder.TypeInherited.int_p == 10
        assert arg_builder.TypeInherited.float_p == 10.0
        assert arg_builder.TypeInherited.string_p == 'Spock'
        assert arg_builder.TypeInherited.list_p_float == [10.0, 20.0]
        assert arg_builder.TypeInherited.list_p_int == [10, 20]
        assert arg_builder.TypeInherited.list_p_str == ['Spock', 'Package']
        assert arg_builder.TypeInherited.list_p_bool == [True, False]
        assert arg_builder.TypeInherited.tuple_p_float == (10.0, 20.0)
        assert arg_builder.TypeInherited.tuple_p_int == (10, 20)
        assert arg_builder.TypeInherited.tuple_p_str == ('Spock', 'Package')
        assert arg_builder.TypeInherited.tuple_p_bool == (True, False)
        assert arg_builder.TypeInherited.choice_p_str == 'option_1'
        assert arg_builder.TypeInherited.choice_p_int == 10
        assert arg_builder.TypeInherited.choice_p_float == 10.0
        assert arg_builder.TypeInherited.list_list_p_int == [[10, 20], [10, 20]]
        assert arg_builder.TypeInherited.list_choice_p_str == ['option_1']
        assert arg_builder.TypeInherited.list_list_choice_p_str == [['option_1'], ['option_1']]
        assert arg_builder.TypeInherited.list_choice_p_int == [10]
        assert arg_builder.TypeInherited.list_choice_p_float == [10.0]
        assert arg_builder.TypeInherited.nested.one == 11
        assert arg_builder.TypeInherited.nested.two == 'ciao'
        assert arg_builder.TypeInherited.nested_list[0].one == 10
        assert arg_builder.TypeInherited.nested_list[0].two == 'hello'
        assert arg_builder.TypeInherited.nested_list[1].one == 20
        assert arg_builder.TypeInherited.nested_list[1].two == 'bye'
        assert arg_builder.TypeInherited.class_enum.one == 11
        assert arg_builder.TypeInherited.class_enum.two == 'ciao'
        # Optional w/ Defaults #
        assert arg_builder.TypeInherited.int_p_opt_def == 10
        assert arg_builder.TypeInherited.float_p_opt_def == 10.0
        assert arg_builder.TypeInherited.string_p_opt_def == 'Spock'
        assert arg_builder.TypeInherited.list_p_opt_def_float == [10.0, 20.0]
        assert arg_builder.TypeInherited.list_p_opt_def_int == [10, 20]
        assert arg_builder.TypeInherited.list_p_opt_def_str == ['Spock', 'Package']
        assert arg_builder.TypeInherited.list_p_opt_def_bool == [True, False]
        assert arg_builder.TypeInherited.tuple_p_opt_def_float == (10.0, 20.0)
        assert arg_builder.TypeInherited.tuple_p_opt_def_int == (10, 20)
        assert arg_builder.TypeInherited.tuple_p_opt_def_str == ('Spock', 'Package')
        assert arg_builder.TypeInherited.tuple_p_opt_def_bool == (True, False)


# TESTS
# BASED ON YAML FILE
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


class TestRaiseWrongInputType:
    """Check all required types work as expected """
    def test_wrong_input_raise(self, monkeypatch):
        with monkeypatch.context() as m:
            m.setattr(sys, 'argv', ['', '--config',
                                    './tests/conf/yaml/test.foo'])
            with pytest.raises(ValueError):
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
            config = ConfigArgBuilder(TypeConfig, NestedStuff, NestedListStuff, TypeOptConfig, TypeDefaultConfig,
                                      TypeDefaultOptConfig,
                                      desc='Test Builder')
            return config.generate()


class TestHelp:
    def test_help(self, monkeypatch):
        with monkeypatch.context() as m:
            m.setattr(sys, 'argv', ['', '--config',
                                    './tests/conf/yaml/test.yaml', '--help'])
            with pytest.raises(SystemExit):
                config = ConfigArgBuilder(TypeConfig, NestedStuff, NestedListStuff, TypeOptConfig, desc='Test Builder')
                return config.generate()


class TestSpockspaceRepr:
    def test_repr(self, monkeypatch, capsys):
        with monkeypatch.context() as m:
            m.setattr(sys, 'argv', ['', '--config',
                                    './tests/conf/yaml/test.yaml'])
            config = ConfigArgBuilder(TypeConfig, NestedStuff, NestedListStuff, TypeOptConfig, desc='Test Builder')
            print(config.generate())
            out, _ = capsys.readouterr()
            assert ('NestedListStuff' in out) and 'TypeConfig' in out


class TestFrozen:
    """Testing the frozen state of the spock config object"""
    @staticmethod
    @pytest.fixture
    def arg_builder(monkeypatch):
        with monkeypatch.context() as m:
            m.setattr(sys, 'argv', ['', '--config',
                                    './tests/conf/yaml/test.yaml'])
            config = ConfigArgBuilder(TypeConfig, NestedStuff, NestedListStuff, TypeOptConfig, desc='Test Builder')
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


class TestRaiseCmdLineNoKey:
    """Testing command line overrides"""
    def test_cmd_line_no_key(self, monkeypatch):
        with monkeypatch.context() as m:
            m.setattr(sys, 'argv', ['', '--config',
                                    './tests/conf/yaml/test.yaml', '--TypeConfig.foo_bar_stuff', '11'
                                    ])
            with pytest.raises(SystemExit):
                config = ConfigArgBuilder(TypeConfig, NestedStuff, NestedListStuff, desc='Test Builder')
                return config.generate()


class TestRaiseCmdLineListLen:
    """Testing command line overrides"""
    def test_cmd_line_list_len(self, monkeypatch):
        with monkeypatch.context() as m:
            m.setattr(sys, 'argv', ['', '--config',
                                    './tests/conf/yaml/test.yaml',
                                    '--TypeConfig.nested_list.NestedListStuff.one', '[11]'
                                    ])
            with pytest.raises(ValueError):
                config = ConfigArgBuilder(TypeConfig, NestedStuff, NestedListStuff, desc='Test Builder')
                return config.generate()



class TestClassCmdLineOverride:
    """Testing command line overrides"""
    @staticmethod
    @pytest.fixture
    def arg_builder(monkeypatch):
        with monkeypatch.context() as m:
            m.setattr(sys, 'argv', ['', '--config',
                                    './tests/conf/yaml/test_class.yaml',
                                    '--TypeConfig.bool_p', '--TypeConfig.int_p', '11', '--TypeConfig.float_p', '11.0',
                                    '--TypeConfig.string_p', 'Hooray',
                                    '--TypeConfig.list_p_float', '[11.0,21.0]', '--TypeConfig.list_p_int', '[11, 21]',
                                    '--TypeConfig.list_p_str', "['Hooray', 'Working']",
                                    '--TypeConfig.list_p_bool', '[False, True]',
                                    '--TypeConfig.tuple_p_float', '(11.0, 21.0)', '--TypeConfig.tuple_p_int', '(11, 21)',
                                    '--TypeConfig.tuple_p_str', "('Hooray', 'Working')",
                                    '--TypeConfig.tuple_p_bool', '(False, True)',
                                    '--TypeConfig.list_list_p_int', "[[11, 21], [11, 21]]",
                                    '--TypeConfig.choice_p_str', 'option_2',
                                    '--TypeConfig.choice_p_int', '20', '--TypeConfig.choice_p_float', '20.0',
                                    '--TypeConfig.list_choice_p_str', "['option_2']",
                                    '--TypeConfig.list_list_choice_p_str', "[['option_2'], ['option_2']]",
                                    '--TypeConfig.list_choice_p_int', '[20]',
                                    '--TypeConfig.list_choice_p_float', '[20.0]',
                                    '--NestedStuff.one', '12', '--NestedStuff.two', 'ancora',
                                    '--TypeConfig.nested_list.NestedListStuff.one', '[11, 21]',
                                    '--TypeConfig.nested_list.NestedListStuff.two', "['Hooray', 'Working']",
                                    ])
            config = ConfigArgBuilder(TypeConfig, NestedStuff, NestedListStuff, desc='Test Builder')
            return config.generate()

    def test_class_overrides(self, arg_builder):
        assert arg_builder.TypeConfig.bool_p is True
        assert arg_builder.TypeConfig.int_p == 11
        assert arg_builder.TypeConfig.float_p == 11.0
        assert arg_builder.TypeConfig.string_p == 'Hooray'
        assert arg_builder.TypeConfig.list_p_float == [11.0, 21.0]
        assert arg_builder.TypeConfig.list_p_int == [11, 21]
        assert arg_builder.TypeConfig.list_p_str == ['Hooray', 'Working']
        assert arg_builder.TypeConfig.list_p_bool == [False, True]
        assert arg_builder.TypeConfig.tuple_p_float == (11.0, 21.0)
        assert arg_builder.TypeConfig.tuple_p_int == (11, 21)
        assert arg_builder.TypeConfig.tuple_p_str == ('Hooray', 'Working')
        assert arg_builder.TypeConfig.tuple_p_bool == (False, True)
        assert arg_builder.TypeConfig.choice_p_str == 'option_2'
        assert arg_builder.TypeConfig.choice_p_int == 20
        assert arg_builder.TypeConfig.choice_p_float == 20.0
        assert arg_builder.TypeConfig.list_list_p_int == [[11, 21], [11, 21]]
        assert arg_builder.TypeConfig.list_choice_p_str == ['option_2']
        assert arg_builder.TypeConfig.list_list_choice_p_str == [['option_2'], ['option_2']]
        assert arg_builder.TypeConfig.list_choice_p_int == [20]
        assert arg_builder.TypeConfig.list_choice_p_float == [20.0]
        assert arg_builder.TypeConfig.class_enum.one == 12
        assert arg_builder.TypeConfig.class_enum.two == 'ancora'
        assert arg_builder.NestedListStuff[0].one == 11
        assert arg_builder.NestedListStuff[0].two == 'Hooray'
        assert arg_builder.NestedListStuff[1].one == 21
        assert arg_builder.NestedListStuff[1].two == 'Working'


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


class TestNonAttrs:
    def test_non_attrs_fail(self, monkeypatch):
        with monkeypatch.context() as m:
            with pytest.raises(TypeError):
                class AttrFail:
                    failed_attr: int
                config = ConfigArgBuilder(TypeConfig, NestedStuff, NestedListStuff, TypeOptConfig, AttrFail,
                                          configs=['./tests/conf/yaml/test.yaml'])
                return config.generate()


class TestChoiceRaises:
    """Check all inherited types work as expected """
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


class TestConfigArgType:
    """Test functions related to the argument builder"""
    def test_type_arg_builder(self, monkeypatch):
        with monkeypatch.context() as m:
            m.setattr(sys, 'argv', ['', '--config',
                                    './tests/conf/yaml/test.yaml'])
            with pytest.raises(TypeError):
                ConfigArgBuilder(['Names'], desc='Test Builder')


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


class TestMixedGeneric:
    def test_mixed_generic(self, monkeypatch):
        with monkeypatch.context() as m:
            with pytest.raises(TypeError):
                @spock
                class GenericFail:
                    generic_fail: Tuple[List[int], List[int], int]


class TestConfigCycles:
    """Checks the raise for cyclical dependencies"""
    def test_config_cycles(self, monkeypatch):
        with monkeypatch.context() as m:
            m.setattr(sys, 'argv', ['', '--config',
                                    './tests/conf/yaml/test_cycle.yaml'])
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


class TestDefaultWriter:
    def test_default_file_writer(self, monkeypatch, tmp_path):
        """Test the default writer works correctly"""
        with monkeypatch.context() as m:
            m.setattr(sys, 'argv', ['', '--config',
                                    './tests/conf/yaml/test.yaml'])
            config = ConfigArgBuilder(TypeConfig, NestedStuff, NestedListStuff, TypeOptConfig, desc='Test Builder')
            # Test the chained version
            config.save(user_specified_path=tmp_path).generate()
            assert len(list(tmp_path.iterdir())) == 1


class TestYAMLWriter:
    def test_yaml_file_writer(self, monkeypatch, tmp_path):
        """Test the YAML writer works correctly"""
        with monkeypatch.context() as m:
            m.setattr(sys, 'argv', ['', '--config',
                                    './tests/conf/yaml/test.yaml'])
            config = ConfigArgBuilder(TypeConfig, NestedStuff, NestedListStuff, TypeOptConfig, desc='Test Builder')
            # Test the chained version
            config.save(user_specified_path=tmp_path, file_extension='.yaml').generate()
            check_path = f'{str(tmp_path)}/*.yaml'
            fname = glob.glob(check_path)[0]
            with open(fname, 'r') as fin:
                print(fin.read())
            assert len(list(tmp_path.iterdir())) == 1


class TestYAMLWriterCreate:
    def test_yaml_file_writer_create(self, monkeypatch, tmp_path):
        """Test the YAML writer works correctly"""
        with monkeypatch.context() as m:
            m.setattr(sys, 'argv', ['', '--config',
                                    './tests/conf/yaml/test.yaml'])
            config = ConfigArgBuilder(TypeConfig, NestedStuff, NestedListStuff, TypeOptConfig, desc='Test Builder',
                                      create_save_path=True)
            # Test the chained version
            config.save(user_specified_path=f'{tmp_path}/tmp', file_extension='.yaml').generate()
            check_path = f'{str(tmp_path)}/tmp/*.yaml'
            fname = glob.glob(check_path)[0]
            with open(fname, 'r') as fin:
                print(fin.read())
            assert len(list(tmp_path.iterdir())) == 1


class TestYAMLWriterSavePath:
    def test_yaml_file_writer_save_path(self, monkeypatch):
        """Test the YAML writer works correctly"""
        with monkeypatch.context() as m:
            m.setattr(sys, 'argv', ['', '--config',
                                    './tests/conf/yaml/test_save_path.yaml'])
            config = ConfigArgBuilder(TypeConfig, NestedStuff, NestedListStuff, TypeOptConfig, desc='Test Builder')
            # Test the chained version
            config_values = config.save(file_extension='.yaml', file_name='pytest').generate()
            check_path = f'{str(config_values.TypeConfig.save_path)}/pytest.spock.cfg.yaml'
            fname = glob.glob(check_path)[0]
            with open(fname, 'r') as fin:
                print(fin.read())
            assert os.path.exists(check_path)
            # Clean up if assert is good
            if os.path.exists(check_path):
                os.remove(check_path)


class TestYAMLWriterNoPath:
    def test_yaml_file_writer_no_path(self, monkeypatch):
        """Test the YAML writer works correctly"""
        with monkeypatch.context() as m:
            m.setattr(sys, 'argv', ['', '--config',
                                    './tests/conf/yaml/test.yaml'])
            with pytest.raises(ValueError):
                config = ConfigArgBuilder(TypeConfig, NestedStuff, NestedListStuff, TypeOptConfig, desc='Test Builder')
                # Test the chained version
                config.save(file_extension='.yaml', file_name='pytest').generate()


class TestWritePathRaise:
    def test_yaml_file_writer(self, monkeypatch, tmp_path):
        """Test the YAML writer fails correctly when create path isn't set"""
        with monkeypatch.context() as m:
            m.setattr(sys, 'argv', ['', '--config',
                                    './tests/conf/yaml/test.yaml'])
            config = ConfigArgBuilder(TypeConfig, NestedStuff, NestedListStuff, TypeOptConfig, desc='Test Builder')
            # Test the chained version
            with pytest.raises(FileNotFoundError):
                config.save(user_specified_path=f'{str(tmp_path)}/foo.bar/fizz.buzz/', file_extension='.yaml').generate()


class TestInvalidExtensionTypeRaise:
    def test_yaml_invalid_extension(self, monkeypatch, tmp_path):
        """Test the YAML writer fails correctly when create path isn't set"""
        with monkeypatch.context() as m:
            m.setattr(sys, 'argv', ['', '--config',
                                    './tests/conf/yaml/test.yaml'])
            config = ConfigArgBuilder(TypeConfig, NestedStuff, NestedListStuff, TypeOptConfig, desc='Test Builder')
            # Test the chained version
            with pytest.raises(ValueError):
                config.save(user_specified_path=f'{str(tmp_path)}/foo.bar/fizz.buzz/', file_extension='.foo').generate()


class TestIsInstance:
    def test_isinstance(self):
        """Test that isinstance is behaving correctly"""
        assert isinstance_spock(TypeConfig) is True
        assert isinstance_spock(object) is False
        assert isinstance_spock(StrChoice) is False


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
            config = ConfigArgBuilder(TypeConfig, NestedStuff, NestedListStuff, TypeOptConfig, TypeDefaultConfig, TypeDefaultOptConfig,
                                      desc='Test Builder')
            return config.generate()


class TestTOMLWriter:
    def test_toml_file_writer(self, monkeypatch, tmp_path):
        """Check the TOML writer works correctly"""
        with monkeypatch.context() as m:
            m.setattr(sys, 'argv', ['', '--config',
                                    './tests/conf/toml/test.toml'])
            config = ConfigArgBuilder(TypeConfig, NestedStuff, NestedListStuff, TypeOptConfig, desc='Test Builder')
            # Test the chained version
            config.save(user_specified_path=tmp_path, file_extension='.toml').generate()
            check_path = f'{str(tmp_path)}/*.toml'
            fname = glob.glob(check_path)[0]
            with open(fname, 'r') as fin:
                print(fin.read())
            assert len(list(tmp_path.iterdir())) == 1


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
            config = ConfigArgBuilder(TypeConfig, NestedStuff, NestedListStuff, TypeOptConfig, TypeDefaultConfig, TypeDefaultOptConfig,
                                      desc='Test Builder')
            return config.generate()


class TestJSONWriter:
    def test_json_file_writer(self, monkeypatch, tmp_path):
        """Check JSON writer works correctly"""
        with monkeypatch.context() as m:
            m.setattr(sys, 'argv', ['', '--config',
                                    './tests/conf/json/test.json'])
            config = ConfigArgBuilder(TypeConfig, NestedStuff, NestedListStuff, TypeOptConfig, desc='Test Builder')
            # Test the chained version
            config.save(user_specified_path=tmp_path, file_extension='.json').generate()
            check_path = f'{str(tmp_path)}/*.json'
            fname = glob.glob(check_path)[0]
            with open(fname, 'r') as fin:
                print(fin.read())
            assert len(list(tmp_path.iterdir())) == 1
