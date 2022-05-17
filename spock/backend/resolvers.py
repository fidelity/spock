# -*- coding: utf-8 -*-

# Copyright FMR LLC <opensource@fidelity.com>
# SPDX-License-Identifier: Apache-2.0

"""Resolver functions for Spock"""
import os
import re
from abc import ABC, abstractmethod
from distutils.util import strtobool
from typing import Any, ByteString, Optional, Pattern, Tuple, Union

from spock.backend.utils import decrypt_value
from spock.exceptions import _SpockResolverError
from spock.utils import _T


class BaseResolver(ABC):
    """Base class for resolvers

    Contains base methods for handling resolver syntax

    Attributes:
        _annotation_set: current set of supported resolver annotations

    """

    def __init__(self):
        """Init for BaseResolver class"""
        self._annotation_set = {"crypto", "inject"}

    @abstractmethod
    def resolve(self, value: Any, value_type: _T) -> Tuple[Any, Optional[str]]:
        """Resolves a variable from a given resolver syntax

        Args:
            value: current value to attempt to resolve
            value_type: type of the value to cast into

        Returns:
            Tuple of correctly typed resolved variable and any annotations

        """
        pass

    @staticmethod
    def _handle_default(value: str) -> Tuple[str, Union[str, None]]:
        """Handles setting defaults if allowed for a resolver

        Args:
            value: current string value

        Returns:
            tuple of given value and the default value

        """
        env_value, default_value = value.split(",")
        default_value = default_value.strip()
        # Swap string None to type None
        if default_value == "None":
            default_value = None
        return env_value, default_value

    @staticmethod
    def _check_base_regex(
        full_regex_op: Pattern,
        value: Any,
    ) -> bool:
        """Check if the value passed into the resolver matches the compiled regex op

        Args:
            full_regex_op: the full compiled regex
            value: the value passed into the resolver

        Returns:
            boolean if there is a regex match

        """
        # If it's a string we can check the regex
        if isinstance(value, str):
            # Check the regex and return non None status
            return full_regex_op.fullmatch(value) is not None
        # If it's not a string we can't resolve anything so just passthrough and let spock handle the value
        else:
            return False

    @staticmethod
    def _attempt_cast(maybe_env: Optional[str], value_type: _T, env_value: str) -> Any:
        """Attempts to cast the resolved variable into the given type

        Args:
            maybe_env: possible resolved variable
            value_type: type to cast into
            env_value: the reference to the resolved variable

        Returns:
            value type cast into the correct type

        Raises:
            _SpockResolverError if it cannot be cast into the specified type

        """
        # Attempt to cast in a try to be able to catch the failed type casts with an exception
        try:
            if value_type.__name__ == "bool":
                typed_env = (
                    value_type(strtobool(maybe_env)) if maybe_env is not None else False
                )
            else:
                typed_env = value_type(maybe_env) if maybe_env is not None else None
        except Exception as e:
            raise _SpockResolverError(
                f"Failed attempting to cast environment variable (name: {env_value}, value: `{maybe_env}`) "
                f"into Spock specified type `{value_type.__name__}`"
            )
        return typed_env

    def _apply_regex(
        self,
        end_regex_op: Pattern,
        clip_regex_op: Pattern,
        value: str,
        allow_default: bool,
        allow_annotation: bool,
    ) -> Tuple[str, str, Optional[str]]:
        """Applies the front and back regexes to the string value, determines defaults and annotations

        Args:
            end_regex_op: compiled regex for the back half of the match
            clip_regex_op: compiled regex for the front half of the match
            value: current string value to resolve
            allow_default: if allowed to contain default value syntax
            allow_annotation: if allowed to contain annotation syntax

        Returns:
            tuple containing the resolved string reference, the default value, and the annotation string

        Raises:
            _SpockResolverError if annotation isn't within the supported set, annotation is not supported, multiple `,`
                values are used, or defaults are given yet not supported

        """
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
        elif (
            not allow_annotation
            and len(clip_regex_op.split(value)) > 2
            and clip_regex_op.split(value)[1] != ""
        ):
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
    """Class for resolving environmental variables

    Attributes:
        _annotation_set: current set of supported resolver annotations
        CLIP_ENV_PATTERN: regex for the front half
        CLIP_REGEX_OP: compiled regex for front half
        END_ENV_PATTERN: regex for back half
        END_REGEX_OP: comiled regex for back half
        FULL_ENV_PATTERN: full regex pattern
        FULL_REGEX_OP: compiled regex for full regex

    """

    # ENV Resolver -- full regex is ^\${spock\.env\.?([a-z]*?):.*}$
    CLIP_ENV_PATTERN = r"^\${spock\.env\.?([a-z]*?):"
    CLIP_REGEX_OP = re.compile(CLIP_ENV_PATTERN)
    END_ENV_PATTERN = r"}$"
    END_REGEX_OP = re.compile(END_ENV_PATTERN)
    FULL_ENV_PATTERN = CLIP_ENV_PATTERN + r".*" + END_ENV_PATTERN
    FULL_REGEX_OP = re.compile(FULL_ENV_PATTERN)

    def __init__(self):
        """Init for EnvResolver"""
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
    def _get_from_env(default_value: Optional[str], env_value: str) -> Optional[str]:
        """Gets a value from an environmental variable

        Args:
            default_value: default value to fall back on for the env resolver
            env_value: current string of the env variable to get

        Returns:
            string or None for the resolved env variable

        Raises:
            _SpockResolverError if the env variable is not available or if no default is specified

        """
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
    """Class for resolving cryptographic variables

    Attributes:
        _annotation_set: current set of supported resolver annotations
        CLIP_ENV_PATTERN: regex for the front half
        CLIP_REGEX_OP: compiled regex for front half
        END_ENV_PATTERN: regex for back half
        END_REGEX_OP: comiled regex for back half
        FULL_ENV_PATTERN: full regex pattern
        FULL_REGEX_OP: compiled regex for full regex
        _salt: current cryptographic salt
        _key: current cryptographic key

    """

    # ENV Resolver -- full regex is ^\${spock\.crypto\.?([a-z]*?):.*}$
    CLIP_ENV_PATTERN = r"^\${spock\.crypto\.?([a-z]*?):"
    CLIP_REGEX_OP = re.compile(CLIP_ENV_PATTERN)
    END_ENV_PATTERN = r"}$"
    END_REGEX_OP = re.compile(END_ENV_PATTERN)
    FULL_ENV_PATTERN = CLIP_ENV_PATTERN + r".*" + END_ENV_PATTERN
    FULL_REGEX_OP = re.compile(FULL_ENV_PATTERN)

    def __init__(self, salt: str, key: ByteString):
        """Init for CryptoResolver

        Args:
            salt: cryptographic salt to use
            key: cryptographic key to use
        """
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
