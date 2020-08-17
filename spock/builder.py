# -*- coding: utf-8 -*-

# Copyright 2019 FMR LLC <opensource@fidelity.com>
# SPDX-License-Identifier: Apache-2.0

"""Handles the building/saving of the configurations from the Spock config classes"""

import argparse
from pathlib import Path
import sys
from spock.saver import Saver


from abc import ABC
from abc import abstractmethod
import attr
from spock.backend.attr.builder import AttrBuilder
from spock.backend.attr.payload import AttrPayload
from spock.backend.dataclass.builder import DataClassBuilder
from spock.backend.dataclass.payload import DataClassPayload
from spock.backend.dataclass._dataclasses import is_dataclass


class BaseBuilder(ABC):
    def __init__(self, *args, configs=None, create_save_path=False, desc='', no_cmd_line=False, **kwargs):
        self._configs = configs
        self._create_save_path = create_save_path
        self._desc = desc
        self._no_cmd_line = no_cmd_line
        self._save_path = None

    @abstractmethod
    def print_usage_and_exit(self, msg=None, sys_exit=True):
        """Prints the help message and exits

        *Args*:

            msg: message to print pre exit

        *Returns*:

            None

        """
        pass

    @abstractmethod
    def generate(self, dict_args):
        """Method to auto-generate the actual class instances from the generated args

        Based on the generated arguments groups and the args read in from the config file(s)
        this function instantiates the classes with the necessary field or attr values

        *Args*:

            dict_args: dictionary of arguments from the configs

        *Returns*:

            namespace containing automatically generated instances of the classes
        """
        pass


class ConfigArgBuilder:
    def __init__(self, *args, configs=None, create_save_path=False, desc='', no_cmd_line=False, **kwargs):
        backend = self._set_backend(args)
        self._builder_obj = backend.get('builder')(
            *args, configs=configs, create_save_path=create_save_path, desc=desc, no_cmd_line=no_cmd_line, **kwargs)
        self._payload_obj = backend.get('payload')
        try:
            self._dict_args = self._get_payload()
            self._arg_namespace = self._builder_obj.generate(self._dict_args)
        except ValueError as e:
            self._builder_obj.print_usage_and_exit(str(e), sys_exit=False)
            raise ValueError(e)

    def __call__(self, *args, **kwargs):
        """Call to self to allow chaining

        *Args*:

            *args:
            **kwargs:

        *Returns*:

            ConfigArgBuilder: self instance
        """
        return ConfigArgBuilder(*args, **kwargs)

    def generate(self):
        """Generate method that returns the actual argument namespace

        *Returns*:

            argument namespace consisting of all config classes

        """
        return self._arg_namespace

    @staticmethod
    def _set_backend(args):
        """Determines which backend class to use

        *Args*:

            args: list of classes passed to the builder

        *Returns*:

            backend: class of backend

        """
        # Gather if all attr backend
        type_attrs = all([attr.has(arg) for arg in args])
        # Gather if all dataclass backend
        type_dataclass = all([is_dataclass(arg) for arg in args])
        if (not type_attrs) and (not type_dataclass):
            raise TypeError(f"*args must be of all attrs backend or dataclass backend")
        elif type_attrs:
            backend = {'builder': AttrBuilder, 'payload': AttrPayload}
        elif type_dataclass:
            backend = {'builder': DataClassBuilder, 'payload': DataClassPayload}
        else:
            raise TypeError(f"*args must be of all attrs backend or dataclass backend")
        return backend

    def _get_config_paths(self):
        """Get config paths from all methods

        Config paths can enter from either the command line or be added in the class init call
        as a kwarg (configs=[])

        *Returns*:

            args: namespace of args

        """
        # Check if the no_cmd_line is not flagged and if the configs are not empty

        if self._no_cmd_line and (self._configs is None):
            raise ValueError("Flag set for preventing command line read but no paths were passed to the config kwarg")
        if not self._no_cmd_line:
            args = self._get_from_arg_parser(self._desc)
        else:
            args = argparse.Namespace(config=[], help=False)
        if self._configs is not None:
            args = self._get_from_kwargs(args, self._configs)
        return args

    @staticmethod
    def _get_from_arg_parser(desc):
        """Get configs from command line

        Gets the config file(s) from the command line arg parser

        *Args*:

            desc: description text for the cmd line argparser

        *Returns*:

            args: namespace of command line args

        """
        # Pull in args via the arg parser pointing to the config file
        parser = argparse.ArgumentParser(description=desc, add_help=False)
        parser.add_argument('-c', '--config', required=False, nargs='+', default=[])
        parser.add_argument('-h', '--help', action='store_true')
        args, _ = parser.parse_known_args(sys.argv)
        return args

    @staticmethod
    def _get_from_kwargs(args, configs):
        """Get configs from the configs kwarg


        *Args*:

            args: argument namespace
            configs: config kwarg

        *Returns*:

            args: arg namespace

        """
        if type(configs).__name__ == 'list':
            args.config.extend(configs)
        else:
            raise TypeError('configs kwarg must be of type list')
        return args

    def _get_payload(self):
        """Get the parameter payload from the config file(s)

        Calls the various ways to get configs and then parses to retrieve the parameter payload

        *Returns*:

            payload: dictionary of parameter values

        """
        args = self._get_config_paths()
        if args.help:
            self._builder_obj.print_usage_and_exit()
        payload = {}
        for configs in args.config:
            pass
            payload.update(self._payload_obj().payload(self._builder_obj.input_classes, configs))
        return payload





