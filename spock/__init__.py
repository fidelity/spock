# -*- coding: utf-8 -*-

# Copyright FMR LLC <opensource@fidelity.com>
# SPDX-License-Identifier: Apache-2.0

"""
Spock is a framework that helps manage complex parameter configurations for Python applications

Please refer to the documentation provided in the README.md
"""

from spock._version import get_versions

__all__ = ["args", "builder", "config"]

__version__ = get_versions()["version"]
del get_versions
