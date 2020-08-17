# -*- coding: utf-8 -*-

# Copyright 2019 FMR LLC <opensource@fidelity.com>
# SPDX-License-Identifier: Apache-2.0

"""Handles payloads from markup files"""

from itertools import chain
import os
from pathlib import Path
from spock.payload import BasePayload


class AttrPayload(BasePayload):
    def __init__(self):
        super(BasePayload, self).__init__()

    def __call__(self, *args, **kwargs):
        """Call to allow self chaining

        *Args*:

            *args:
            **kwargs:

        *Returns*:

            Payload: instance of self

        """
        return AttrPayload()

    def payload(self, input_classes, path):
        pass

    def _handle_includes(self, base_payload, config_extension, input_classes, path, payload):
        pass
