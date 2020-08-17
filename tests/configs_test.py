# -*- coding: utf-8 -*-

# Copyright 2019 FMR LLC <opensource@fidelity.com>
# SPDX-License-Identifier: Apache-2.0

from spock.backend.dataclass.args import *
from spock.config import spock_config


@spock_config
class ChoiceFail:
    """This creates a test config to fail on an out of set choice"""
    # Required choice -- Str
    choice_p_str: ChoiceArg(choice_set=['option_1', 'option_2'])


@spock_config
class TypeConfig:
    """This creates a test Spock config of all supported variable types as required parameters"""
    # Special Type -- Saves Generated Configs to this path
    save_path: SavePathOptArg
    # Boolean - Set
    bool_p_set: BoolArg
    # Boolean - Un Set
    bool_p: BoolArg
    # Required Int
    int_p: IntArg
    # Required Float
    float_p: FloatArg
    # Required String
    string_p: StrArg
    # Required List -- Float
    list_p_float: ListArg[float]
    # Required List -- Int
    list_p_int: ListArg[int]
    # Required List -- Str
    list_p_str: ListArg[str]
    # Required List -- Bool
    list_p_bool: ListArg[bool]
    # Required Tuple -- Float
    tuple_p_float: TupleArg[float]
    # Required Tuple -- Int
    tuple_p_int: TupleArg[int]
    # Required Tuple -- Str
    tuple_p_str: TupleArg[str]
    # Required Tuple -- Bool
    tuple_p_bool: TupleArg[bool]
    # Required choice -- Str
    choice_p_str: ChoiceArg(choice_set=['option_1', 'option_2'])
    # Required choice -- Int
    choice_p_int: ChoiceArg(choice_set=[10, 20])
    # Required choice -- Float
    choice_p_float: ChoiceArg(choice_set=[10.0, 20.0])


@spock_config
class TypeOptConfig:
    """This creates a test Spock config of all supported variable types as optional parameters"""
    # DEFAULTS NOT SET #
    # Optional Int default not set
    int_p_opt_no_def: IntOptArg
    # Optional Float default not set
    float_p_opt_no_def: FloatOptArg
    # Optional String default not set
    string_p_opt_no_def: StrOptArg
    # Optional List default not set
    list_p_opt_no_def_float: ListOptArg[float]
    # Optional List default not set
    list_p_opt_no_def_int: ListOptArg[int]
    # Optional List default not set
    list_p_opt_no_def_str: ListOptArg[str]
    # Optional List default not set
    list_p_opt_no_def_bool: ListOptArg[bool]
    # Optional Tuple default not set
    tuple_p_opt_no_def_float: TupleOptArg[float]
    # Optional Tuple default not set
    tuple_p_opt_no_def_int: TupleOptArg[int]
    # Optional Tuple default not set
    tuple_p_opt_no_def_str: TupleOptArg[str]
    # Optional Tuple default not set
    tuple_p_opt_no_def_bool: TupleOptArg[bool]
    # Additional dummy argument
    int_p: IntOptArg


@spock_config
class TypeDefaultConfig:
    """This creates a test Spock config of all supported variable types as required parameters and falls back
        to defaults
    """
    # Boolean - Set
    bool_p_set_def: BoolArg = True
    # Required Int
    int_p_def: IntArg = 10
    # Required Float
    float_p_def: FloatArg = 10.0
    # Required String
    string_p_def: StrArg = 'Spock'
    # Required List -- Float
    list_p_float_def: ListArg[float] = ListArg.defaults([10.0, 20.0])
    # Required List -- Int
    list_p_int_def: ListArg[int] = ListArg.defaults([10, 20])
    # Required List -- Str
    list_p_str_def: ListArg[str] = ListArg.defaults(['Spock', 'Package'])
    # Required List -- Bool
    list_p_bool_def: ListArg[bool] = ListArg.defaults([True, False])
    # Required Tuple -- Float
    tuple_p_float_def: TupleArg[float] = TupleArg.defaults((10.0, 20.0))
    # Required Tuple -- Int
    tuple_p_int_def: TupleArg[int] = TupleArg.defaults((10, 20))
    # Required Tuple -- Str
    tuple_p_str_def: TupleArg[str] = TupleArg.defaults(('Spock', 'Package'))
    # Required Tuple -- Bool
    tuple_p_bool_def: TupleArg[bool] = TupleArg.defaults((True, False))
    # Required choice
    choice_p_str_def: ChoiceArg(choice_set=['option_1', 'option_2'], default='option_2')


@spock_config
class TypeDefaultOptConfig:
    """This creates a test Spock config of all supported variable types as optional parameters"""
    # DEFAULTS SET #
    # Optional Int default set
    int_p_opt_def: IntOptArg = 10
    # Optional Int default set
    float_p_opt_def: FloatOptArg = 10.0
    # Optional String default set
    string_p_opt_def: StrOptArg = 'Spock'
    # Optional List default set
    list_p_opt_def_float: ListOptArg[float] = ListOptArg.defaults([10.0, 20.0])
    # Optional List default set
    list_p_opt_def_int: ListOptArg[int] = ListOptArg.defaults([10, 20])
    # Optional List default set
    list_p_opt_def_bool: ListOptArg[bool] = ListOptArg.defaults([True, False])
    # Optional List default set
    list_p_opt_def_str: ListOptArg[str] = ListOptArg.defaults(['Spock', 'Package'])
    # Optional Tuple default set
    tuple_p_opt_def_float: TupleOptArg[float] = TupleOptArg.defaults((10.0, 20.0))
    # Optional Tuple default set
    tuple_p_opt_def_int: TupleOptArg[int] = TupleOptArg.defaults((10, 20))
    # Optional Tuple default set
    tuple_p_opt_def_str: TupleOptArg[str] = TupleOptArg.defaults(('Spock', 'Package'))
    # Optional Tuple default set
    tuple_p_opt_def_bool: TupleOptArg[bool] = TupleOptArg.defaults((True, False))


@spock_config
class TypeInherited(TypeConfig, TypeDefaultOptConfig):
    """This tests inheritance with mixed default and non-default arguments"""
    ...
