# -*- coding: utf-8 -*-

from spock.config import spock
from typing import List
from typing import Optional
from typing import Tuple


@spock
class Test:
    other: Optional[int]
    test: Tuple[float]
    value: List[int] = [1, 2]


def main():
    test = Test(test=(1.0, 2.0))
    print("Hi Mom")


if __name__ == '__main__':
    main()