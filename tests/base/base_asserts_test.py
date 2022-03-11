# -*- coding: utf-8 -*-
# Copyright FMR LLC <opensource@fidelity.com>
# SPDX-License-Identifier: Apache-2.0

from tests.base.attr_configs_test import FirstDoubleNestedConfig, foo


class AllTypes:
    # Required #
    def test_all_set(self, arg_builder):
        # Required #
        assert arg_builder.TypeConfig.bool_p_set is True
        assert arg_builder.TypeConfig.bool_p is False
        assert arg_builder.TypeConfig.int_p == 10
        assert arg_builder.TypeConfig.float_p == 12.0
        assert arg_builder.TypeConfig.string_p == "Spock"
        assert arg_builder.TypeConfig.list_p_float == [10.0, 20.0]
        assert arg_builder.TypeConfig.list_p_int == [10, 20]
        assert arg_builder.TypeConfig.list_p_str == ["Spock", "Package"]
        assert arg_builder.TypeConfig.list_p_bool == [True, False]
        assert arg_builder.TypeConfig.tuple_p_float == (10.0, 20.0)
        assert arg_builder.TypeConfig.tuple_p_int == (10, 20)
        assert arg_builder.TypeConfig.tuple_p_str == ("Spock", "Package")
        assert arg_builder.TypeConfig.tuple_p_bool == (True, False)
        assert arg_builder.TypeConfig.tuple_p_mixed == (5, 11.5)
        assert arg_builder.TypeConfig.choice_p_str == "option_1"
        assert arg_builder.TypeConfig.choice_p_int == 10
        assert arg_builder.TypeConfig.choice_p_float == 10.0
        assert arg_builder.TypeConfig.list_list_p_int == [[10, 20], [10, 20]]
        assert arg_builder.TypeConfig.list_choice_p_str == ["option_1"]
        assert arg_builder.TypeConfig.list_list_choice_p_str == [
            ["option_1"],
            ["option_1"],
        ]
        assert arg_builder.TypeConfig.list_choice_p_int == [10]
        assert arg_builder.TypeConfig.list_choice_p_float == [10.0]
        assert arg_builder.TypeConfig.nested.one == 11
        assert arg_builder.TypeConfig.nested.two == "ciao"
        assert arg_builder.TypeConfig.nested_list[0].one == 10
        assert arg_builder.TypeConfig.nested_list[0].two == "hello"
        assert arg_builder.TypeConfig.nested_list[1].one == 20
        assert arg_builder.TypeConfig.nested_list[1].two == "bye"
        assert arg_builder.TypeConfig.class_enum.one == 11
        assert arg_builder.TypeConfig.class_enum.two == "ciao"
        assert (
            isinstance(
                arg_builder.TypeConfig.high_config.double_nested_config,
                FirstDoubleNestedConfig,
            )
            is True
        )
        assert arg_builder.TypeConfig.high_config.double_nested_config.h_factor == 0.99
        assert arg_builder.TypeConfig.high_config.double_nested_config.v_factor == 0.90
        assert arg_builder.TypeConfig.call_me == foo

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
        assert arg_builder.TypeOptConfig.call_me_maybe is None


