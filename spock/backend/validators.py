# -*- coding: utf-8 -*-

# Copyright FMR LLC <opensource@fidelity.com>
# SPDX-License-Identifier: Apache-2.0

"""Handles custom attr validators"""

import os
from pathlib import Path
from typing import Any, List, NewType, Tuple, Type, Union

import attr

from spock.backend.custom import _C, _T, directory, file


def _check_instance(value: Any, name: str, type: type) -> None:
    """Mimics instance_of validator from attrs library

    Args:
        value: current value
        name: attribute name
        type: type to test against

    Raises:
        TypeError: if instance is not of the correct type

    Returns:
        None

    """
    if not isinstance(value, type):
        raise TypeError(
            f"{name} must be {type} (got {value} that is "
            f"{value.__class__.__name__})"
        )


def _is_file(type: _T, check_access: bool, attr: attr.Attribute, value: str) -> None:
    """Checks to verify that a file exists and if flagged that there are correct
    permissions on the file

    Private version of the method

    Args:
        type: type to test against
        check_access: checks if r/w on file
        attr: current attribute being validated
        value: current value trying to be set as the attribute

    Raises:
        ValueError: If the file path is not a valid file
        PermissionError: If the file does not have r/w permissions

    Returns:
        None

    """
    # Check the instance type first
    _check_instance(value, attr.name, str)
    # # If so then cast to underlying type
    # value = file(value)
    if not Path(value).resolve().is_file():
        raise ValueError(f"{attr.name} must be a file: {value} is not a valid file")
    r = os.access(value, os.R_OK)
    w = os.access(value, os.W_OK)
    if check_access and (not r or (not w)):
        raise PermissionError(
            f"{attr.name}: Missing correct permissions on the "
            f"directory at {value} - (read:{r}, write: {w})"
        )


@attr.attrs(repr=False, slots=True, hash=True)
class _IsFileValidator:
    """Attr style validator for checking if a path is a file

    Attributes:
        type: current type to check against
        check_access: flag to check r/w permissions

    """

    type = attr.attrib()
    check_access = attr.attrib()

    def __call__(self, inst: _C, attr: attr.Attribute, value: str) -> None:
        """Overloading call method

        Args:
            inst: current class object being built
            attr: current attribute being validated
            value: current value trying to be set as the attribute

        Returns:
            None

        """
        _is_file(self.type, check_access=self.check_access, attr=attr, value=value)

    def __repr__(self) -> str:
        return "<is_file validator>"


def is_file(type: _T, check_access: bool = True) -> _IsFileValidator:
    """A validator that raises exceptions if the file path isn't a valid file or if
    missing correct r/w privs

    Args:
        type: current type to check against
        check_access: flag to check r/w permissions

    Returns:
        _IsFileValidator object

    """
    return _IsFileValidator(type, check_access)


def _is_directory(
    type: _T, create: bool, check_access: bool, attr: attr.Attribute, value: str
) -> None:
    """

    Args:
        type: type to test against
        create:
        check_access: checks if r/w on directory
        attr: current attribute being validated
        value: current value trying to be set as the attribute

    Raises:
        ValueError: if the given path isn't a directory
        PermissionError: if the given path cannot be created or if missing the
        correct r/w permissions

    Returns:
        None

    """
    # Check the instance type first
    _check_instance(value, attr.name, str)
    # If it's not a path and not flagged to create then raise exception
    if not Path(value).resolve().is_dir() and not create:
        raise ValueError(
            f"{attr.name} must be a directory: {value} is not a " f"valid directory"
        )
    # Else just try and create the path -- exist_ok means if the path already exists
    # it won't throw an exception
    elif not Path(value).resolve().is_dir() and create:
        try:
            os.makedirs(value, exist_ok=True)
            print(
                f"{attr.name} - Created directory at {value} as it did not exist "
                f"(is_directory validator create=True)"
            )
        except Exception as e:
            raise PermissionError(f"Not able to create a directory at {value}: {e}")
    # If check access -- then make sure one can read/write within the directory
    r = os.access(value, os.R_OK)
    w = os.access(value, os.W_OK)
    if check_access and (not r or (not w)):
        raise PermissionError(
            f"{attr.name}: Missing correct permissions on the "
            f"directory at {value} - (read:{r}, write: {w})"
        )


@attr.attrs(repr=False, slots=True, hash=True)
class _IsDirectoryValidator:
    """Attr style validator for checking if a path is a directory

    Attributes:
        type: current type to check against
        create: flag to attempt to create directory if it doesn't exist
        check_access: flag to check r/w permissions

    """

    type = attr.attrib()
    create = attr.attrib()
    check_access = attr.attrib()

    def __call__(self, inst: _C, attr: attr.Attribute, value: str) -> None:
        """Overloading call method

        Args:
            inst: current class object being built
            attr: current attribute being validated
            value: current value trying to be set as the attribute

        Returns:
            None

        """
        _is_directory(
            self.type,
            create=self.create,
            check_access=self.check_access,
            attr=attr,
            value=value,
        )

    def __repr__(self) -> str:
        return f"<is_directory validator with create={self.create}>"


def is_directory(
    type: _T, create: bool = True, check_access: bool = True
) -> _IsDirectoryValidator:
    """A validator that raises exceptions if the path isn't a valid directory, if
    missing correct r/w privs, or if the directory cannot be created

    Args:
        type: current type to check against
        create: flag to attempt to create directory if it doesn't exist
        check_access: flag to check r/w permissions

    Returns:
        _IsDirectoryValidator object

    """
    return _IsDirectoryValidator(type, create, check_access)


