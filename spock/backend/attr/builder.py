# -*- coding: utf-8 -*-

# Copyright 2019 FMR LLC <opensource@fidelity.com>
# SPDX-License-Identifier: Apache-2.0

"""Handles the building/saving of the configurations from the Spock config classes"""

import attr
from spock.backend.base import BaseBuilder
import sys


class AttrBuilder(BaseBuilder):
    def __init__(self, *args, configs=None, create_save_path=False, desc='', no_cmd_line=False, **kwargs):
        super().__init__(*args, configs=configs, create_save_path=create_save_path, desc=desc,
                                               no_cmd_line=no_cmd_line, **kwargs)
        for arg in self.input_classes:
            if not attr.has(arg):
                raise TypeError('*arg inputs to ConfigArgBuilder must all be class instances with attrs attributes')

    def print_usage_and_exit(self, msg=None, sys_exit=True):
        print('USAGE:')
        print(f'  {sys.argv[0]} -c [--config] config1 [config2, config3, ...]')
        print('CONFIG:')
        for attrs_class in self.input_classes:
            print('  ' + attrs_class.__name__ + ':')
            for val in attrs_class.__attrs_attrs__:
                type_string = val.metadata['base']
                if 'type' in val.metadata:
                    type_string += "[{0}]".format(val.metadata['type'])
                # Construct the type with the metadata
                if 'optional' in val.metadata:
                    type_string = "Optional[{0}]".format(type_string)
                print(f'    {val.name}: {type_string}')
        if msg is not None:
            print(msg)
        if sys_exit:
            sys.exit(1)

    def _handle_arguments(self, args, class_obj):
        attr_name = class_obj.__name__
        fields = {}
        for val in class_obj.__attrs_attrs__:
            # Check if namespace is named and then check for key -- checking for local class def
            if attr_name in args and val.name in args[attr_name]:
                fields[val.name] = args[attr_name][val.name]
            # If not named then just check for keys -- checking for global def
            elif val.name in args:
                fields[val.name] = args[val.name]
        return fields
