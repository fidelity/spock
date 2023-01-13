# -*- coding: utf-8 -*-

# Copyright FMR LLC <opensource@fidelity.com>
# SPDX-License-Identifier: Apache-2.0

"""Handles custom types"""

from typing import TypeVar

directory = type("directory", (str,), {})
file = type("file", (str,), {})


_T = TypeVar("_T")
_C = TypeVar("_C", bound=type)
