# -*- coding: utf-8 -*-

# Copyright FMR LLC <opensource@fidelity.com>
# SPDX-License-Identifier: Apache-2.0

"""Utility functions for Spock"""

import ast
import os
import random
import socket
import subprocess
import sys
from argparse import _ArgumentGroup
from enum import EnumMeta
from math import isclose
from pathlib import Path
from time import localtime, strftime
from typing import Any, Dict, List, Tuple, Type, TypeVar, Union
from warnings import warn

import attr
import git
import pkg_resources

from spock.exceptions import _SpockValueError

minor = sys.version_info.minor


def make_salt(salt_len: int = 16):
    """Make a salt of specific length

    Args:
        salt_len: length of the constructed salt

    Returns:
        salt string

    """
    alphabet = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    return "".join(random.choice(alphabet) for _ in range(salt_len))


def _get_alias_type():
    """Gets the correct type of GenericAlias for versions less than 3.6

    Returns:
        _GenericAlias type

    """
    if minor < 7:
        from typing import GenericMeta as _GenericAlias
    else:
        from typing import _GenericAlias

    return _GenericAlias


def _get_callable_type():
    """Gets the correct underlying type reference for callable objects depending on the python version

    Returns:
        _VariadicGenericAlias type

    """
    if minor == 6:
        from typing import CallableMeta as _VariadicGenericAlias
    elif (minor > 6) and (minor < 9):
        from typing import _VariadicGenericAlias
    elif minor > 8:
        from typing import _CallableType as _VariadicGenericAlias
    else:
        raise RuntimeError(
            f"Attempting to use spock with python version `3.{minor}` which is unsupported"
        )
    return _VariadicGenericAlias


_SpockGenericAlias = _get_alias_type()
_SpockVariadicGenericAlias = _get_callable_type()
_T = TypeVar("_T")
_C = TypeVar("_C", bound=type)


def _filter_optional(val: List, allow_optional: bool = True):
    """Filters an iterable for None values if they are allowed

    Args:
        val: iterable of values that might contain None
        allow_optional: allows the check to succeed if a given val in the iterable is None

    Returns:
        filtered list of values with None values removed

    Raises:
        _SpockValueError

    """
    filtered_val = []
    for idx, v in enumerate(val):
        if v is None and not allow_optional:
            raise _SpockValueError(
                f"Optional values not allowed -- encountered None value in position `{idx}` of the iterable"
            )
        elif v is not None:
            filtered_val.append(v)
    return filtered_val


def sum_vals(
    val: List[Union[float, int, None]],
    sum_val: Union[float, int],
    allow_optional: bool = True,
    rel_tol: float = 1e-9,
    abs_tol: float = 0.0,
):
    """Checks if an iterable of values sums within tolerance to a specified value

    Args:
        val: iterable of values to sum
        sum_val: sum value to compare against
        allow_optional: allows the check to succeed if a given val in the iterable is None
        rel_tol: relative tolerance – it is the maximum allowed difference between a and b
        abs_tol: the minimum absolute tolerance – useful for comparisons near zero

    Returns:
        None

    Raises:
        _SpockValueError

    """
    filtered_val = _filter_optional(val, allow_optional)
    if not isclose(sum(filtered_val), sum_val, rel_tol=rel_tol, abs_tol=abs_tol):
        raise _SpockValueError(
            f"Sum of iterable is `{sum(filtered_val)}` which is not equal to specified value `{sum_val}` within given tolerances"
        )


def eq_len(val: List[Union[Tuple, List, None]], allow_optional: bool = True):
    """Checks that all values passed in the iterable are of the same length

    Args:
        val: iterable to compare lengths
        allow_optional: allows the check to succeed if a given val in the iterable is None

    Returns:
        None

    Raises:
        _SpockValueError

    """
    filtered_val = _filter_optional(val, allow_optional)
    # just do a set comprehension -- iterables shouldn't be that long so pay the O(n) price
    lens = {len(v) for v in filtered_val}
    if len(lens) != 1:
        raise _SpockValueError(
            f"Length mismatch -- current lengths of values within the iterable are `{lens}`"
        )


