# -*- coding: utf-8 -*-

# Copyright FMR LLC <opensource@fidelity.com>
# SPDX-License-Identifier: Apache-2.0

"""Handles payloads from markup files"""

import os
import sys
from abc import abstractmethod
from itertools import chain
from pathlib import Path

from spock.backend.handler import BaseHandler
from spock.backend.utils import convert_to_tuples, deep_update, get_type_fields
from spock.utils import check_path_s3


class BasePayload(BaseHandler):  # pylint: disable=too-few-public-methods
    """Handles building the payload for config file(s)

    This class builds out the payload from config files of multiple types. It handles various
    file types and also composition of config files via recursive calls

    *Attributes*:

        _loaders: maps of each file extension to the loader class
        __s3_config: optional S3Config object to handle s3 access

    """

    def __init__(self, s3_config=None):
        super(BasePayload, self).__init__(s3_config=s3_config)

    @staticmethod
    @abstractmethod
    def _update_payload(base_payload, input_classes, ignore_classes, payload):
        """Updates the payload

        Checks the parameters defined in the config files against the provided classes and if
        passable adds them to the payload

        *Args*:

            base_payload: current payload
            input_classes: class to roll into
            ignore_classes: list of classes to ignore
            payload: total payload

        *Returns*:

            payload: updated payload

        """

    def payload(self, input_classes, ignore_classes, path, cmd_args, deps):
        """Builds the payload from config files

        Public exposed call to build the payload and set any command line overrides

        *Args*:

            input_classes: list of backend classes
            ignore_classes: list of classes to ignore
            path: path to config file(s)
            cmd_args: command line overrides
            deps: dictionary of config dependencies

        *Returns*:

            payload: dictionary of all mapped parameters

        """
        payload = self._payload(input_classes, ignore_classes, path, deps, root=True)
        payload = self._handle_overrides(payload, ignore_classes, cmd_args)
        return payload

    def _payload(self, input_classes, ignore_classes, path, deps, root=False):
        """Private call to construct the payload

        Main function call that builds out the payload from config files of multiple types. It handles
        various file types and also composition of config files via a recursive calls

        *Args*:
            input_classes: list of backend classes
            ignore_classes: list of classes to ignore
            path: path to config file(s)
            deps: dictionary of config dependencies

        *Returns*:

            payload: dictionary of all mapped parameters

        """
        # Match to loader based on file-extension
        config_extension = Path(path).suffix.lower()
        # Verify extension
        self._check_extension(file_extension=config_extension)
        # Load from file
        base_payload = self._supported_extensions.get(config_extension)().load(
            path, s3_config=self._s3_config
        )
        # Check and? update the dependencies
        deps = self._handle_dependencies(deps, path, root)
        payload = {}
        if "config" in base_payload:
            payload = self._handle_includes(
                base_payload,
                config_extension,
                input_classes,
                ignore_classes,
                path,
                payload,
                deps,
            )
        payload = self._update_payload(
            base_payload, input_classes, ignore_classes, payload
        )
        return payload

    @staticmethod
    def _handle_dependencies(deps, path, root):
        """Handles config file dependencies

        Checks to see if the config path (full or relative) has already been encountered. Essentially a DFS for graph
        cycles

        *Args*:

            deps: dictionary of config dependencies
            path: current config path
            root: boolean if root

        *Returns*:

            deps: updated dependencies

        """
        if root and path in deps.get("paths"):
            raise ValueError(
                f"Duplicate Read -- Config file {path} has already been encountered. "
                f"Please remove duplicate reads of config files."
            )
        elif path in deps.get("paths") or path in deps.get("rel_paths"):
            raise ValueError(
                f"Cyclical Dependency -- Config file {path} has already been encountered. "
                f"Please remove cyclical dependencies between config files."
            )
        else:
            # Update the dependency lists
            deps.get("paths").append(path)
            deps.get("rel_paths").append(os.path.basename(path))
            if root:
                deps.get("roots").append(path)
        return deps

    def _handle_includes(
        self,
        base_payload,
        config_extension,
        input_classes,
        ignore_classes,
        path,
        payload,
        deps,
    ):  # pylint: disable=too-many-arguments
        """Handles config composition

        For all of the config tags in the config file this function will recursively call the payload function
        with the composition path to get the additional payload(s) from the composed file(s) -- checks for file
        validity or if it is an S3 URI via regex

        *Args*:

            base_payload: base payload that has a config kwarg
            config_extension: file type
            input_classes: defined backend classes
            ignore_classes: list of classes to ignore
            path: path to base file
            payload: payload pulled from composed files
            deps: dictionary of config dependencies

        *Returns*:

            payload: payload update from composed files

        """
        included_params = {}
        for inc_path in base_payload["config"]:
            if check_path_s3(inc_path):
                use_path = inc_path
            elif os.path.exists(inc_path):
                use_path = inc_path
            elif os.path.join(os.path.dirname(path), inc_path):
                use_path = os.path.join(os.path.dirname(path), inc_path)
            else:
                raise RuntimeError(
                    f"Could not find included {config_extension} file {inc_path} or is not an S3 URI!"
                )
            included_params.update(
                self._payload(input_classes, ignore_classes, use_path, deps)
            )
        payload.update(included_params)
        return payload

    def _handle_overrides(self, payload, ignore_classes, args):
        """Handle command line overrides

        Iterate through the command line override values, determine at what level to set them, and set them if possible

        *Args*:

            payload: current payload dictionary
            args: command line override args

        *Returns*:

            payload: updated payload dictionary with override values set

        """
        skip_keys = ["config", "help"]
        pruned_args = self._prune_args(args, ignore_classes)
        for k, v in pruned_args.items():
            if k not in skip_keys and v is not None:
                payload = self._handle_payload_override(payload, k, v)
        return payload

    @staticmethod
    def _prune_args(args, ignore_classes):
        """Prunes ignored class names from the cmd line args list to prevent incorrect access

        *Args*:

            args: current cmd line args
            ignore_classes: list of class names to ignore

        *Returns*:

            dictionary of pruned cmd line args

        """
        ignored_stems = [val.__name__ for val in ignore_classes]
        return {
            k: v for k, v in vars(args).items() if k.split(".")[0] not in ignored_stems
        }

    @staticmethod
    @abstractmethod
    def _handle_payload_override(payload, key, value):
        """Handles the complex logic needed for List[spock class] overrides

        Messy logic that sets overrides for the various different types. The hardest being List[spock class] since str
        names have to be mapped backed to sys.modules and can be set at either the general or class level.

        *Args*:

            payload: current payload dictionary
            key: current arg key
            value: value at current arg key

        *Returns*:

            payload: modified payload with overrides

        """


