# -*- coding: utf-8 -*-
from enum import Enum
from spock.config import spock
from typing import List
from typing import Tuple
from typing import Optional
from .second import Choice

#
class Choice(Enum):
    """Blah

    Attributes:
        pear: help pears
        banana: help bananas

    """
    pear = 'pear'
    banana = 'banana'


@spock
class OtherStuff:
    """Other stuff class

    Attributes:
        three: heahadsf
        four: asdfjhasdlkf

    """
    three: int
    four: str


@spock
class Stuff:
    """Stuff class

    Attributes:
        one: help
        two: teadsfa

    """
    one: int
    two: str


class ClassStuff(Enum):
    """Class enum

    Attributes:
        other_stuff: OtherStuff class
        stuff: Stuff class

    """
    other_stuff = OtherStuff
    stuff = Stuff


@spock
class NestedListStuff:
    """Class enum

    Attributes:
        maybe: some val
        more: some other value

    """
    maybe: int
    more: str


@spock
class Test:
    """High level docstring that just so happens to be multiline adfjads;lfja;sdlkjfklasjflkasjlkfjal;sdfjlkajsdfl;kja
    adfasfdsafklasdjfkladsjklfasdjlkf

    Mid-level docstring

    Attributes:
        fail: help me obi wan
        test: you are my only hopes
        most_broken: class stuff enum
        new_choice: choice type optionality
        one: just a basic parameter
        nested_list: Repeated list of a class type
    """
    # new_choice: Choice
    # fail: Tuple[Tuple[int, int], Tuple[int, int]]
    test: List[int]
    # fail: List[List[int]]
    # flipper: bool
    # most_broken: ClassStuff
    # one: int
    nested_list: List[NestedListStuff]