def within(
    val: Union[float, int, None],
    low_bound: Union[float, int],
    upper_bound: Union[float, int],
    inclusive_lower: bool = False,
    inclusive_upper: bool = False,
    allow_optional: bool = True,
) -> None:
    """Checks that a value is within a defined range

    Args:
        val: value to check against
        low_bound: lower bound of range
        upper_bound: upper bound of range
        inclusive_lower: if the check includes the bound value (i.e. >=)
        inclusive_upper: if the check includes the bound value (i.e. <=)
        allow_optional: allows the check to succeed if val is none

    Returns:
        None

    Raises:
        _SpockValueError

    """
    # Skip if None and allowed
    if allow_optional and val is None:
        pass
    elif val is None and not allow_optional:
        raise _SpockValueError(
            f"Set value is None and allow_optional is `{allow_optional}`"
        )
    else:
        # Check lower bounds
        lower_fn = le if inclusive_upper else lt
        upper_fn = ge if inclusive_lower else gt
        upper_fn(val=val, bound=low_bound, allow_optional=allow_optional)
        lower_fn(val=val, bound=upper_bound, allow_optional=allow_optional)


def ge(
    val: Union[float, int, None], bound: Union[float, int], allow_optional: bool = True
) -> None:
    """Checks that a value is greater than or equal to (inclusive) a lower bound

    Args:
        val: value to check against
        bound: lower bound
        allow_optional: allows the check to succeed if val is none

    Returns:
        None

    Raises:
        _SpockValueError

    """
    # Skip if None and allowed
    if allow_optional and val is None:
        pass
    elif val is None and not allow_optional:
        raise _SpockValueError(
            f"Set value is None and allow_optional is `{allow_optional}`"
        )
    else:
        if val < bound:
            raise _SpockValueError(
                f"Set value `{val}` is not >= given bound value `{bound}`"
            )


def gt(
    val: Union[float, int, None], bound: Union[float, int], allow_optional: bool = True
) -> None:
    """Checks that a value is greater (non-inclusive) than a lower bound

    Args:
        val: value to check against
        bound: lower bound
        allow_optional: allows the check to succeed if val is none

    Returns:
        None

    Raises:
        _SpockValueError

    """
    # Skip if None and allowed
    if allow_optional and val is None:
        pass
    elif val is None and not allow_optional:
        raise _SpockValueError(
            f"Set value is None and allow_optional is `{allow_optional}`"
        )
    else:
        if val <= bound:
            raise _SpockValueError(
                f"Set value `{val}` is not > given bound value `{bound}`"
            )


def le(
    val: Union[float, int, None], bound: Union[float, int], allow_optional: bool = True
) -> None:
    """Checks that a value is less than or equal to (inclusive) an upper bound

    Args:
        val: value to check against
        bound: upper bound
        allow_optional: allows the check to succeed if val is none

    Returns:
        None

    Raises:
        _SpockValueError

    """
    # Skip if None and allowed
    if allow_optional and val is None:
        pass
    elif val is None and not allow_optional:
        raise _SpockValueError(
            f"Set value is None and allow_optional is `{allow_optional}`"
        )
    else:
        if val > bound:
            raise _SpockValueError(
                f"Set value `{val}` is not <= given bound value `{bound}`"
            )


def lt(
    val: Union[float, int], bound: Union[float, int], allow_optional: bool = True
) -> None:
    """Checks that a value is less (non-inclusive) than an upper bound

    Args:
        val: value to check against
        bound: upper bound
        allow_optional: allows the check to succeed if val is none

    Returns:
        None

    Raises:
        _SpockValueError

    """
    # Skip if None and allowed
    if allow_optional and val is None:
        pass
    elif val is None and not allow_optional:
        raise _SpockValueError(
            f"Set value is None and allow_optional is `{allow_optional}`"
        )
    else:
        if val >= bound:
            raise _SpockValueError(
                f"Set value `{val}` is not < given bound value `{bound}`"
            )