class AllDefaults:
    def test_all_defaults(self, arg_builder):
        # Defaults #
        assert arg_builder.TypeDefaultConfig.bool_p_set_def is True
        assert arg_builder.TypeDefaultConfig.int_p_def == 10
        assert arg_builder.TypeDefaultConfig.float_p_def == 10.0
        assert arg_builder.TypeDefaultConfig.string_p_def == "Spock"
        assert arg_builder.TypeDefaultConfig.list_p_float_def == [10.0, 20.0]
        assert arg_builder.TypeDefaultConfig.list_p_int_def == [10, 20]
        assert arg_builder.TypeDefaultConfig.list_p_str_def == ["Spock", "Package"]
        assert arg_builder.TypeDefaultConfig.list_p_bool_def == [True, False]
        assert arg_builder.TypeDefaultConfig.tuple_p_float_def == (10.0, 20.0)
        assert arg_builder.TypeDefaultConfig.tuple_p_int_def == (10, 20)
        assert arg_builder.TypeDefaultConfig.tuple_p_str_def == ("Spock", "Package")
        assert arg_builder.TypeDefaultConfig.tuple_p_bool_def == (True, False)
        assert arg_builder.TypeDefaultConfig.choice_p_str_def == "option_2"
        assert arg_builder.TypeDefaultConfig.list_choice_p_str_def == ["option_1"]
        assert arg_builder.TypeDefaultConfig.list_list_choice_p_str_def == [
            ["option_1"],
            ["option_1"],
        ]
        assert arg_builder.TypeDefaultConfig.nested_def.one == 11
        assert arg_builder.TypeDefaultConfig.nested_def.two == "ciao"
        assert arg_builder.TypeDefaultConfig.nested_no_conf_def.away == "arsenal"
        assert arg_builder.TypeDefaultConfig.nested_no_conf_def.goals == 0
        assert arg_builder.TypeDefaultConfig.nested_list_def[0].one == 10
        assert arg_builder.TypeDefaultConfig.nested_list_def[0].two == "hello"
        assert arg_builder.TypeDefaultConfig.nested_list_def[1].one == 20
        assert arg_builder.TypeDefaultConfig.nested_list_def[1].two == "bye"
        assert arg_builder.TypeDefaultConfig.nested_list_def_2[0].one == 100
        assert arg_builder.TypeDefaultConfig.nested_list_def_2[0].two == "two"
        assert arg_builder.TypeDefaultConfig.nested_list_def_2[1].one == 300
        assert arg_builder.TypeDefaultConfig.nested_list_def_2[1].two == "four"
        assert arg_builder.TypeDefaultConfig.class_enum_def.one == 11
        assert arg_builder.TypeDefaultConfig.class_enum_def.two == "ciao"
        assert (
            isinstance(
                arg_builder.TypeDefaultConfig.high_config_def.double_nested_config,
                FirstDoubleNestedConfig,
            )
            is True
        )
        assert (
            arg_builder.TypeDefaultConfig.high_config_def.double_nested_config.h_factor
            == 0.99
        )
        assert (
            arg_builder.TypeDefaultConfig.high_config_def.double_nested_config.v_factor
            == 0.90
        )
        assert arg_builder.TypeDefaultConfig.call_me_maybe == foo

        # Optional w/ Defaults #
        assert arg_builder.TypeDefaultOptConfig.int_p_opt_def == 10
        assert arg_builder.TypeDefaultOptConfig.float_p_opt_def == 10.0
        assert arg_builder.TypeDefaultOptConfig.string_p_opt_def == "Spock"
        assert arg_builder.TypeDefaultOptConfig.list_p_opt_def_float == [10.0, 20.0]
        assert arg_builder.TypeDefaultOptConfig.list_p_opt_def_int == [10, 20]
        assert arg_builder.TypeDefaultOptConfig.list_p_opt_def_str == [
            "Spock",
            "Package",
        ]
        assert arg_builder.TypeDefaultOptConfig.list_p_opt_def_bool == [True, False]
        assert arg_builder.TypeDefaultOptConfig.tuple_p_opt_def_float == (10.0, 20.0)
        assert arg_builder.TypeDefaultOptConfig.tuple_p_opt_def_int == (10, 20)
        assert arg_builder.TypeDefaultOptConfig.tuple_p_opt_def_str == (
            "Spock",
            "Package",
        )
        assert arg_builder.TypeDefaultOptConfig.tuple_p_opt_def_bool == (True, False)
        assert arg_builder.TypeDefaultOptConfig.choice_p_str_opt_def == "option_2"
        assert arg_builder.TypeDefaultOptConfig.list_choice_p_str_opt_def == [
            "option_1"
        ]
        assert arg_builder.TypeDefaultOptConfig.list_list_choice_p_str_opt_def == [
            ["option_1"],
            ["option_1"],
        ]
        assert arg_builder.TypeDefaultOptConfig.nested_opt_def.one == 11
        assert arg_builder.TypeDefaultOptConfig.nested_opt_def.two == "ciao"
        assert arg_builder.TypeDefaultOptConfig.nested_list_opt_def[0].one == 10
        assert arg_builder.TypeDefaultOptConfig.nested_list_opt_def[0].two == "hello"
        assert arg_builder.TypeDefaultOptConfig.nested_list_opt_def[1].one == 20
        assert arg_builder.TypeDefaultOptConfig.nested_list_opt_def[1].two == "bye"
        assert arg_builder.TypeDefaultOptConfig.class_enum_opt_def.one == 11
        assert arg_builder.TypeDefaultOptConfig.class_enum_opt_def.two == "ciao"
        assert arg_builder.TypeDefaultOptConfig.call_me_maybe == foo


