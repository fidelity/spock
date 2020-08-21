# -*- coding: utf-8 -*-

from spock.backend.dataclass.args import IntOptArg, ListOptArg
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
    # new_choice: Optional[Choice]
    fix_me: Tuple[Tuple[int]]
    # new: int
    # fail: List
    # fail: List[int]
    # fail: List[List[int]]
    # save_path: SavePath = '/tmp'
    # other: Optional[int]
    # value: Optional[List[int]] = [1, 2]

@spock
class Test2:
    new_other: int


@spock
class Test3(Test2, Test):
    ccccombo_breaker: int


def main():
    # test = Test()
    attrs_class = ConfigArgBuilder(Test).generate()
    print(attrs_class)
    # dc_class = ConfigArgBuilder(Test2).save(user_specified_path='/tmp', file_extension='.yaml').generate()


if __name__ == '__main__':
    main()