# -*- coding: utf-8 -*-

# Copyright 2019 FMR LLC <opensource@fidelity.com>
# SPDX-License-Identifier: Apache-2.0

from attr.exceptions import FrozenInstanceError
import glob
import pytest
from spock.builder import ConfigArgBuilder
from tests.attr.attr_configs_test import *
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


class TestGeneralCmdLineOverride:
    """Testing command line overrides"""
    @staticmethod
    @pytest.fixture
    def arg_builder(monkeypatch):
        with monkeypatch.context() as m:
            m.setattr(sys, 'argv', ['', '--config',
                                    './tests/conf/yaml/test.yaml',
                                    '--TypeConfig.bool_p', '--TypeConfig.int_p', '11', '--TypeConfig.float_p', '11.0',
                                    '--TypeConfig.string_p', 'Hooray',
                                    '--TypeConfig.list_p_float', '[11.0, 21.0]', '--TypeConfig.list_p_int', '[11, 21]',
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

                                    ])
            config = ConfigArgBuilder(TypeConfig, NestedStuff, NestedListStuff, desc='Test Builder')
            return config.generate()

    def test_overrides(self, arg_builder):
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
        assert arg_builder.NestedStuff.one == 12
        assert arg_builder.NestedStuff.two == 'ancora'


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
            check_path = str(tmp_path) + '/*.yaml'
            fname = glob.glob(check_path)[0]
            with open(fname, 'r') as fin:
                print(fin.read())
            assert len(list(tmp_path.iterdir())) == 1


class TestWritePathRaise:
    def test_yaml_file_writer(self, monkeypatch, tmp_path):
        """Test the YAML writer works correctly"""
        with monkeypatch.context() as m:
            m.setattr(sys, 'argv', ['', '--config',
                                    './tests/conf/yaml/test.yaml'])
            config = ConfigArgBuilder(TypeConfig, NestedStuff, NestedListStuff, TypeOptConfig, desc='Test Builder')
            # Test the chained version
            with pytest.raises(FileNotFoundError):
                config.save(user_specified_path=str(tmp_path)+'/foo.bar/fizz.buzz/', file_extension='.yaml').generate()


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
            check_path = str(tmp_path) + '/*.toml'
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
            check_path = str(tmp_path) + '/*.json'
            fname = glob.glob(check_path)[0]
            with open(fname, 'r') as fin:
                print(fin.read())
            assert len(list(tmp_path.iterdir())) == 1
