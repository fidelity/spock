# -*- coding: utf-8 -*-

# Copyright 2019 FMR LLC <opensource@fidelity.com>
# SPDX-License-Identifier: Apache-2.0

"""Handles the definitions of arguments types for Spock"""

from typing import List
from typing import Tuple
from typing import TypeVar
from spock.utils import _def_list
from spock.utils import _def_tuple


class BoolArg(int):
    """Spock boolean argument

    Overloads the bool type for Spock

    """
    def __new__(cls, x):
        """Creates a new instance of a Spock boolean arg

        *Args*:

            x: boolean value

        *Returns*:

            boolean variable
        """
        return super().__new__(cls, bool(x))


class IntArg(int):
    """Spock integer argument

    Overloads the integer type for Spock

    """
    def __new__(cls, x):
        """Creates a new instance of a Spock integer arg

        *Args*:

            x: integer value

        *Returns*:

            integer variable
        """
        return super().__new__(cls, x)


class IntOptArg(int):
    """Spock integer optional argument

    Overloads the integer type and makes the argument optional for Spock

    """
    def __new__(cls, x):
        """Creates a new instance of a Spock optional integer arg

        *Args*:

            x: integer value

        *Returns*:

            integer variable
        """
        return super().__new__(cls, x)


class FloatArg(float):
    """Spock float argument

    Overloads the float type for Spock

    """
    def __new__(cls, x):
        """Creates a new instance of a Spock float arg

        *Args*:

            x: float value

        *Returns*:

            float variable
        """
        return super().__new__(cls, x)


class FloatOptArg(float):
    """Spock float optional argument

    Overloads the float type and makes the argument optional for Spock

    """
    def __new__(cls, x):
        """Creates a new instance of a Spock float optional arg

        *Args*:

            x: float value

        *Returns*:

            float variable
        """
        return super().__new__(cls, x)


class StrArg(str):
    """Spock string argument

    Overloads the string type  for Spock

    """
    def __new__(cls, x):
        """Creates a new instance of a Spock string arg

        *Args*:

            x: string value

        *Returns*:

            string variable
        """
        return super().__new__(cls, x)


class StrOptArg(str):
    """Spock string optional argument

    Overloads the string type and makes the argument optional for Spock

    """
    def __new__(cls, x):
        """Creates a new instance of a Spock string optional arg

        *Args*:

            x: string value

        *Returns*:

            string variable
        """
        return super().__new__(cls, x)


# Make a type var
__T = TypeVar('__T')


class ListArg(List[__T]):  # pylint: disable=too-few-public-methods
    """Spock list argument

    Overloads the list type for Spock

    """
    @staticmethod
    def defaults(values: List):
        """Creates a new instance of a Spock list arg

        *Args*:

            values: list values

        *Returns*:

            list variable
        """
        return _def_list(values)


class ListOptArg(List[__T]):  # pylint: disable=too-few-public-methods
    """Spock list optional argument

    Overloads the list type and makes the argument optional for Spock

    """
    @staticmethod
    def defaults(values: List):
        """Creates a new instance of a Spock list optional arg

        *Args*:

            values: list values

        *Returns*:

            list variable
        """
        return _def_list(values)


class TupleArg(Tuple[__T]):  # pylint: disable=too-few-public-methods
    """Spock tuple argument

    Overloads the tuple type for Spock

    """
    @staticmethod
    def defaults(values: Tuple):
        """Creates a new instance of a Spock tuple arg

        *Args*:

            values: tuple values

        *Returns*:

            tuple variable
        """
        return _def_tuple(values)


class TupleOptArg(Tuple[__T]):  # pylint: disable=too-few-public-methods
    """Spock tuple optional argument

    Overloads the tuple type and makes the argument optional for Spock

    """
    @staticmethod
    def defaults(values: Tuple):
        """Creates a new instance of a Spock tuple optional arg

        *Args*:

            values: tuple values

        *Returns*:

            tuple variable
        """
        return _def_tuple(values)


class ChoiceArg:  # pylint: disable=too-few-public-methods
    """Spock type of a choice set

    Requires defaults or file values to be from a predefined set

    """
    def __init__(self, choice_set: List, default=None):
        self.choice_set = choice_set
        self.default = default
        self.set_type = self._verify()

    def _verify(self):
        """Validates the types within a set

        *Returns*:

            str name of type

        """
        type_set = {type(val) for val in self.choice_set}
        if len(type_set) > 1:
            raise TypeError(f'ChoiceArg must all be of the same type: {type_set}')
        return list(type_set)[0]


class SavePathOptArg(str):
    """Spock special key for saving the Spock config to file

    Defines a special key use to save the current Spock config to file

    """
    def __new__(cls, x):
        return super().__new__(cls, x)


def boolean_string(bool_string):
    """Map boolean string to boolean type

    *Args*:

        s: boolean string

    *Returns*:

        string True/False to actual bool type

    """
    if bool_string not in {'False', 'True'}:
        raise ValueError('Not a valid boolean string')
    return bool_string == 'True'
