# -*- coding: utf-8 -*-

# Copyright FMR LLC <opensource@fidelity.com>
# SPDX-License-Identifier: Apache-2.0

"""Resolver functions for Spock"""
import os
import re
from abc import ABC, abstractmethod
from typing import Any, ByteString, Optional, Tuple

from spock.backend.utils import decrypt_value
from spock.exceptions import _SpockResolverError
from spock.utils import _T


class BaseResolver(ABC):
    def __init__(self):
        self._annotation_set = {"crypto", "inject"}

    @abstractmethod
    def resolve(self, value: Any, value_type: _T) -> Tuple[Any, Optional[str]]:
        pass

    @staticmethod
    def _handle_default(value: str):
        env_value, default_value = value.split(",")
        default_value = default_value.strip()
        # Swap string None to type None
        if default_value == "None":
            default_value = None
        return env_value, default_value

    @staticmethod
    def _check_base_regex(
        full_regex_op: re.Pattern,
        value: Any,
    ) -> bool:
        # If it's a string we can check the regex
        if isinstance(value, str):
            # Check the regex and return non None status
            return full_regex_op.fullmatch(value) is not None
        # If it's not a string we can't resolve anything so just passthrough and let spock handle the value
        else:
            return False

    @staticmethod
    def _attempt_cast(maybe_env: Optional[str], value_type: _T, env_value: str):
        # Attempt to cast in a try to be able to catch the failed type casts with an exception
        try:
            typed_env = value_type(maybe_env) if maybe_env is not None else None
        except Exception as e:
            raise _SpockResolverError(
                f"Failed attempting to cast environment variable (name: {env_value}, value: `{maybe_env}`) "
                f"into Spock specified type `{value_type.__name__}`"
            )
        return typed_env

    def _apply_regex(
        self,
        end_regex_op: re.Pattern,
        clip_regex_op: re.Pattern,
        value: str,
        allow_default: bool,
        allow_annotation: bool,
    ):
        # Based on the start and end regex ops find the value the user set
        env_str = end_regex_op.split(clip_regex_op.split(value)[-1])[0]
        if (
            allow_annotation
            and len(clip_regex_op.split(value)) > 2
            and clip_regex_op.split(value)[1] != ""
        ):
            annotation = clip_regex_op.split(value)[1]
            if annotation not in self._annotation_set:
                raise _SpockResolverError(
                    f"Environment variable annotation must be within {self._annotation_set} -- got `{annotation}`"
                )
        elif not allow_annotation and len(clip_regex_op.split(value)) > 2:
            raise _SpockResolverError(
                f"Found annotation style format however `{value}` does not support annotations"
            )
        else:
            annotation = None
        # Attempt to split on a comma for a default value
        split_len = len(env_str.split(","))
        # Default found if the len is 2
        if split_len == 2 and allow_default:
            env_value, default_value = self._handle_default(env_str)
        # If the length is larger than two then the syntax is messed up
        elif split_len > 2 and allow_default:
            raise _SpockResolverError(
                f"Issue with environment variable syntax -- currently `{value}` has more than one `,` which means the "
                f"optional default value cannot be resolved -- please use only one `,` separator within the syntax"
            )
        elif split_len > 1 and not allow_default:
            raise _SpockResolverError(
                f"Syntax does not support default values -- currently `{value}` contains the separator `,` which "
                f"id used to indicate default values"
            )
        else:
            env_value = env_str
            default_value = "None"
        return env_value, default_value, annotation


class EnvResolver(BaseResolver):
    # ENV Resolver -- full regex is ^\${spock\.env:.*}$
    CLIP_ENV_PATTERN = r"^\${spock\.env\.?([a-z]*?):"
    CLIP_REGEX_OP = re.compile(CLIP_ENV_PATTERN)
    END_ENV_PATTERN = r"}$"
    END_REGEX_OP = re.compile(END_ENV_PATTERN)
    FULL_ENV_PATTERN = CLIP_ENV_PATTERN + r".*" + END_ENV_PATTERN
    FULL_REGEX_OP = re.compile(FULL_ENV_PATTERN)

    def __init__(self):
        super(EnvResolver, self).__init__()

    def resolve(self, value: Any, value_type: _T) -> Tuple[Any, Optional[str]]:
        # Check the full regex for a match
        regex_match = self._check_base_regex(self.FULL_REGEX_OP, value)
        # if there is a regex match it needs to be handled by the underlying resolver ops
        if regex_match:
            # Apply the regex
            env_value, default_value, annotation = self._apply_regex(
                self.END_REGEX_OP,
                self.CLIP_REGEX_OP,
                value,
                allow_default=True,
                allow_annotation=True,
            )
            # Get the value from the env
            maybe_env = self._get_from_env(default_value, env_value)
            # Attempt to cast the value to its underlying type
            typed_env = self._attempt_cast(maybe_env, value_type, env_value)
        # Else just pass through
        else:
            typed_env = value
            annotation = None
        return typed_env, annotation

    @staticmethod
    def _get_from_env(default_value: Optional[str], env_value: str):
        # Attempt to get the env variable
        if default_value == "None":
            maybe_env = os.getenv(env_value)
        else:
            maybe_env = os.getenv(env_value, default_value)
        if maybe_env is None and default_value == "None":
            raise _SpockResolverError(
                f"Attempted to get `{env_value}` from environment variables but it is not set -- please set this "
                f"variable or provide a default via the following syntax ${{spock.env:{env_value},DEFAULT}}"
            )
        return maybe_env


class CryptoResolver(BaseResolver):
    # ENV Resolver -- full regex is ^\${spock\.crypto:.*}$
    CLIP_ENV_PATTERN = r"^\${spock\.crypto:"
    CLIP_REGEX_OP = re.compile(CLIP_ENV_PATTERN)
    END_ENV_PATTERN = r"}$"
    END_REGEX_OP = re.compile(END_ENV_PATTERN)
    FULL_ENV_PATTERN = CLIP_ENV_PATTERN + r".*" + END_ENV_PATTERN
    FULL_REGEX_OP = re.compile(FULL_ENV_PATTERN)

    def __init__(self, salt: str, key: ByteString):
        super(CryptoResolver, self).__init__()
        self._salt = salt
        self._key = key

    def resolve(self, value: Any, value_type: _T) -> Tuple[Any, Optional[str]]:
        regex_match = self._check_base_regex(self.FULL_REGEX_OP, value)
        if regex_match:
            crypto_value, default_value, annotation = self._apply_regex(
                self.END_REGEX_OP,
                self.CLIP_REGEX_OP,
                value,
                allow_default=False,
                allow_annotation=False,
            )
            decrypted_value = decrypt_value(crypto_value, self._key, self._salt)
            typed_decrypted = self._attempt_cast(
                decrypted_value, value_type, crypto_value
            )
            annotation = "crypto"
        # Pass through
        else:
            typed_decrypted = value
            annotation = None
        # Crypto in --> crypto out annotation wise or else this exposes the value in plaintext
        return typed_decrypted, annotation
