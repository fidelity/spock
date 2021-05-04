# -*- coding: utf-8 -*-

# Copyright 2019 FMR LLC <opensource@fidelity.com>
# SPDX-License-Identifier: Apache-2.0

"""
Spock is a framework that helps manage complex parameter configurations for Python applications

Please refer to the documentation provided in the README.md
"""

from spock._version import get_versions
from spock.backend.s3.utils import S3Config

__all__ = ["args", "builder", "config", "S3Config"]

__version__ = get_versions()['version']
del get_versions