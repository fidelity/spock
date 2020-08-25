# -*- coding: utf-8 -*-

# Copyright 2019 FMR LLC <opensource@fidelity.com>
# SPDX-License-Identifier: Apache-2.0

from enum import Enum
from spock.args import SavePath
from spock.config import spock
from typing import List
from typing import Optional
from typing import Tuple


class StrChoice(Enum):
    option_1 = 'option_1'
    option_2 = 'option_2'


class IntChoice(Enum):
    option_1 = 10
    option_2 = 20


class FloatChoice(Enum):
    option_1 = 10.0
    option_2 = 20.0


@spock
class ChoiceFail:
    """This creates a test config to fail on an out of set choice"""
    # Required choice -- Str
    choice_p_str: StrChoice


@spock
class TypeConfig:
    """This creates a test Spock config of all supported variable types as required parameters"""
    # Special Type -- Saves Generated Configs to this path
    save_path: SavePath
    # Boolean - Set
    bool_p_set: bool
    # Boolean - Un Set
    bool_p: bool
    # Required Int
    int_p: int
    # Required Float
    float_p: float
    # Required String
    string_p: str
    # Required List -- Float
    list_p_float: List[float]
    # Required List -- Int
    list_p_int: List[int]
    # Required List of List -- Int
    list_list_p_int: List[List[int]]
    # Required List -- Str
    list_p_str: List[str]
    # Required List -- Bool
    list_p_bool: List[bool]
    # Required Tuple -- Float
    tuple_p_float: Tuple[float]
    # Required Tuple -- Int
    tuple_p_int: Tuple[int]
    # Required Tuple -- Str
    tuple_p_str: Tuple[str]
    # Required Tuple -- Bool
    tuple_p_bool: Tuple[bool]
    # Required choice -- Str
    choice_p_str: StrChoice
    # Required choice -- Int
    choice_p_int: IntChoice
    # Required choice -- Float
    choice_p_float: FloatChoice


@spock
class TypeOptConfig:
    """This creates a test Spock config of all supported variable types as optional parameters"""
    # DEFAULTS NOT SET #
    # Optional Int default not set
    int_p_opt_no_def: Optional[int]
    # Optional Float default not set
    float_p_opt_no_def: Optional[float]
    # Optional String default not set
    string_p_opt_no_def: Optional[str]
    # Optional List default not set
    list_p_opt_no_def_float: Optional[List[float]]
    # Optional List default not set
    list_p_opt_no_def_int: Optional[List[int]]
    # Optional List default not set
    list_p_opt_no_def_str: Optional[List[str]]
    # Optional List default not set
    list_p_opt_no_def_bool: Optional[List[bool]]
    # Optional Tuple default not set
    tuple_p_opt_no_def_float: Optional[Tuple[float]]
    # Optional Tuple default not set
    tuple_p_opt_no_def_int: Optional[Tuple[int]]
    # Optional Tuple default not set
    tuple_p_opt_no_def_str: Optional[Tuple[str]]
    # Optional Tuple default not set
    tuple_p_opt_no_def_bool: Optional[Tuple[bool]]
    # Additional dummy argument
    int_p: Optional[int]


@spock
class TypeDefaultConfig:
    """This creates a test Spock config of all supported variable types as required parameters and falls back
        to defaults
    """
    # Boolean - Set
    bool_p_set_def: bool = True
    # Required Int
    int_p_def: int = 10
    # Required Float
    float_p_def: float = 10.0
    # Required String
    string_p_def: str = 'Spock'
    # Required List -- Float
    list_p_float_def: List[float] = [10.0, 20.0]
    # Required List -- Int
    list_p_int_def: List[int] = [10, 20]
    # Required List -- Str
    list_p_str_def: List[str] = ['Spock', 'Package']
    # Required List -- Bool
    list_p_bool_def: List[bool] = [True, False]
    # Required Tuple -- Float
    tuple_p_float_def: Tuple[float] = (10.0, 20.0)
    # Required Tuple -- Int
    tuple_p_int_def: Tuple[int] = (10, 20)
    # Required Tuple -- Str
    tuple_p_str_def: Tuple[str] = ('Spock', 'Package')
    # Required Tuple -- Bool
    tuple_p_bool_def: Tuple[bool] = (True, False)
    # Required choice
    choice_p_str_def: StrChoice = 'option_2'


@spock
class TypeDefaultOptConfig:
    """This creates a test Spock config of all supported variable types as optional parameters"""
    # DEFAULTS SET #
    # Optional Int default set
    int_p_opt_def: Optional[int] = 10
    # Optional Int default set
    float_p_opt_def: Optional[float] = 10.0
    # Optional String default set
    string_p_opt_def: Optional[str] = 'Spock'
    # Optional List default set
    list_p_opt_def_float: Optional[List[float]] = [10.0, 20.0]
    # Optional List default set
    list_p_opt_def_int: Optional[List[int]] = [10, 20]
    # Optional List default set
    list_p_opt_def_bool: Optional[List[bool]] = [True, False]
    # Optional List default set
    list_p_opt_def_str: Optional[List[str]] = ['Spock', 'Package']
    # Optional Tuple default set
    tuple_p_opt_def_float: Optional[Tuple[float]] = (10.0, 20.0)
    # Optional Tuple default set
    tuple_p_opt_def_int: Optional[Tuple[int]] = (10, 20)
    # Optional Tuple default set
    tuple_p_opt_def_str: Optional[Tuple[str]] = ('Spock', 'Package')
    # Optional Tuple default set
    tuple_p_opt_def_bool: Optional[Tuple[bool]] = (True, False)


@spock
class TypeInherited(TypeConfig, TypeDefaultOptConfig):
    """This tests inheritance with mixed default and non-default arguments"""
    ...
