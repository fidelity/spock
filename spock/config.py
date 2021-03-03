# -*- coding: utf-8 -*-

# Copyright 2019 FMR LLC <opensource@fidelity.com>
# SPDX-License-Identifier: Apache-2.0

"""Creates the spock config decorator that wraps attrs"""

from spock.backend.attr.config import spock_attr

# Simplified decorator for attrs
spock = spock_attr
