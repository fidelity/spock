# -*- coding: utf-8 -*-

from spock.backend.dataclass.args import IntOptArg, ListOptArg
from spock.config import spock
from spock.config import spock_config
from typing import List
from typing import Optional
from enum import Enum
from spock.builder import ConfigArgBuilder


class Choice(Enum):
    pear = 'pear'
    banana = 'banana'


@spock
class Test:
    # new_choice: Optional[Choice]
    # new: int
    # fail: List
    # fail: List[int]
    fail: List[List[int]]
    # other: Optional[int]
    value: Optional[List[int]] = [1, 2]


@spock_config
class Test2:
    other: IntOptArg
    value: ListOptArg


def main():
    # test = Test()
    attrs_class = ConfigArgBuilder(Test).generate()
    print(attrs_class)
    # dc_class = ConfigArgBuilder(Test2).save(user_specified_path='/tmp', file_extension='.yaml').generate()


if __name__ == '__main__':
    main()
