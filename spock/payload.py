# -*- coding: utf-8 -*-

# Copyright 2019 FMR LLC <opensource@fidelity.com>
# SPDX-License-Identifier: Apache-2.0

"""Handles payloads from markup files"""

from abc import ABC
from abc import abstractmethod
from spock.handlers import JSONHandler
from spock.handlers import TOMLHandler
from spock.handlers import YAMLHandler


class BasePayload(ABC):
    """Handles building the payload for config file(s)

    This class builds out the payload from config files of multiple types. It handles various
    file types and also composition of config files via a recursive calls

    *Attributes*:

        _loaders: maps of each file extension to the loader class

    """
    def __init__(self):
        self._loaders = {'.yaml': YAMLHandler(), '.toml': TOMLHandler(), '.json': JSONHandler()}

    @abstractmethod
    def payload(self, input_classes, path):
        """Builds the payload from config files

        Main function call that builds out the payload from config files of multiple types. It handles
        various file types and also composition of config files via a recursive calls

        *Args*:

            input_classes: list of input classes that define the necessary parameters
            path: path to config file(s)

        *Returns*:

            payload: dictionary of all mapped parameters

        """
        pass

    @abstractmethod
    def _handle_includes(self, base_payload, config_extension, input_classes, path, payload):
        """Handles config composition

        For all of the config tags in the config file this function will recursively call the payload function
        with the composition path to get the additional payload(s) from the composed file(s)

        *Args*:

            base_payload: base payload that has a config kwarg
            config_extension: file type
            input_classes: defined input classes
            path: path to base file
            payload: payload pulled from composed files

        Returns:

            payload: payload update from composed files

        """
        pass