def _find_all_spock_classes(attr_class: _C) -> List:
    """Within a spock class determine if there are any references to other spock classes

    Args:
        attr_class: a class with attrs attributes

    Returns:
        list of dependent spock classes

    """
    # Get the top level dict
    dict_attr = attr.fields_dict(attr_class)
    # Dependent classes
    dep_classes = []
    for k, v in dict_attr.items():
        # Checks for direct spock/attrs instance
        if _is_spock_instance(v.type):
            dep_classes.append(v.type)
        # Check for enum of spock/attrs instance
        elif isinstance(v.type, EnumMeta) and _check_4_spock_iterable(v.type):
            dep_classes.extend(_get_enum_classes(v.type))
        # Check for List[@spock-class] -- needs to be checked against 3.6 typing.List as well
        elif ((v.type is list) or (v.type is List)) and _is_spock_instance(
            v.metadata["type"].__args__[0]
        ):
            dep_classes.append(v.metadata["type"].__args__[0])
    return dep_classes


def _check_4_spock_iterable(iter_obj: Union[Tuple, List]) -> bool:
    """Checks if an iterable type contains a spock class

    Args:
        iter_obj: iterable type

    Returns:
        boolean if the iterable contains at least one spock class

    """
    return _check_iterable(iter_obj=iter_obj)


def _get_enum_classes(enum_obj: EnumMeta) -> List:
    """Checks if any of the values of an enum are spock classes and adds to a list

    Args:
        enum_obj: enum class

    Returns:
        list of enum values that are spock classes

    """
    return [v.value for v in enum_obj if _is_spock_instance(v.value)]


def path_object_to_s3path(path: Path) -> str:
    """Convert a path object into a string s3 path

    Args:
        path: a spock config path

    Returns:
        string of s3 path

    """
    return path.parts[0] + "//" + "/".join(path.parts[1:])


def check_path_s3(path: Path) -> bool:
    """Checks the given path to see if it matches the s3:// regex

    Args:
        path: a spock config path

    Returns:
        boolean of regex match

    """
    return len(path.parts) > 1 and path.parts[0] == "s3:"


def _is_spock_instance(__obj: object) -> bool:
    """Checks if the object is a @spock decorated class

    Private interface that checks to see if the object passed in is registered within the spock module and also
    is a class with attrs attributes (__attrs_attrs__)

    Args:
        __obj: class to inspect

    Returns:
        bool

    """
    return attr.has(__obj) and (__obj.__module__ == "spock.backend.config")


def _is_spock_tune_instance(__obj: object) -> bool:
    """Checks if the object is a @spock decorated class

    Private interface that checks to see if the object passed in is registered within the spock module tune addon and also
    is a class with attrs attributes (__attrs_attrs__)

    Args:
        __obj: class to inspect

    Returns:
        bool

    """
    return attr.has(__obj) and (__obj.__module__ == "spock.addons.tune.config")


def _check_iterable(iter_obj: Union[Tuple, List, EnumMeta]) -> bool:
    """Check if an iterable type contains a spock class

    Args:
        iter_obj: iterable type

    Returns:
        boolean if the iterable contains at least one spock class

    """
    return any([_is_spock_instance(v.value) for v in iter_obj])


