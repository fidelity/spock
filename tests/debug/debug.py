# -*- coding: utf-8 -*-
from spock.config import spock
from typing import List
from typing import Optional
from typing import Tuple
from enum import Enum
from spock.builder import ConfigArgBuilder
from spock.backend.attr.typed import SavePath
import pickle
from argparse import Namespace


# class Choice(Enum):
#     pear = 'pear'
#     banana = 'banana'
#
#
# class IntChoice(Enum):
#     option_1 = 10
#     option_2 = 20
#
#
@spock
class OtherStuff:
    """Other stuff class

    three: heahadsf
    four: asdfjhasdlkf

    """
    three: int
    four: str


@spock
class Stuff:
    """Stuff class

    one: help
    two: teadsfa

    """
    one: int
    two: str


class ClassStuff(Enum):
    """Class enum

    other_stuff: OtherStuff class
    stuff: Stuff class

    """
    other_stuff = OtherStuff
    stuff = Stuff

#
# @spock
# class RepeatStuff:
#     hi: int
#     bye: float


@spock
class Test:
    """High level docstring that just so happens to be multiline adfjads;lfja;sdlkjfklasjflkasjlkfjal;sdfjlkajsdfl;kja
    adfasfdsafklasdjfkladsjklfasdjlkf

    Mid-level docstring

    Attributes:
        fail: help me obi wan
        test: you are my only hopes
        most_broken: class stuff enum

    """
    # new_choice: Optional[Choice]
    # # fix_me: Tuple[Tuple[int]]
    # new: int = 3
    # fail: bool
    fail: Tuple[Tuple[int, int], Tuple[int, int]]
    test: List[int] = [1, 2]
    # fail: List[List[int]] = [[1, 2], [1, 2]]
    # borken: Stuff = Stuff
    # borken: List[RepeatStuff]
    # more_borken: OtherStuff
    most_broken: ClassStuff
    # borken: int
    # borken: Optional[List[List[Choice]]] = [['pear'], ['banana']]
    # save_path: SavePath = '/tmp'
    # other: Optional[int]
    # value: Optional[List[int]] = [1, 2]


# @spock
# class Test2:
#     new: int
#     other: int
#     fail: int
#     foo: str

#
# @spock
# class Test3(Test2, Test):
#     ccccombo_breaker: int


def main():
    attrs_class = ConfigArgBuilder(Test, Stuff, OtherStuff, desc='I am a description').generate()
    # with open('/tmp/debug.pickle', 'wb') as fid:
    #     pickle.dump(attrs_class, file=fid)

    # with open('/tmp/debug.pickle', 'rb') as fid:
    #     attrs_load = pickle.load(fid)
    # attrs_class = ConfigArgBuilder(Test, Test2).generate()

    print(attrs_class)
    # print(attrs_load)
    # dc_class = ConfigArgBuilder(OldInherit).generate()
    # print(dc_class)


if __name__ == '__main__':
    main()