# class ConfigArgBuilder:
#     """Automatically generates dataclass instances from config file(s)
#
#     This class builds out necessary arguments from *args dataclasses, reads
#     the arguments from specified config file(s), and subsequently (via chained
#     call to generate) generates each class instance based on the necessary
#     field values for each dataclass
#
#     *Attributes*:
#
#         _arg_namespace: generated argument namespace
#         _configs: None or List of configs to read from
#         _create_save_path: boolean to make the path to save to
#         _data_classes: all of the data classes from *args
#         _desc: description for the arg parser
#         _dict_args: dictionary args from the command line
#         _no_cmd_line: flag to force no command line reads
#         _optional_types: Dictionary that holds the names of types that are
#         optional
#         _save_path: list of path(s) to save the configs to
#
#     """
#     def __init__(self, *args, configs=None, create_save_path=False, desc='', no_cmd_line=False, **kwargs):
#         self._save_path = None
#         self._optional_types = {'FloatOptArg', 'IntOptArg', 'StrOptArg',
#                                 'ListOptArg', 'TupleOptArg', 'SavePathOptArg'}
#         self._data_classes = args
#         for arg in self._data_classes:
#             if not is_dataclass(arg):
#                 raise TypeError('*arg inputs to ConfigArgBuilder must all be instances of @dataclass')
#         self._configs = configs
#         self._create_save_path = create_save_path
#         self._desc = desc
#         self._no_cmd_line = no_cmd_line
#         try:
#             self._dict_args = self._get_payload()
#             self._arg_namespace = self._generate()
#         except ValueError as e:
#             self.print_usage_and_exit(str(e), sys_exit=False)
#             raise ValueError(e)
#
#     def print_usage_and_exit(self, msg=None, sys_exit=True):
#         """Prints the help message and exits
#
#         *Args*:
#
#             msg: message to print pre exit
#
#         *Returns*:
#
#             None
#
#         """
#         print('USAGE:')
#         print(f'  {sys.argv[0]} -c [--config] config1 [config2, config3, ...]')
#         print('CONFIG:')
#         for data_class in self._data_classes:
#             print('  ' + data_class.__name__ + ':')
#             dc_vars = vars(data_class)
#             for key, val in dc_vars.get('__dataclass_fields__').items():
#                 if type(val.type).__name__ == 'ChoiceArg':
#                     type_name = type(val.type).__name__
#                 # Magic again -- check for type == type allows for delineation between basic types and list/tuples
#                 elif type(val.type) == type:
#                     type_name = val.type.__name__
#                 else:
#                     type_name = val.type.__origin__.__name__
#                     type_name += '[' + self._extract_base_type(val.type).__name__ + ']'
#                 print(f'    {key}: {type_name}')
#         if msg is not None:
#             print(msg)
#         if sys_exit:
#             sys.exit(1)
#
#     def _get_config_paths(self):
#         """Get config paths from all methods
#
#         Config paths can enter from either the command line or be added in the class init call
#         as a kwarg (configs=[])
#
#         *Returns*:
#
#             args: namespace of args
#
#         """
#         # Check if the no_cmd_line is not flagged and if the configs are not empty
#
#         if self._no_cmd_line and (self._configs is None):
#             raise ValueError("Flag set for preventing command line read but no paths were passed to the config kwarg")
#         if not self._no_cmd_line:
#             args = self._get_from_arg_parser(self._desc)
#         else:
#             args = Namespace(config=[], help=False)
#         if self._configs is not None:
#             args = self._get_from_kwargs(args, self._configs)
#         return args
#
#     @staticmethod
#     def _get_from_arg_parser(desc):
#         """Get configs from command line
#
#         Gets the config file(s) from the command line arg parser
#
#         *Args*:
#
#             desc: description text for the cmd line argparser
#
#         *Returns*:
#
#             args: namespace of command line args
#
#         """
#         # Pull in args via the arg parser pointing to the config file
#         parser = argparse.ArgumentParser(description=desc, add_help=False)
#         parser.add_argument('-c', '--config', required=False, nargs='+', default=[])
#         parser.add_argument('-h', '--help', action='store_true')
#         args, _ = parser.parse_known_args(sys.argv)
#         return args
#
#     @staticmethod
#     def _get_from_kwargs(args, configs):
#         """Get configs from the configs kwarg
#
#
#         *Args*:
#
#             args: argument namespace
#             configs: config kwarg
#
#         *Returns*:
#
#             args: arg namespace
#
#         """
#         if type(configs).__name__ == 'list':
#             args.config.extend(configs)
#         else:
#             raise TypeError('configs kwarg must be of type list')
#         return args
#
#     def _get_payload(self):
#         """Get the parameter payload from the config file(s)
#
#         Calls the various ways to get configs and then parses to retrieve the parameter payload
#
#         *Returns*:
#
#             payload: dictionary of parameter values
#
#         """
#         args = self._get_config_paths()
#         if args.help:
#             self.print_usage_and_exit()
#         payload = {}
#         for configs in args.config:
#             payload.update(Payload().payload(self._data_classes, configs))
#         return payload
#
#     def __call__(self, *args, **kwargs):
#         """Call to self to allow chaining
#
#         *Args*:
#
#             *args:
#             **kwargs:
#
#         *Returns*:
#
#             ConfigArgBuilder: self instance
#         """
#         return ConfigArgBuilder(*args, **kwargs)
#
#     def _generate(self):
#         """Method to auto-generate the actual class instances from the generated args
#
#         Based on the generated arguments groups and the args read in from the config file(s)
#         this function instantiates the dataclass configs with the necessary field values
#
#         *Returns*:
#
#             auto_dc: namespace containing automatically generated instances of dataclasses
#         """
#         auto_dc = {}
#         for data_classes in self._data_classes:
#             dc_build = self._auto_generate(self._dict_args, data_classes)
#             auto_dc.update({type(dc_build).__name__: dc_build})
#         return Namespace(**auto_dc)
#
#     def generate(self):
#         """Generate method that returns the actual argument namespace
#
#         *Returns*:
#
#             argument namespace consisting of all config classes
#
#         """
#         return self._arg_namespace
#
#     def save(self, user_specified_path=None, extra_info=True, file_extension='.yaml'):
#         """Saves the current config setup to file with a UUID
#
#         *Args*:
#
#             user_specified_path: if user provides a path it will be used as the path to write
#             extra_info: additional info to write to saved config (run date and git info)
#             file_extension: file type to write (default: yaml)
#
#         *Returns*:
#
#             self so that functions can be chained
#         """
#         if user_specified_path is not None:
#             save_path = Path(user_specified_path)
#         elif self._save_path is not None:
#             save_path = Path(self._save_path)
#         else:
#             raise ValueError('Save did not receive a valid path from: (1) SavePathOptArg or (2) '
#                              'the user via user_specified_path')
#         # Call the saver class and save function
#         Saver().save(self._arg_namespace, save_path, self._create_save_path, extra_info, file_extension)
#         return self
#
#     def _auto_generate(self, args, data_class):
#         """Builds an instance of a DataClass
#
#         Builds an instance of a dataclass with the necessary field values from the argument
#         dictionary read from the config file(s)
#
#         *Args*:
#
#             args: dictionary of arguments read from the config file(s)
#             data_class: data class to build
#
#         *Returns*:
#
#             An instance of data_class with correct values assigned to fields
#         """
#         # Handle the basic data types
#         fields = self._handle_basic_arguments(args, data_class)
#         return data_class(**fields)
#
#     def _handle_basic_arguments(self, args, data_class):
#         """Handles all base types
#
#         These can be easily mapped from the dataclass to another dataclass by some var inspection
#
#         *Args*:
#
#             args: read file arguments
#             data_class: instance of a dataclass
#
#         *Returns*:
#
#             fields: dictionary of mapped parameters
#
#         """
#         fields = {}
#         # Access the vars
#         dc_vars = vars(data_class)
#         # Get the dataclass name
#         dc_name = data_class.__name__
#         for key, val in dc_vars.get('__dataclass_fields__').items():
#             # pure magic -- Lists, Tuples, etc. are not of type type (they are GenericAlias) so one must
#             # check against this before accessing the __name__ attribute which GenericAlias does not have
#             if type(val.type) == type:
#                 if val.type.__name__ == 'SavePathOptArg':
#                     self._save_path = args.get(key)
#             # Check if namespace is named and then check for key -- checking for local def
#             if dc_name in args and key in args[dc_name]:
#                 fields[key] = self._check_function(args[dc_name][key], val)
#             # If not named then just check for keys -- checking for global def
#             elif key in args:
#                 fields[key] = self._check_function(args[key], val)
#             # If not found then fallback on defaults if defined
#             else:
#                 default, found_default = self.check_for_defaults(val)
#                 if not found_default:
#                     if type(val.type) == type and val.type.__name__ in self._optional_types:
#                         fields[key] = None
#                         continue
#                     elif type(val.type) != type and val.type.__origin__.__name__ in self._optional_types:
#                         fields[key] = None
#                         continue
#                     elif 'Bool' in val.type.__name__:
#                         fields[key] = False
#                         continue
#                     else:
#                         raise ValueError(f'Required value {dc_name}.{key}: no default set or value defined in file')
#                 fields[key] = self._check_function(default, val)
#         return fields
#
#     @staticmethod
#     def _int_to_float(inst, target_type):
#         """Converts instance int to float
#
#         *Args*:
#             inst: instance
#             target_type: target type
#
#         *Returns*:
#             inst: instance type cast into float
#
#         """
#         if target_type == float and type(inst) == int:
#             inst = float(inst)
#         return inst
#
#     def _check_function(self, x, val):
#         """Wrapper around the valid type check with a cast
#
#         *Args*:
#
#             x: instance
#             val: value
#
#         *Returns*:
#
#             casted value
#
#         """
#         return cast(self._check_valid_type(x, val))
#
#     def _check_valid_type(self, instance, val):
#         """Checks that the instance is of the correct type
#
#         *Args*:
#
#             instance: object instance
#             val: value
#
#         *Returns*:
#
#             instance: object instance
#
#         """
#         if type(val.type) == type:
#             # pure magic -- Lists, Tuples, etc. are not of type type (they are GenericAlias) so one must
#             # check against this before accessing the __name__ attribute which GenericAlias does not have
#             # Get the base variable type
#             var_type = val.type.__bases__[0]
#             instance = self._int_to_float(instance, var_type)
#             valid = isinstance(instance, var_type)
#             if not valid:
#                 raise ValueError(f'Wrong type ({type(instance)}) passed to {val.name}. Require {var_type}')
#         elif type(val.type).__name__ == 'ChoiceArg':
#             instance = self._check_choice_type(val.type, instance)
#             var_type = val.type.set_type
#             valid = isinstance(instance, var_type)
#             if not valid:
#                 raise ValueError(f'Wrong type ({type(instance)}) passed to {val.name}. Require {var_type}')
#         else:
#             # It's an iterable - check it's a list (only iterable provided by markup)
#             var_type = self._extract_base_type(val.type)
#             iter_name = val.type.__origin__.__name__
#             valid = isinstance(instance, (tuple, list))
#             if not valid:
#                 raise ValueError(
#                     f'Wrong type ({type(instance).__name__}) passed to {val.name}.\n'
#                     f'Require {iter_name}[{var_type.__name__}]')
#             instance = tuple((self._int_to_float(i, var_type) for i in instance))
#             if len(instance) > 0:
#                 valid = isinstance(instance[0], var_type)
#                 if not valid:
#                     raise ValueError(
#                         f'Wrong type (List[{type(instance[0]).__name__}]) passed to {val.name}.\n'
#                         f'Require {iter_name}[{var_type.__name__}]')
#         return instance
#
#     @staticmethod
#     def _extract_base_type(given_type):
#         """Extracts the type from a _GenericAlias
#
#         *Args*:
#
#             tp: type
#
#         *Returns*:
#
#             tp: type of generic type
#         """
#         if isinstance(given_type, _GenericAlias) and given_type is not Generic:
#             return given_type.__args__[0]  # assume we only have generic types with a single argument
#         return given_type
#
#     def check_for_defaults(self, val):
#         """Checks for default values
#
#         *Args*:
#
#             default: default value
#             default_factory: default factory
#
#         *Returns*:
#
#             default_val: value of default
#             found_default: boolean if default found
#
#         """
#         found_default = False
#         default_val = None
#         if type(val.type).__name__ == 'ChoiceArg':
#             default_val = self._check_choice_type(val.type, val.type.default)
#             found_default = True
#         elif type(val.default).__name__ != '_MISSING_TYPE':
#             default_val = val.default
#             found_default = True
#         elif type(val.default_factory).__name__ != '_MISSING_TYPE':
#             default_val = val.default_factory()
#             found_default = True
#         return default_val, found_default
#
#     @staticmethod
#     def _check_choice_type(choice_set, val):
#         """Checks the type and set of a ChoiceArg value
#
#         *Args*:
#
#             choice_set: ChoiceArg instance
#             val: value to set
#             val_name: name of the parameter
#
#         *Returns*:
#
#             val: value to set
#
#         """
#         if val not in choice_set.choice_set:
#             raise ValueError(f'{val} is not within the set of defined choices {choice_set.choice_set}')
#         return val
