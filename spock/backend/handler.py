# -*- coding: utf-8 -*-

# Copyright FMR LLC <opensource@fidelity.com>
# SPDX-License-Identifier: Apache-2.0

"""Base handler Spock class"""

from abc import ABC

from spock.handlers import JSONHandler, TOMLHandler, YAMLHandler


class BaseHandler(ABC):
    """Base class for saver and payload

    *Attributes*:

        _writers: maps file extension to the correct i/o handler
        _s3_config: optional S3Config object to handle s3 access

    """

    def __init__(self, s3_config=None):
        self._supported_extensions = {
            ".yaml": YAMLHandler,
            ".toml": TOMLHandler,
            ".json": JSONHandler,
        }
        self._s3_config = s3_config

    def _check_extension(self, file_extension: str):
        if file_extension not in self._supported_extensions:
            raise TypeError(
                f"File extension {file_extension} not supported -- \n"
                f"File extension must be from {list(self._supported_extensions.keys())}"
            )
