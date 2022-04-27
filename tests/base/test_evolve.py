# -*- coding: utf-8 -*-
import sys

import attr
import pytest

from spock import spock
from spock import SpockBuilder
from spock.exceptions import _SpockEvolveError, _SpockUndecoratedClass

from tests.base.attr_configs_test import *

@attr.s(auto_attribs=True)
class FailedClass:
    one: int = 30


@spock
class NotEvolved:
    one: int = 10


@spock
class EvolveNestedStuff:
    one: int = 10
    two: str = 'hello'


@spock
class EvolveNestedListStuff:
    one: int = 10
    two: str = 'hello'


class EvolveClassChoice(Enum):
    class_nested_stuff = EvolveNestedStuff
    class_nested_list_stuff = EvolveNestedListStuff


@spock
class TypeThinDefaultConfig:
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
    string_p_def: str = "Spock"
    # Required List -- Float
    list_p_float_def: List[float] = [10.0, 20.0]
    # Required List -- Int
    list_p_int_def: List[int] = [10, 20]
    # Required List -- Str
    list_p_str_def: List[str] = ["Spock", "Package"]
    # Required List -- Bool
    list_p_bool_def: List[bool] = [True, False]
    # Required Tuple -- Float
    tuple_p_float_def: Tuple[float] = (10.0, 20.0)
    # Required Tuple -- Int
    tuple_p_int_def: Tuple[int] = (10, 20)
    # Required Tuple -- Str
    tuple_p_str_def: Tuple[str] = ("Spock", "Package")
    # Required Tuple -- Bool
    tuple_p_bool_def: Tuple[bool] = (True, False)
    # Required choice
    choice_p_str_def: StrChoice = "option_2"
    # Required list of choice -- Str
    list_choice_p_str_def: List[StrChoice] = ["option_1"]
    # Required list of list of choice -- Str
    list_list_choice_p_str_def: List[List[StrChoice]] = [["option_1"], ["option_1"]]
    # Class Enum
    class_enum_def: EvolveClassChoice = EvolveNestedStuff()


class TestEvolve:
    """Testing evolve functionality"""

    @staticmethod
    @pytest.fixture
    def arg_builder(monkeypatch):
        with monkeypatch.context() as m:
            m.setattr(sys, "argv", [""])
            config = SpockBuilder(EvolveNestedStuff, EvolveNestedListStuff, TypeThinDefaultConfig)
            return config

    def test_evolve(self, arg_builder):
        evolve_nested_stuff = EvolveNestedStuff(
            one=12345, two='abcdef'
        )
        evolve_type_config = TypeThinDefaultConfig(
            bool_p_set_def=False,
            int_p_def=16,
            float_p_def=16.0,
            string_p_def="Spocked",
            list_p_float_def=[16.0, 26.0],
            list_p_int_def=[16, 26],
            list_p_str_def=["Spocked", "Packaged"],
            list_p_bool_def=[False, True],
            tuple_p_float_def=(16.0, 26.0),
            tuple_p_int_def=(16, 26),
            tuple_p_str_def=("Spocked", "Packaged"),
            tuple_p_bool_def=(False, True),
            choice_p_str_def="option_1",
            list_choice_p_str_def=["option_2"],
            list_list_choice_p_str_def=[["option_2"], ["option_2"]]
        )
        # Evolve the class
        new_class = arg_builder.evolve(evolve_nested_stuff, evolve_type_config)
        # Assert based on evolution
        assert new_class.TypeThinDefaultConfig.bool_p_set_def is False
        assert new_class.TypeThinDefaultConfig.int_p_def == 16
        assert new_class.TypeThinDefaultConfig.float_p_def == 16.0
        assert new_class.TypeThinDefaultConfig.string_p_def == "Spocked"
        assert new_class.TypeThinDefaultConfig.list_p_float_def == [16.0, 26.0]
        assert new_class.TypeThinDefaultConfig.list_p_int_def == [16, 26]
        assert new_class.TypeThinDefaultConfig.list_p_str_def == ["Spocked", "Packaged"]
        assert new_class.TypeThinDefaultConfig.list_p_bool_def == [False, True]
        assert new_class.TypeThinDefaultConfig.tuple_p_float_def == (16.0, 26.0)
        assert new_class.TypeThinDefaultConfig.tuple_p_int_def == (16, 26)
        assert new_class.TypeThinDefaultConfig.tuple_p_str_def == ("Spocked", "Packaged")
        assert new_class.TypeThinDefaultConfig.tuple_p_bool_def == (False, True)
        assert new_class.TypeThinDefaultConfig.choice_p_str_def == "option_1"
        assert new_class.TypeThinDefaultConfig.list_choice_p_str_def == ["option_2"]
        assert new_class.TypeThinDefaultConfig.list_list_choice_p_str_def == [
            ["option_2"],
            ["option_2"],
        ]
        assert new_class.TypeThinDefaultConfig.class_enum_def.one == 12345
        assert new_class.TypeThinDefaultConfig.class_enum_def.two == 'abcdef'

    def test_raise_multiples(self, arg_builder):
        evolve_nested_stuff = EvolveNestedStuff(
            one=12345, two='abcdef'
        )
        evolve_nested_stuff_2 = EvolveNestedStuff(
            one=123456, two='abcdefg'
        )
        with pytest.raises(_SpockEvolveError):
            new_class = arg_builder.evolve(evolve_nested_stuff, evolve_nested_stuff_2)

    def test_raise_not_input(self, arg_builder):
        evolve_not_evolved = NotEvolved(one=100)
        with pytest.raises(_SpockEvolveError):
            new_class = arg_builder.evolve(evolve_not_evolved)

    def test_2_dict(self, arg_builder):
        evolve_nested_stuff = EvolveNestedStuff(
            one=12345, two='abcdef'
        )
        evolve_type_config = TypeThinDefaultConfig(
            bool_p_set_def=False,
            int_p_def=16,
            float_p_def=16.0,
            string_p_def="Spocked",
            list_p_float_def=[16.0, 26.0],
            list_p_int_def=[16, 26],
            list_p_str_def=["Spocked", "Packaged"],
            list_p_bool_def=[False, True],
            tuple_p_float_def=(16.0, 26.0),
            tuple_p_int_def=(16, 26),
            tuple_p_str_def=("Spocked", "Packaged"),
            tuple_p_bool_def=(False, True),
            choice_p_str_def="option_1",
            list_choice_p_str_def=["option_2"],
            list_list_choice_p_str_def=[["option_2"], ["option_2"]]
        )
        # Evolve the class
        new_class = arg_builder.evolve(evolve_nested_stuff, evolve_type_config)
        assert isinstance(arg_builder.spockspace_2_dict(new_class), dict) is True



