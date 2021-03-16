# -*- coding: utf-8 -*-
from enum import Enum
from spock.config import spock
from typing import List
from typing import Tuple


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
class Test:
    """High level docstring that just so happens to be multiline adfjads;lfja;sdlkjfklasjflkasjlkfjal;sdfjlkajsdfl;kja
    adfasfdsafklasdjfkladsjklfasdjlkf

    Mid-level docstring

    Attributes:
        fail: help me obi wan
        test: you are my only hopes
        most_broken: class stuff enum
        new_choice: choice type optionality

    """
    new_choice: Choice
    fail: Tuple[Tuple[int, int], Tuple[int, int]]
    test: List[int] = [1, 2]
    most_broken: ClassStuff