def make_argument(
    arg_name: str, arg_type: _T, parser: Type[_ArgumentGroup]
) -> _ArgumentGroup:
    """Make argparser argument based on type

    Based on the type passed in handle the creation of the argparser argument so that overrides will have the correct
    behavior when set

    Args:
        arg_name: name for the argument
        arg_type: type of the argument
        parser: current parser

    Returns:
        parser: updated argparser

    """
    # For generic alias we take the input string and use a custom type callable to convert
    if isinstance(arg_type, _SpockGenericAlias):
        parser.add_argument(arg_name, required=False, type=_handle_generic_type_args)
    # For Unions -- python 3.6 can't deal with them correctly -- use the same ast method that generics require
    elif (
        hasattr(arg_type, "__origin__")
        and (arg_type.__origin__ is Union)
        and (minor < 7)
    ):
        parser.add_argument(arg_name, required=False, type=_handle_generic_type_args)
    # For choice enums we need to check a few things first
    elif isinstance(arg_type, EnumMeta):
        type_set = list({type(val.value) for val in arg_type})[0]
        # if this is an enum of a class switch the type to str as this is how it gets matched
        type_set = str if type_set.__name__ == "type" else type_set
        parser.add_argument(arg_name, required=False, type=type_set)
    # For booleans we map to store true
    elif arg_type == bool:
        parser.add_argument(arg_name, required=False, action="store_true")
    # Else we are a simple base type which we can cast to
    else:
        parser.add_argument(arg_name, required=False, type=arg_type)
    return parser


def _handle_generic_type_args(val: str) -> Any:
    """Evaluates a string containing a Python literal

    Seeing a list and tuple types will come in as string literal format, use ast to get the actual type

    Args:
        val: string literal

    Returns:
        the underlying string literal type

    """
    return ast.literal_eval(val)


def get_packages() -> Dict:
    """Gets all currently installed packages and assembles a dictionary of name: version

    Notes:
        https://stackoverflow.com/a/50013400

    Returns:
        dictionary of all currently available packages

    """
    named_list = sorted([str(i.key) for i in pkg_resources.working_set])
    return {
        f"# {i}": str(pkg_resources.working_set.by_key[i].version) for i in named_list
    }


def add_info() -> Dict:
    """Adds extra information to the output dictionary

    Args:

    Returns:
        out_dict: output dictionary
    """
    out_dict = {}
    out_dict = add_generic_info(out_dict)
    out_dict = add_repo_info(out_dict)
    return out_dict


def make_blank_git(out_dict: Dict) -> Dict:
    """Adds blank git info

    Args:
        out_dict: current output dictionary

    Returns:
        out_dict: output dictionary with added git info

    """
    for key in ("BRANCH", "COMMIT SHA", "STATUS", "ORIGIN"):
        out_dict.update({f"# Git {key}": "UNKNOWN"})
    return out_dict


def add_repo_info(out_dict: Dict) -> Dict:
    """Adds GIT information to the output dictionary

    Args:
        out_dict: output dictionary

    Returns:
        out_dict: output dictionary
    """
    try:  # pragma: no cover
        # Assume we are working out of a repo
        repo = git.Repo(os.getcwd(), search_parent_directories=True)
        # Check if we are really in a detached head state as later info will fail if we are
        if minor < 7:
            head_result = subprocess.run(
                "git rev-parse --abbrev-ref --symbolic-full-name HEAD",
                stdout=subprocess.PIPE,
                shell=True,
                check=False,
            )
        else:
            head_result = subprocess.run(
                "git rev-parse --abbrev-ref --symbolic-full-name HEAD",
                capture_output=True,
                shell=True,
                check=False,
            )
        if head_result.stdout.decode().rstrip("\n") == "HEAD":
            out_dict = make_blank_git(out_dict)
        else:
            out_dict.update({"# Git Branch": repo.active_branch.name})
            out_dict.update({"# Git Commit": repo.active_branch.commit.hexsha})
            out_dict.update(
                {"# Git Date": repo.active_branch.commit.committed_datetime}
            )
            if (
                len(repo.untracked_files) > 0
                or len(repo.active_branch.commit.diff(None)) > 0
            ):
                git_status = "DIRTY"
            else:
                git_status = "CLEAN"
            out_dict.update({"# Git Status": git_status})
            out_dict.update(
                {"# Git Origin": repo.active_branch.commit.repo.remotes.origin.url}
            )
    except git.InvalidGitRepositoryError:  # pragma: no cover
        # But it's okay if we are not
        out_dict = make_blank_git(out_dict)
    return out_dict


