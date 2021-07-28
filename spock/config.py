# -*- coding: utf-8 -*-

# Copyright FMR LLC <opensource@fidelity.com>
# SPDX-License-Identifier: Apache-2.0

"""Creates the spock config decorator that wraps attrs"""

from spock.backend.config import spock_attr
from spock.utils import _is_spock_instance

# Simplified decorator for attrs
spock = spock_attr

# Public alias for checking if an object is a @spock annotated class
isinstance_spock = _is_spock_instance
