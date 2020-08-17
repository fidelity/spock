# -*- coding: utf-8 -*-

from spock.backend.dataclass.args import IntOptArg, ListOptArg
from spock.config import spock
from spock.config import spock_config
from typing import List
from typing import Optional
from spock.builder import ConfigArgBuilder

@spock
class Test:
    other: Optional[int]
    value: Optional[List[int]]


@spock_config
class Test2:
    other: IntOptArg
    value: ListOptArg


def main():
    # test = Test()
    # attrs_class = ConfigArgBuilder(Test).save(user_specified_path='/tmp/', file_extension='.yaml').generate()
    dc_class = ConfigArgBuilder(Test2).save(user_specified_path='/tmp', file_extension='.yaml').generate()


if __name__ == '__main__':
    main()