class AttrPayload(BasePayload):
    """Handles building the payload for attrs backend

    This class builds out the payload from config files of multiple types. It handles various
    file types and also composition of config files via a recursive calls

    *Attributes*:

        _loaders: maps of each file extension to the loader class

    """

    def __init__(self, s3_config=None):
        """Init for AttrPayload

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
        return AttrPayload(*args, **kwargs)

    @staticmethod
    def _update_payload(base_payload, input_classes, ignore_classes, payload):
        # Get basic args
        attr_fields = {
            attr.__name__: [val.name for val in attr.__attrs_attrs__]
            for attr in input_classes
        }
        # Get the ignore fields
        ignore_fields = {
            attr.__name__: [val.name for val in attr.__attrs_attrs__]
            for attr in ignore_classes
        }
        # Class names
        class_names = [val.__name__ for val in input_classes]
        # Parse out the types if generic
        type_fields = get_type_fields(input_classes)
        for keys, values in base_payload.items():
            if keys not in ignore_fields:
                # check if the keys, value pair is expected by the attr class
                if keys != "config":
                    # Dict infers that we are overriding a global setting in a specific config
                    if isinstance(values, dict):
                        # we're in a namespace
                        # Check for incorrect specific override of global def
                        if keys not in attr_fields:
                            raise TypeError(
                                f"Referring to a class space {keys} that is undefined"
                            )
                        for i_keys in values.keys():
                            if i_keys not in attr_fields[keys]:
                                raise ValueError(
                                    f"Provided an unknown argument named {keys}.{i_keys}"
                                )
                    else:
                        # Check if the key is actually a reference to another class
                        if keys in class_names:
                            if isinstance(values, list):
                                # Check for incorrect specific override of global def
                                if keys not in attr_fields:
                                    raise ValueError(
                                        f"Referring to a class space {keys} that is undefined"
                                    )
                                # We are in a repeated class def
                                # Raise if the key set is different from the defined set (i.e. incorrect arguments)
                                key_set = set(
                                    list(chain(*[list(val.keys()) for val in values]))
                                )
                                for i_keys in key_set:
                                    if i_keys not in attr_fields[keys]:
                                        raise ValueError(
                                            f"Provided an unknown argument named {keys}.{i_keys}"
                                        )
                            # Chain all the values from multiple spock classes into one list
                            elif keys not in list(chain(*attr_fields.values())):
                                raise ValueError(
                                    f"Provided an unknown argument named {keys}"
                                )
                        # Chain all the values from multiple spock classes into one list
                        elif keys not in list(chain(*attr_fields.values())):
                            raise ValueError(
                                f"Provided an unknown argument named {keys}"
                            )
                if keys in payload and isinstance(values, dict):
                    payload[keys].update(values)
                else:
                    payload[keys] = values
        tuple_payload = convert_to_tuples(payload, type_fields, class_names)
        payload = deep_update(payload, tuple_payload)
        return payload

    @staticmethod
    def _handle_payload_override(payload, key, value):
        """Handles the complex logic needed for List[spock class] overrides

        Messy logic that sets overrides for the various different types. The hardest being List[spock class] since str
        names have to be mapped backed to sys.modules and can be set at either the general or class level.

        *Args*:

            payload: current payload dictionary
            key: current arg key
            value: value at current arg key

        *Returns*:

            payload: modified payload with overrides

        """
        key_split = key.split(".")
        curr_ref = payload
        for idx, split in enumerate(key_split):
            # If the root isn't in the payload then it needs to be added but only for the first key split
            if idx == 0 and (split not in payload):
                payload.update({split: {}})
            # Check for curr_ref switch over -- verify by checking the sys modules names
            if (
                idx != 0
                and (split in payload)
                and (isinstance(curr_ref, str))
                and (hasattr(sys.modules["spock"].backend.config, split))
            ):
                curr_ref = payload[split]
            elif (
                idx != 0
                and (split in payload)
                and (isinstance(payload[split], str))
                and (hasattr(sys.modules["spock"].backend.config, payload[split]))
            ):
                curr_ref = payload[split]
            # elif check if it's the last value and figure out the override
            elif idx == (len(key_split) - 1):
                # Handle bool(s) a bit differently as they are store_true
                if isinstance(curr_ref, dict) and isinstance(value, bool):
                    if value is not False:
                        curr_ref[split] = value
                # If we are at the dictionary level we should be able to just payload override
                elif isinstance(curr_ref, dict) and not isinstance(value, bool):
                    curr_ref[split] = value
                # If we are at a list level it must be some form of repeated class since this is the end of the class
                # tree -- check the instance type but also make sure the cmd-line override is the correct len
                elif isinstance(curr_ref, list) and len(value) == len(curr_ref):
                    # Walk the list and check for the key
                    for ref_idx, val in enumerate(curr_ref):
                        if split in val:
                            val[split] = value[ref_idx]
                        else:
                            raise ValueError(
                                f"cmd-line override failed for {key} -- "
                                f"Failed to find key {split} within lowest level List[Dict]"
                            )
                elif isinstance(curr_ref, list) and len(value) != len(curr_ref):
                    raise ValueError(
                        f"cmd-line override failed for {key} -- "
                        f"Specified key {split} with len {len(value)} does not match len {len(curr_ref)} "
                        f"of List[Dict]"
                    )
                else:
                    raise ValueError(
                        f"cmd-line override failed for {key} -- "
                        f"Failed to find key {split} within lowest level Dict"
                    )
            # If it's not keep walking the current payload
            else:
                curr_ref = curr_ref[split]
        return payload
