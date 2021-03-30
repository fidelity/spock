# -*- coding: utf-8 -*-

# Copyright 2019 FMR LLC <opensource@fidelity.com>
# SPDX-License-Identifier: Apache-2.0

"""Handles the building/saving of the configurations from the Spock config classes"""

import attr
from enum import EnumMeta
import re
import sys
from warnings import warn
from spock.backend.base import BaseBuilder


class AttrBuilder(BaseBuilder):
    """Attr specific builder

    Class that handles building for the attr backend

    *Attributes*

        input_classes: list of input classes that link to a backend
        _configs: None or List of configs to read from
        _create_save_path: boolean to make the path to save to
        _desc: description for the arg parser
        _no_cmd_line: flag to force no command line reads
        save_path: list of path(s) to save the configs to

    """
    def __init__(self, *args, configs=None, create_save_path=False, desc='', no_cmd_line=False, **kwargs):
        super().__init__(*args, configs=configs, create_save_path=create_save_path, desc=desc,
                         no_cmd_line=no_cmd_line, **kwargs)
        for arg in self.input_classes:
            if not attr.has(arg):
                raise TypeError('*arg inputs to ConfigArgBuilder must all be class instances with attrs attributes')

    def print_usage_and_exit(self, msg=None, sys_exit=True, exit_code=1):
        print(f'usage: {sys.argv[0]} -c [--config] config1 [config2, config3, ...]')
        print(f'\n{self._desc if self._desc != "" else ""}\n')
        print('configuration(s):\n')
        self._handle_help_info()
        if msg is not None:
            print(msg)
        if sys_exit:
            sys.exit(exit_code)

    def _handle_help_info(self):
        self._attrs_help(self.input_classes)

    def _handle_arguments(self, args, class_obj):
        attr_name = class_obj.__name__
        class_names = [val.__name__ for val in self.input_classes]
        # Handle repeated classes
        if attr_name in class_names and attr_name in args and isinstance(args[attr_name], list):
            fields = self._handle_repeated(args[attr_name], attr_name, class_names)
        # Handle non-repeated classes
        else:
            fields = {}
            for val in class_obj.__attrs_attrs__:
                # Check if namespace is named and then check for key -- checking for local class def
                if attr_name in args and val.name in args[attr_name]:
                    fields[val.name] = self._handle_nested_class(args, args[attr_name][val.name], class_names)
                # If not named then just check for keys -- checking for global def
                elif val.name in args:
                    fields[val.name] = self._handle_nested_class(args, args[val.name], class_names)
                # Check for special keys to set
                if 'special_key' in val.metadata and val.metadata['special_key'] is not None:
                    if val.name in args:
                        self.save_path = args[val.name]
                    elif val.default is not None:
                        self.save_path = val.default
        return fields

    def _handle_repeated(self, args, check_value, class_names):
        """Handles repeated classes as lists

        *Args*:

            args: dictionary of arguments from the configs
            check_value: value to check classes against
            class_names: current class names

        *Returns*:

            list of input_class[match)idx[0]] types filled with repeated values

        """
        # Check to see if the value trying to be set is actually an input class
        match_idx = [idx for idx, val in enumerate(class_names) if val == check_value]
        return [self.input_classes[match_idx[0]](**val) for val in args]

    def _handle_nested_class(self, args, check_value, class_names):
        """Handles passing another class to the field dictionary

        *Args*:
            args: dictionary of arguments from the configs
            check_value: value to check classes against
            class_names: current class names

        *Returns*:

            either the check_value or the necessary class

        """
        # Check to see if the value trying to be set is actually an input class
        match_idx = [idx for idx, val in enumerate(class_names) if val == check_value]
        # If so then create the needed class object by unrolling the args to **kwargs and return it
        if len(match_idx) > 0:
            if len(match_idx) > 1:
                raise ValueError('Match error -- multiple classes with the same name definition')
            else:
                if args.get(self.input_classes[match_idx[0]].__name__) is None:
                    raise ValueError(f'Missing config file definition for the referenced class '
                                     f'{self.input_classes[match_idx[0]].__name__}')
                current_arg = args.get(self.input_classes[match_idx[0]].__name__)
                if isinstance(current_arg, list):
                    class_value = [self.input_classes[match_idx[0]](**val) for val in current_arg]
                else:
                    class_value = self.input_classes[match_idx[0]](**current_arg)
            return_value = class_value
        # else return the expected value
        else:
            return_value = check_value
        return return_value
