# -*- coding: utf-8 -*-

# Copyright FMR LLC <opensource@fidelity.com>
# SPDX-License-Identifier: Apache-2.0

"""Resolver functions for Spock"""

import re
import os
from typing import Any

from spock.exceptions import _SpockEnvResolverError
from spock.utils import _T


# ENV Resolver -- full regex is ^\${spock\.env:.*}$
CLIP_ENV_PATTERN = r"^\${spock\.env:"
CLIP_REGEX_OP = re.compile(CLIP_ENV_PATTERN)
END_ENV_PATTERN = r"}$"
END_REGEX_OP = re.compile(END_ENV_PATTERN)
FULL_ENV_PATTERN = CLIP_ENV_PATTERN + r".*" + END_ENV_PATTERN
FULL_REGEX_OP = re.compile(FULL_ENV_PATTERN)


def parse_env_variables(value: Any, value_type: _T) -> Any:
    # Check if it matches the regex
    # if so then split and replace with the value from the env -- have to check here if the env variable actually
    # exists -- if it doesn't then we need to raise an exception -- allow for None?

    # If it's a string we can check the regex
    if isinstance(value, str):
        # Check the regex
        match_obj = FULL_REGEX_OP.fullmatch(value)
        # if the object exists then we've matched a pattern and need to handle it
        if match_obj is not None:
            return _get_env_value(value, value_type)
        # Regex doesn't match so just passthrough
        else:
            return value
    # If it's not a string we can't resolve anything so just passthrough and let spock handle the value
    else:
        return value


def _handle_default(value: str):
    env_value, default_value = value.split(',')
    default_value = default_value.strip()
    # Swap string None to type None
    if default_value == "None":
        default_value = None
    return env_value, default_value


def _get_env_value(value: str, value_type: _T):
    # Based on the start and end regex ops find the value the user set
    env_str = END_REGEX_OP.split(CLIP_REGEX_OP.split(value)[1])[0]
    # Attempt to split on a comma for a default value
    split_len = len(env_str.split(','))
    # Default found if the len is 2
    if split_len == 2:
        env_value, default_value = _handle_default(env_str)
    # If the length is larger than two then the syntax is messed up
    elif split_len > 2:
        raise _SpockEnvResolverError(
            f"Issue with environment variable syntax -- currently `{value}` has more than one `,` which means the "
            f"optional default value cannot be resolved -- please use only one `,` separator within the syntax"
        )
    else:
        env_value = env_str
        default_value = "None"
    # Attempt to get the env variable
    if default_value == "None":
        maybe_env = os.getenv(env_value)
    else:
        maybe_env = os.getenv(env_value, default_value)
    if maybe_env is None and default_value == "None":
        raise _SpockEnvResolverError(
            f"Attempted to get `{env_value}` from environment variables but it is not set -- please set this "
            f"variable or provide a default via the following syntax ${{spock.env:{env_value},DEFAULT}}"
        )
    else:
        # Attempt to cast in a try to be able to catch the failed type casts with an exception
        try:
            typed_env = value_type(maybe_env) if maybe_env is not None else None
        except Exception as e:
            raise _SpockEnvResolverError(
                f"Failed attempting to cast environment variable (name: {env_value}, value: `{maybe_env}`) "
                f"into Spock specified type `{value_type.__name__}`"
            )
        return typed_env
