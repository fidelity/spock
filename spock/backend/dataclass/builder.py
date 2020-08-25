# -*- coding: utf-8 -*-

# Copyright 2019 FMR LLC <opensource@fidelity.com>
# SPDX-License-Identifier: Apache-2.0

"""Handles the building/saving of the configurations from the Spock config classes"""

import sys
from typing import Generic
from spock.backend.dataclass._dataclasses import is_dataclass
from spock.backend.base import BaseBuilder
from spock.backend.dataclass.utils import cast
minor = sys.version_info.minor
if minor < 7:
    from typing import GenericMeta as _GenericAlias
else:
    from typing import _GenericAlias


class DataClassBuilder(BaseBuilder):
    """Dataclass specific builder

    Class that handles building for the dataclass backend

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
        self._optional_types = {'FloatOptArg', 'IntOptArg', 'StrOptArg',
                                'ListOptArg', 'TupleOptArg', 'SavePathOptArg'}
        for arg in self.input_classes:
            if not is_dataclass(arg):
                raise TypeError('*arg inputs to ConfigArgBuilder must all be instances of dataclass')

    def print_usage_and_exit(self, msg=None, sys_exit=True):
        print('USAGE:')
        print(f'  {sys.argv[0]} -c [--config] config1 [config2, config3, ...]')
        print('CONFIG:')
        for data_class in self.input_classes:
            print('  ' + data_class.__name__ + ':')
            dc_vars = vars(data_class)
            for key, val in dc_vars.get('__dataclass_fields__').items():
                if type(val.type).__name__ == 'ChoiceArg':
                    type_name = type(val.type).__name__
                # Magic again -- check for type == type allows for delineation between basic types and list/tuples
                elif type(val.type) == type:
                    type_name = val.type.__name__
                else:
                    type_name = val.type.__origin__.__name__
                    type_name += '[' + self._extract_base_type(val.type).__name__ + ']'
                print(f'    {key}: {type_name}')
        if msg is not None:
            print(msg)
        if sys_exit:
            sys.exit(1)

    def _handle_arguments(self, args, class_obj):
        fields = {}
        # Access the vars
        dc_vars = vars(class_obj)
        # Get the dataclass name
        dc_name = class_obj.__name__
        for key, val in dc_vars.get('__dataclass_fields__').items():
            # pure magic -- Lists, Tuples, etc. are not of type type (they are GenericAlias) so one must
            # check against this before accessing the __name__ attribute which GenericAlias does not have
            if type(val.type) == type:
                if val.type.__name__ == 'SavePathOptArg':
                    self.save_path = args.get(key)
            # Check if namespace is named and then check for key -- checking for local def
            if dc_name in args and key in args[dc_name]:
                fields[key] = self._check_function(args[dc_name][key], val)
            # If not named then just check for keys -- checking for global def
            elif key in args:
                fields[key] = self._check_function(args[key], val)
            # If not found then fallback on defaults if defined
            else:
                default, found_default = self.check_for_defaults(val)
                if not found_default:
                    if type(val.type) == type and val.type.__name__ in self._optional_types:
                        fields[key] = None
                        continue
                    elif type(val.type) != type and val.type.__origin__.__name__ in self._optional_types:
                        fields[key] = None
                        continue
                    elif 'Bool' in val.type.__name__:
                        fields[key] = False
                        continue
                    else:
                        raise ValueError(f'Required value {dc_name}.{key}: no default set or value defined in file')
                fields[key] = self._check_function(default, val)
        return fields

    @staticmethod
    def _int_to_float(inst, target_type):
        """Converts instance int to float

        *Args*:
            inst: instance
            target_type: target type

        *Returns*:
            inst: instance type cast into float

        """
        if target_type == float and type(inst) == int:
            inst = float(inst)
        return inst

    def _check_function(self, x, val):
        """Wrapper around the valid type check with a cast

        *Args*:

            x: instance
            val: value

        *Returns*:

            casted value

        """
        return cast(self._check_valid_type(x, val))

    def _check_valid_type(self, instance, val):
        """Checks that the instance is of the correct type

        *Args*:

            instance: object instance
            val: value

        *Returns*:

            instance: object instance

        """
        if type(val.type) == type:
            # pure magic -- Lists, Tuples, etc. are not of type type (they are GenericAlias) so one must
            # check against this before accessing the __name__ attribute which GenericAlias does not have
            # Get the base variable type
            var_type = val.type.__bases__[0]
            instance = self._int_to_float(instance, var_type)
            valid = isinstance(instance, var_type)
            if not valid:
                raise ValueError(f'Wrong type ({type(instance)}) passed to {val.name}. Require {var_type}')
        elif type(val.type).__name__ == 'ChoiceArg':
            instance = self._check_choice_type(val.type, instance)
            var_type = val.type.set_type
            valid = isinstance(instance, var_type)
            if not valid:
                raise ValueError(f'Wrong type ({type(instance)}) passed to {val.name}. Require {var_type}')
        else:
            # It's an iterable - check it's a list (only iterable provided by markup)
            var_type = self._extract_base_type(val.type)
            iter_name = val.type.__origin__.__name__
            valid = isinstance(instance, (tuple, list))
            if not valid:
                raise ValueError(
                    f'Wrong type ({type(instance).__name__}) passed to {val.name}.\n'
                    f'Require {iter_name}[{var_type.__name__}]')
            instance = tuple((self._int_to_float(i, var_type) for i in instance))
            if len(instance) > 0:
                valid = isinstance(instance[0], var_type)
                if not valid:
                    raise ValueError(
                        f'Wrong type (List[{type(instance[0]).__name__}]) passed to {val.name}.\n'
                        f'Require {iter_name}[{var_type.__name__}]')
        return instance

    @staticmethod
    def _extract_base_type(given_type):
        """Extracts the type from a _GenericAlias

        *Args*:

            tp: type

        *Returns*:

            tp: type of generic type
        """
        if isinstance(given_type, _GenericAlias) and given_type is not Generic:
            return given_type.__args__[0]  # assume we only have generic types with a single argument
        return given_type

    def check_for_defaults(self, val):
        """Checks for default values

        *Args*:

            default: default value
            default_factory: default factory

        *Returns*:

            default_val: value of default
            found_default: boolean if default found

        """
        found_default = False
        default_val = None
        if type(val.type).__name__ == 'ChoiceArg':
            default_val = self._check_choice_type(val.type, val.type.default)
            found_default = True
        elif type(val.default).__name__ != '_MISSING_TYPE':
            default_val = val.default
            found_default = True
        elif type(val.default_factory).__name__ != '_MISSING_TYPE':
            default_val = val.default_factory()
            found_default = True
        return default_val, found_default

    @staticmethod
    def _check_choice_type(choice_set, val):
        """Checks the type and set of a ChoiceArg value

        *Args*:

            choice_set: ChoiceArg instance
            val: value to set
            val_name: name of the parameter

        *Returns*:

            val: value to set

        """
        if val not in choice_set.choice_set:
            raise ValueError(f'{val} is not within the set of defined choices {choice_set.choice_set}')
        return val
