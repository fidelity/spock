# -*- coding: utf-8 -*-
from spock.backend.dataclass.args import IntArg, ListArg, IntOptArg, ChoiceArg, SavePathOptArg
from spock.config import spock
from spock.config import spock_config
from typing import List
from typing import Optional
from typing import Tuple
from enum import Enum
from spock.builder import ConfigArgBuilder
from spock.backend.attr.typed import SavePath
import pickle
from argparse import Namespace


class Choice(Enum):
    pear = 'pear'
    banana = 'banana'


@spock
class OtherStuff:
    three: int
    four: str


@spock
class Stuff:
    one: int
    two: str


class ClassStuff(Enum):
    other_stuff = OtherStuff
    stuff = Stuff



@spock
class Test:
    # new_choice: Choice
    # # fix_me: Tuple[Tuple[int]]
    # new: int
    # # fail: bool
    # # fail: List
    # test: List[int]
    # fail: List[List[int]]
    # # borken: Stuff
    # borken: List[Stuff]
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
    attrs_class = ConfigArgBuilder(Test, OtherStuff, Stuff).generate()
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
