# -*- coding: utf-8 -*-

# Copyright FMR LLC <opensource@fidelity.com>
# SPDX-License-Identifier: Apache-2.0

"""
Spock is a framework that helps manage complex parameter configurations for Python applications

Please refer to the documentation provided in the README.md
"""

from spock._version import get_versions
from spock.backend.typed import SavePath
from spock.builder import ConfigArgBuilder
from spock.config import spock

SpockBuilder = ConfigArgBuilder

__all__ = ["args", "builder", "config", "SavePath", "spock", "SpockBuilder"]

__version__ = get_versions()["version"]
del get_versions
