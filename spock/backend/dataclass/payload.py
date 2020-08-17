# -*- coding: utf-8 -*-

# Copyright 2019 FMR LLC <opensource@fidelity.com>
# SPDX-License-Identifier: Apache-2.0

"""Handles payloads from markup files"""

from itertools import chain
import os
from pathlib import Path
from spock.payload import BasePayload


class DataClassPayload(BasePayload):
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
        return DataClassPayload()

    def payload(self, input_classes, path):
        # Match to loader based on file-extension
        config_extension = Path(path).suffix.lower()
        supported_extensions = list(self._loaders.keys())
        if config_extension not in supported_extensions:
            raise TypeError(f'File extension {config_extension} not supported\n'
                            f'Must be from {supported_extensions}')
        # Load from file
        base_payload = self._loaders.get(config_extension).load(path)
        payload = {}
        if 'config' in base_payload:
            payload = self._handle_includes(
                base_payload, config_extension, input_classes, path, payload)
        payload = self._update_payload(base_payload, input_classes, payload)
        return payload

    def _handle_includes(self, base_payload, config_extension, input_classes, path, payload):  #pylint: disable=too-many-arguments
        included_params = {}
        for inc_path in base_payload['config']:
            if not os.path.exists(inc_path):
                # maybe it's relative?
                abs_inc_path = os.path.join(os.path.dirname(path), inc_path)
            else:
                abs_inc_path = inc_path
            if not os.path.exists(abs_inc_path):
                raise RuntimeError(f'Could not find included {config_extension} file {inc_path}!')
            included_params.update(self.payload(input_classes, abs_inc_path))
        payload.update(included_params)
        return payload

    @staticmethod
    def _update_payload(base_payload, input_classes, payload):
        """Updates the payload

        Checks the parameters defined in the config files against the provided dataclasses and if
        passable adds them to the payload

        *Args*:

            base_payload: current payload
            input_classes: dataclass to roll into
            payload: total payload

        *Returns*:

            payload: updated payload

        """
        # Get basic args
        dc_fields = {dc.__name__: list(vars(dc).get('__dataclass_fields__').keys()) for dc in input_classes}
        # Get the choice args and insert them
        # dc_fields = self._handle_choices(dc_fields, input_classes)
        for keys, values in base_payload.items():
            # check if the keys, value pair is expected by a dataclass
            if keys != 'config':
                # Dict infers that we are overriding a global setting in a specific config
                if isinstance(values, dict):
                    # we're in a namespace
                    # Check for incorrect specific override of global def
                    if keys not in dc_fields:
                        raise TypeError(f'Referring to a class space {keys} that is undefined')
                    for i_keys in values.keys():
                        if i_keys not in dc_fields[keys]:
                            raise ValueError(f'Provided an unknown argument named {keys}.{i_keys}')
                else:
                    # Chain all the values from multiple spock classes into one list
                    if keys not in list(chain(*dc_fields.values())):
                        raise ValueError(f'Provided an unknown argument named {keys}')
            if keys in payload and isinstance(values, dict):
                payload[keys].update(values)
            else:
                payload[keys] = values
        return payload
