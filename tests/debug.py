# -*- coding: utf-8 -*-

from spock.args import IntArg
from spock.config import spock
from spock.config import spock_config
from typing import List
from typing import Optional
from typing import Tuple
from spock.builder import NewConfigArgBuilder

@spock
class Test:
    other: int
    value: Optional[List[int]]


@spock_config
class Test2:
    other: IntArg = 1


def main():
    test = Test(other=1, foo=2)
    attrs_class = NewConfigArgBuilder(Test)
    dc_class = NewConfigArgBuilder(Test2)
    print("Hi Mom")


if __name__ == '__main__':
    main()