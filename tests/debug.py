# -*- coding: utf-8 -*-

from spock.attr_backend.typed import katra, SpockTypes
from spock.config import spock


@spock
class Test:
    other = katra(SpockTypes.BOOL)
    value = katra(typed=SpockTypes.LIST, default=[1, 2.0])


def main():
    test = Test()
    print("Hi Mom")

if __name__ == '__main__':
    main()