class AllInherited:
    def test_all_inherited(self, arg_builder):
        # Required #
        assert arg_builder.TypeInherited.bool_p_set is True
        assert arg_builder.TypeInherited.bool_p is False
        assert arg_builder.TypeInherited.int_p == 10
        assert arg_builder.TypeInherited.float_p == 10.0
        assert arg_builder.TypeInherited.string_p == "Spock"
        assert arg_builder.TypeInherited.list_p_float == [10.0, 20.0]
        assert arg_builder.TypeInherited.list_p_int == [10, 20]
        assert arg_builder.TypeInherited.list_p_str == ["Spock", "Package"]
        assert arg_builder.TypeInherited.list_p_bool == [True, False]
        assert arg_builder.TypeInherited.tuple_p_float == (10.0, 20.0)
        assert arg_builder.TypeInherited.tuple_p_int == (10, 20)
        assert arg_builder.TypeInherited.tuple_p_str == ("Spock", "Package")
        assert arg_builder.TypeInherited.tuple_p_bool == (True, False)
        assert arg_builder.TypeInherited.choice_p_str == "option_1"
        assert arg_builder.TypeInherited.choice_p_int == 10
        assert arg_builder.TypeInherited.choice_p_float == 10.0
        assert arg_builder.TypeInherited.list_list_p_int == [[10, 20], [10, 20]]
        assert arg_builder.TypeInherited.list_choice_p_str == ["option_1"]
        assert arg_builder.TypeInherited.list_list_choice_p_str == [
            ["option_1"],
            ["option_1"],
        ]
        assert arg_builder.TypeInherited.list_choice_p_int == [10]
        assert arg_builder.TypeInherited.list_choice_p_float == [10.0]
        assert arg_builder.TypeInherited.nested.one == 11
        assert arg_builder.TypeInherited.nested.two == "ciao"
        assert arg_builder.TypeInherited.nested_list[0].one == 10
        assert arg_builder.TypeInherited.nested_list[0].two == "hello"
        assert arg_builder.TypeInherited.nested_list[1].one == 20
        assert arg_builder.TypeInherited.nested_list[1].two == "bye"
        assert arg_builder.TypeInherited.class_enum.one == 11
        assert arg_builder.TypeInherited.class_enum.two == "ciao"
        assert (
            isinstance(
                arg_builder.TypeInherited.high_config.double_nested_config,
                FirstDoubleNestedConfig,
            )
            is True
        )
        assert (
            arg_builder.TypeInherited.high_config.double_nested_config.h_factor == 0.99
        )
        assert (
            arg_builder.TypeInherited.high_config.double_nested_config.v_factor == 0.90
        )
        assert arg_builder.TypeInherited.call_me == foo

        # Optional w/ Defaults #
        assert arg_builder.TypeInherited.int_p_opt_def == 10
        assert arg_builder.TypeInherited.float_p_opt_def == 10.0
        assert arg_builder.TypeInherited.string_p_opt_def == "Spock"
        assert arg_builder.TypeInherited.list_p_opt_def_float == [10.0, 20.0]
        assert arg_builder.TypeInherited.list_p_opt_def_int == [10, 20]
        assert arg_builder.TypeInherited.list_p_opt_def_str == ["Spock", "Package"]
        assert arg_builder.TypeInherited.list_p_opt_def_bool == [True, False]
        assert arg_builder.TypeInherited.tuple_p_opt_def_float == (10.0, 20.0)
        assert arg_builder.TypeInherited.tuple_p_opt_def_int == (10, 20)
        assert arg_builder.TypeInherited.tuple_p_opt_def_str == ("Spock", "Package")
        assert arg_builder.TypeInherited.tuple_p_opt_def_bool == (True, False)
        assert arg_builder.TypeInherited.call_me_maybe == foo


class AllDynamic:
    def test_all_dynamic(self, arg_builder):
        assert arg_builder.ConfigDynamicDefaults.x == 235
        assert arg_builder.ConfigDynamicDefaults.y == "yarghhh"
        assert arg_builder.ConfigDynamicDefaults.z == [10, 20]
        assert arg_builder.ConfigDynamicDefaults.p == 1
        assert arg_builder.ConfigDynamicDefaults.q == 'shhh'