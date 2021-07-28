# -*- coding: utf-8 -*-

# Copyright FMR LLC <opensource@fidelity.com>
# SPDX-License-Identifier: Apache-2.0

"""Handles the tuner payload backend"""

from spock.backend.payload import BasePayload
from spock.backend.utils import get_attr_fields


class TunerPayload(BasePayload):
    """Handles building the payload for tuners

    This class builds out the payload from config files of multiple types. It handles various
    file types and also composition of config files via a recursive calls

    *Attributes*:

        _loaders: maps of each file extension to the loader class

    """

    def __init__(self, s3_config=None):
        """Init for TunerPayload

        *Args*:

            s3_config: optional S3 config object

        """
        super().__init__(s3_config=s3_config)

    def __call__(self, *args, **kwargs):
        """Call to allow self chaining

        *Args*:

            *args:
            **kwargs:

        *Returns*:

            Payload: instance of self

        """
        return TunerPayload(*args, **kwargs)

    @staticmethod
    def _update_payload(base_payload, input_classes, ignore_classes, payload):
        # Get basic args
        attr_fields = get_attr_fields(input_classes=input_classes)
        # Get the ignore fields
        ignore_fields = get_attr_fields(input_classes=ignore_classes)
        for k, v in base_payload.items():
            if k not in ignore_fields:
                if k != "config":
                    # Dict infers that we are overriding a global setting in a specific config
                    if isinstance(v, dict):
                        # we're in a namespace
                        # Check for incorrect specific override of global def
                        if k not in attr_fields:
                            raise TypeError(
                                f"Referring to a class space {k} that is undefined"
                            )
                        for i_keys in v.keys():
                            if i_keys not in attr_fields[k]:
                                raise ValueError(
                                    f"Provided an unknown argument named {k}.{i_keys}"
                                )
                    if k in payload and isinstance(v, dict):
                        payload[k].update(v)
                    else:
                        payload[k] = v
                    # Handle tuple conversion here -- lazily
                    for ik, iv in v.items():
                        if "bounds" in iv:
                            iv["bounds"] = tuple(iv["bounds"])
        return payload

    @staticmethod
    def _handle_payload_override(payload, key, value):
        key_split = key.split(".")
        curr_ref = payload
        for idx, split in enumerate(key_split):
            # If the root isn't in the payload then it needs to be added but only for the first key split
            if idx == 0 and (split not in payload):
                payload.update({split: {}})
            # Check if it's the last value and figure out the override
            if idx == (len(key_split) - 1):
                # Handle bool(s) a bit differently as they are store_true
                if isinstance(curr_ref, dict) and isinstance(value, bool):
                    if value is not False:
                        curr_ref[split] = value
                # If we are at the dictionary level we should be able to just payload override
                elif isinstance(curr_ref, dict) and not isinstance(value, bool):
                    curr_ref[split] = value
                else:
                    raise ValueError(
                        f"cmd-line override failed for {key} -- "
                        f"Failed to find key {split} within lowest level Dict"
                    )
            # If it's not keep walking the current payload
            else:
                curr_ref = curr_ref[split]
        return payload
