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


class Choice(Enum):
    pear = 'pear'
    banana = 'banana'


@spock
class Test:
    new_choice: Choice
    # fix_me: Tuple[Tuple[int]]
    new: int
    fail: bool
    # fail: List
    test: List[int]
    # fail: List[List[int]]
    # save_path: SavePath = '/tmp'
    # other: Optional[int]
    # value: Optional[List[int]] = [1, 2]

# @spock
# class Test2:
#     new_other: int
#
#
# @spock
# class Test3(Test2, Test):
#     ccccombo_breaker: int


def main():
    # test = Test()
    attrs_class = ConfigArgBuilder(Test).generate()
    print(attrs_class)
    # dc_class = ConfigArgBuilder(OldInherit).generate()
    # print(dc_class)


if __name__ == '__main__':
    main()
