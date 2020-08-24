# -*- coding: utf-8 -*-

# Copyright 2019 FMR LLC <opensource@fidelity.com>
# SPDX-License-Identifier: Apache-2.0

"""Creates the spock config decorator that wraps dataclasses"""

from spock.backend.dataclass.config import spock_dataclass
from spock.backend.attr.config import spock_attr

# Dataclasses for legacy support -- now wraps attr via an adapter
spock_config = spock_dataclass

# Simplified decorator for attrs
spock = spock_attr
