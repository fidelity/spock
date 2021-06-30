# -*- coding: utf-8 -*-

# Copyright FMR LLC <opensource@fidelity.com>
# SPDX-License-Identifier: Apache-2.0

"""Handles the optuna backend"""

import attr

try:
    import optuna
except ImportError:
    print('Missing libraries to support tune functionality. Please re-install with the extra tune dependencies -- '
          'pip install spock-config[tune]')


class OptunaBuilder:
    def __init__(self, *args, configs=None, no_cmd_line=False, **kwargs):
        """OptunaBuilder init

        Args:
            *args: list of input classes that link to a backend
            configs: None or List of configs to read from
            desc: description for the arg parser
            no_cmd_line: flag to force no command line reads
            **kwargs: any extra keyword args
        """
        # super().__init__(*args, configs=configs, desc=desc, no_cmd_line=no_cmd_line, **kwargs)
        self.input_classes = args
        self._configs = configs
        self._no_cmd_line = no_cmd_line
        self._verify_attr()

    def _verify_attr(self):
        """Verifies that all the input classes are attr based

         *Returns*:

            None

        """
        for arg in self.input_classes:
            if not attr.has(arg):
                raise TypeError(f'*arg inputs to {self.__class__.__name__} must all be class instances with attrs attributes')