def add_generic_info(out_dict: Dict) -> Dict:
    """Adds date, fqdn information to the output dictionary

    Args:
        out_dict: output dictionary

    Returns:
        out_dict: output dictionary
    """
    out_dict.update({"# Machine FQDN": socket.getfqdn()})
    out_dict.update({"# Python Executable": sys.executable})
    out_dict.update(
        {
            "# Python Version": f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
        }
    )
    out_dict.update({"# Python Script": os.path.realpath(sys.argv[0])})
    out_dict.update({"# Run Date": strftime("%Y-%m-%d", localtime())})
    out_dict.update({"# Run Time": strftime("%H:%M:%S", localtime())})
    # Make a best effort to determine if run in a container
    out_dict.update({"# Run w/ Docker": str(_maybe_docker())})
    # Make a best effort to determine if run in a container via k8s
    out_dict.update({"# Run w/ Kubernetes": str(_maybe_k8s())})

    return out_dict


def _maybe_docker(cgroup_path: str = "/proc/self/cgroup") -> bool:
    """Make a best effort to determine if run in a docker container

    Args:
        cgroup_path: path to cgroup file

    Returns:
        boolean of best effort docker determination

    """
    # A few options seem to be at play here:
    # 1. Check for /.dockerenv -- docker should create this is any container
    bool_env = os.path.exists("/.dockerenv")
    # 2. Check /proc/self/cgroup for "docker"
    # https://stackoverflow.com/a/48710609
    bool_cgroup = os.path.isfile(cgroup_path) and any(
        "docker" in line for line in open(cgroup_path)
    )
    return bool_env or bool_cgroup


def _maybe_k8s(cgroup_path: str = "/proc/self/cgroup") -> bool:
    """Make a best effort to determine if run in a container via k8s

    Args:
        cgroup_path: path to cgroup file

    Returns:
        boolean of best effort k8s determination

    """
    # A few options seem to be at play here:
    # 1. Check for KUBERNETES_SERVICE_HOST -- kublet should add this to every running pod
    bool_env = os.environ.get("KUBERNETES_SERVICE_HOST") is not None
    # 2. Similar to docker check /proc/self/cgroup for "kubepods"
    # https://stackoverflow.com/a/48710609
    bool_cgroup = os.path.isfile(cgroup_path) and any(
        "kubepods" in line for line in open(cgroup_path)
    )
    return bool_env or bool_cgroup


def deep_payload_update(source: Dict, updates: Dict) -> Dict:
    """Deeply updates a dictionary

    Iterates through a dictionary recursively to update individual values within a possibly nested dictionary
    of dictionaries -- creates a dictionary if empty and trying to recurse

    Args:
        source: source dictionary
        updates: updates to the dictionary

    Returns:
        source: updated version of the source dictionary

    """

    for k, v in updates.items():
        if isinstance(v, (dict, Dict)) and v:
            source_dict = {} if source.get(k) is None else source.get(k)
            updated_dict = deep_payload_update(source_dict, v)
            if updated_dict:
                source[k] = updated_dict
        else:
            source[k] = v
    return source


def check_payload_overwrite(
    payload: Dict, updates: Dict, configs: str, overwrite: str = ""
) -> None:
    """Warns when parameters are overwritten across payloads as order will matter

    Args:
        payload: current payload
        payload_update: update to add to payload
        configs: config path
        overwrite: name of parent

    Returns:
    """
    for k, v in updates.items():
        if isinstance(v, dict) and v:
            overwrite += k + ":"
            current_payload = {} if payload.get(k) is None else payload.get(k)
            check_payload_overwrite(current_payload, v, configs, overwrite=overwrite)
        else:
            if k in payload:
                warn(
                    f"Overriding an already set parameter {overwrite + k} from {configs}\n"
                    f"Be aware that value precedence is set by the order of the config files (last to load)...",
                    SyntaxWarning,
                )
