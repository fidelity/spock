# -*- coding: utf-8 -*-

# Copyright FMR LLC <opensource@fidelity.com>
# SPDX-License-Identifier: Apache-2.0

"""Utility functions for Spock"""

import ast
import os
import socket
import subprocess
import sys
from enum import EnumMeta
from pathlib import Path
from time import localtime, strftime
from typing import List, Type, Union
from warnings import warn

import attr
import git

from spock.exceptions import _SpockValueError

minor = sys.version_info.minor


def _get_alias_type():
    if minor < 7:
        from typing import GenericMeta as _GenericAlias
    else:
        from typing import _GenericAlias

    return _GenericAlias


def _get_callable_type():
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


def within(
    val: Union[float, int],
    low_bound: Union[float, int],
    upper_bound: Union[float, int],
    inclusive_lower: bool = False,
    inclusive_upper: bool = False,
) -> None:
    """Checks that a value is within a defined range

    Args:
        val: value to check against
        low_bound: lower bound of range
        upper_bound: upper bound of range
        inclusive_lower: if the check includes the bound value (i.e. >=)
        inclusive_upper: if the check includes the bound value (i.e. <=)

    Returns:
        None

    Raises:
        _SpockValueError

    """
    # Check lower bounds
    lower_fn = le if inclusive_upper else lt
    upper_fn = ge if inclusive_lower else gt
    upper_fn(val=val, bound=low_bound)
    lower_fn(val=val, bound=upper_bound)


def ge(val: Union[float, int], bound: Union[float, int]) -> None:
    """Checks that a value is greater than or equal to (inclusive) a lower bound

    Args:
        val: value to check against
        bound: lower bound

    Returns:
        None

    Raises:
        _SpockValueError

    """
    if val < bound:
        raise _SpockValueError(
            f"Set value `{val}` is not >= given bound value `{bound}`"
        )


def gt(val: Union[float, int], bound: Union[float, int]) -> None:
    """Checks that a value is greater (non-inclusive) than a lower bound

    Args:
        val: value to check against
        bound: lower bound

    Returns:
        None

    Raises:
        _SpockValueError

    """
    if val <= bound:
        raise _SpockValueError(
            f"Set value `{val}` is not > given bound value `{bound}`"
        )


def le(
    val: Union[float, int],
    bound: Union[float, int],
) -> None:
    """Checks that a value is less than or equal to (inclusive) an upper bound

    Args:
        val: value to check against
        bound: upper bound

    Returns:
        None

    Raises:
        _SpockValueError

    """
    if val > bound:
        raise _SpockValueError(
            f"Set value `{val}` is not <= given bound value `{bound}`"
        )


def lt(val: Union[float, int], bound: Union[float, int]) -> None:
    """Checks that a value is less (non-inclusive) than an upper bound

    Args:
        val: value to check against
        bound: upper bound

    Returns:
        None

    Raises:
        _SpockValueError

    """
    if val >= bound:
        raise _SpockValueError(
            f"Set value `{val}` is not < given bound value `{bound}`"
        )


def _find_all_spock_classes(attr_class: Type):
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


def _check_4_spock_iterable(iter_obj: Union[tuple, list]):
    """Checks if an iterable type contains a spock class

    Args:
        iter_obj: iterable type

    Returns:
        boolean if the iterable contains at least one spock class

    """
    return _check_iterable(iter_obj=iter_obj)


def _get_enum_classes(enum_obj: EnumMeta):
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


def _is_spock_instance(__obj: object):
    """Checks if the object is a @spock decorated class

    Private interface that checks to see if the object passed in is registered within the spock module and also
    is a class with attrs attributes (__attrs_attrs__)

    Args:
        __obj: class to inspect

    Returns:
        bool

    """
    return attr.has(__obj) and (__obj.__module__ == "spock.backend.config")


def _is_spock_tune_instance(__obj: object):
    """Checks if the object is a @spock decorated class

    Private interface that checks to see if the object passed in is registered within the spock module tune addon and also
    is a class with attrs attributes (__attrs_attrs__)

    Args:
        __obj: class to inspect

    Returns:
        bool

    """
    return attr.has(__obj) and (__obj.__module__ == "spock.addons.tune.config")


def _check_iterable(iter_obj: Union[tuple, list, EnumMeta]):
    """Check if an iterable type contains a spock class

    Args:
        iter_obj: iterable type

    Returns:
        boolean if the iterable contains at least one spock class

    """
    return any([_is_spock_instance(v.value) for v in iter_obj])


def make_argument(arg_name, arg_type, parser):
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


def _handle_generic_type_args(val):
    """Evaluates a string containing a Python literal

    Seeing a list and tuple types will come in as string literal format, use ast to get the actual type

    Args:
        val: string literal

    Returns:
        the underlying string literal type

    """
    return ast.literal_eval(val)


def add_info():
    """Adds extra information to the output dictionary

    Args:

    Returns:
        out_dict: output dictionary
    """
    out_dict = {}
    out_dict = add_generic_info(out_dict)
    out_dict = add_repo_info(out_dict)
    return out_dict


def make_blank_git(out_dict):
    """Adds blank git info

    Args:
        out_dict: current output dictionary

    Returns:
        out_dict: output dictionary with added git info

    """
    for key in ("BRANCH", "COMMIT SHA", "STATUS", "ORIGIN"):
        out_dict.update({f"# Git {key}": "UNKNOWN"})
    return out_dict


def add_repo_info(out_dict):
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


def add_generic_info(out_dict):
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


def _maybe_docker(cgroup_path="/proc/self/cgroup"):
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


def _maybe_k8s(cgroup_path="/proc/self/cgroup"):
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


def deep_payload_update(source, updates):
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
        if isinstance(v, dict) and v:
            source_dict = {} if source.get(k) is None else source.get(k)
            updated_dict = deep_payload_update(source_dict, v)
            if updated_dict:
                source[k] = updated_dict
        else:
            source[k] = v
    return source


def check_payload_overwrite(payload, updates, configs, overwrite=""):
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
