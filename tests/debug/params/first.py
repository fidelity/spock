# -*- coding: utf-8 -*-
from enum import Enum
from spock.config import spock
from typing import List
from typing import Tuple
from .second import Choice


class IntChoice(Enum):
    """Integer enum

    Attributes:
        option_1: first choice
        option_2: second choice

    """
    option_1 = 10
    option_2 = 20



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
        borken: nested choice
        new: Integer enum choice

    """
    # new_choice: Choice
    # fail: Tuple[Tuple[Choice, Choice], Tuple[Choice, Choice]]
    fail: Tuple[Tuple[Tuple[Choice], Tuple[Choice]], Tuple[Tuple[Choice], Tuple[Choice]]]
    # failed: List[List[int]]
    # test: List[int] = [1, 2]
    # most_broken: ClassStuff
    borken: List[List[Choice]] = [['pear'], ['banana']]
    new: IntChoice