@attr.attrs(repr=False, slots=True, hash=True)
class _InstanceOfValidator:
    """Attr style validator for handling instance checks

    This handles the underlying new types (directory and path) that type check
    in a different manner than normal -- thus we essentially shim the underlying attr
    validator with our own to catch the extra cases we need to

    Attributes:
        type: current type to check against

    """

    type = attr.attrib()

    def __call__(self, inst: _C, attr: attr.Attribute, value: Any) -> None:
        """Overloading call method

        Args:
            inst: current class object being built
            attr: current attribute being validated
            value: current value trying to be set as the attribute

        Returns:
            None

        """
        # Catch directory type -- tuples suck, so we need to handle them with their own
        # condition here -- basically if the tuple is of type directory then we need
        # to validate on the dir instance
        if (
            isinstance(self.type, type) and self.type.__name__ == directory.__name__
        ) or (
            isinstance(self.type, tuple)
            and hasattr(self.type[0], "__name__")
            and self.type[0].__name__ == "directory"
        ):
            return _is_directory(
                self.type, create=True, check_access=True, attr=attr, value=value
            )
        # Catch the file type -- tuples suck, so we need to handle them with their own
        # condition here -- basically if the tuple is of type directory then we need
        # to validate on the dir instance
        elif (isinstance(self.type, type) and self.type.__name__ == file.__name__) or (
            isinstance(self.type, tuple)
            and hasattr(self.type[0], "__name__")
            and self.type[0].__name__ == "file"
        ):
            return _is_file(type=self.type, check_access=True, attr=attr, value=value)
        # Fallback on base attr
        else:
            return _check_instance(value=value, name=attr.name, type=self.type)

    def __repr__(self) -> str:
        return f"<custom instance_of validator for type {self.type}>"


def instance_of(type: _T) -> _InstanceOfValidator:
    """A validator that verifies that the type is correct

    Args:
        type: current type to check against

    Returns:
        class of _InstanceOfValidator

    """
    return _InstanceOfValidator(type=type)


@attr.attrs(repr=False, slots=True, hash=True)
class _IsLenValidator:
    """Attr style validator for handling exact length checks

    Attributes:
        length: length value to check against

    """

    length = attr.attrib()

    def __call__(
        self, inst: _C, attr: attr.Attribute, value: Union[List, Tuple]
    ) -> None:
        """Overloading call method

        Args:
            inst: current class object being built
            attr: current attribute being validated
            value: current value trying to be set as the attribute

        Returns:
            None

        """
        # Check that the lengths strictly match
        if len(value) != self.length:
            raise ValueError(
                f"{attr.name} was defined to require {self.length} values but was "
                f"provided with {len(value)}"
            )

    def __repr__(self) -> str:
        return f"<len validator for length of {self.length}>"


def is_len(length: int):
    """A validator that makes sure the input length matches what was specified

    Args:
        length: length value to check against

    Returns:

    """
    return _IsLenValidator(length=length)


@attr.attrs(repr=False, slots=True, hash=True)
class _OrderedIsInstanceDeepIterable:
    """Attr style validator for handling instance checks in a deep iterable that is
    ordered

    This handles creating instance validators for deep iterables that have an ordered
    nature -- mainly tuples. Since we need to march in the correct order of the given
    types we have to overload the IsInstance class with new one that handles recursing
    on its own

    Attributes:
        ordered_types: ordered iterator of the requested types
        recurse_callable: callable function that allows for recursing to create
        validators in the deep iterable object
        iterable_validator: validator on the iterable

    """

    ordered_types = attr.attrib()
    recurse_callable = attr.attrib(validator=attr.validators.is_callable())
    iterable_validator = attr.attrib(
        default=None, validator=attr.validators.optional(attr.validators.is_callable())
    )

    def __call__(
        self, inst: _C, attr: attr.Attribute, value: Union[List[Type], Tuple[Type, ...]]
    ):
        """Overloading call method

        Args:
            inst: current class object being built
            attr: current attribute being validated
            value: current value trying to be set as the attribute

        Returns:
            None

        """

        validator_list = [self.recurse_callable(val) for val in self.ordered_types]
        value_tuple = tuple(zip(value, validator_list))

        if self.iterable_validator is not None:
            self.iterable_validator(inst, attr, value)

        for member, validator in value_tuple:
            validator(inst, attr, member)

    def __repr__(self):

        return (
            f"<ordered is instance deep_iterable validator for types "
            f"{self.ordered_types}>"
        )


def ordered_is_instance_deep_iterable(
    ordered_types: Tuple[Type, ...],
    recurse_callable,
    iterable_validator,
):
    """A validator that makes sure the deep iterable matches the requested types in the
    given order

    Args:
        ordered_types: ordered iterator of the requested types
        recurse_callable: callable function that allows for recursing to create
        validators in the deep iterable object
        iterable_validator: validator on the iterable

    Returns:

    """
    return _OrderedIsInstanceDeepIterable(
        ordered_types, recurse_callable, iterable_validator
    )


def _in_type(instance, attribute, value, options):
    """attrs validator for class type enum

    Checks if the type of the class (e.g. value) is in the specified set of types
    provided. Also checks if the value
    is specified via the Enum definition

    Args:
        instance: current object instance
        attribute: current attribute instance
        value: current value trying to be set in the attrs instance
        options: list, tuple, or enum of allowed options

    Returns:
    """
    if type(value) not in options:
        raise ValueError(f"{attribute.name} must be in {options}")
