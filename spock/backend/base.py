# -*- coding: utf-8 -*-

# Copyright 2019 FMR LLC <opensource@fidelity.com>
# SPDX-License-Identifier: Apache-2.0

"""Handles base Spock classes"""

from abc import ABC
from abc import abstractmethod
import argparse
import os
from pathlib import Path
import sys
from uuid import uuid1
from spock.handlers import JSONHandler
from spock.handlers import TOMLHandler
from spock.handlers import YAMLHandler
from spock.utils import add_info
from spock.utils import make_argument


class BaseSaver(ABC):  # pylint: disable=too-few-public-methods
    """Base class for saving configs

    Contains methods to build a correct output payload and then writes to file based on the file
    extension

    *Attributes*:

        _writers: maps file extension to the correct i/o handler

    """
    def __init__(self):
        self._writers = {'.yaml': YAMLHandler, '.toml': TOMLHandler, '.json': JSONHandler}

    def save(self, payload, path, create_save_path=False, extra_info=True, file_extension='.yaml'):  #pylint: disable=too-many-arguments
        """Writes Spock config to file

        Cleans and builds an output payload and then correctly writes it to file based on the
        specified file extension

        *Args*:

            payload: current config payload
            path: path to save
            create_save_path: boolean to create the path if non-existent
            extra_info: boolean to write extra info
            file_extension: what type of file to write

        *Returns*:

            None

        """
        supported_extensions = list(self._writers.keys())
        if file_extension not in list(self._writers.keys()):
            raise ValueError(f'Invalid fileout extension. Expected a fileout from {supported_extensions}')
        # Make the filename
        name = str(uuid1()) + '.spock.cfg' + file_extension
        fid = path / name
        # Fix up values
        out_dict = self._clean_up_values(payload, extra_info, file_extension)
        try:
            if not os.path.exists(path) and create_save_path:
                os.makedirs(path)
            with open(fid, 'w') as file_out:
                self._writers.get(file_extension)().save(out_dict, file_out)
        except OSError as e:
            print(f'Not a valid file path to write to: {fid}')
            raise e

    @abstractmethod
    def _clean_up_values(self, payload, extra_info, file_extension):
        """Clean up the config payload so it can be written to file

        *Args*:

            payload: dirty payload
            extra_info: boolean to add extra info
            file_extension: type of file to write

        *Returns*:

            clean_dict: cleaned output payload

        """

    @staticmethod
    def _clean_output(out_dict, extra_info):
        """Clean up the dictionary so it can be written to file

        *Args*:

            out_dict: cleaned dictionary
            extra_info: boolean to add extra info

        *Returns*:

            clean_dict: cleaned output payload

        """
        # Convert values
        clean_dict = {}
        for key, val in out_dict.items():
            clean_inner_dict = {}
            for inner_key, inner_val in val.items():
                # Convert tuples to lists so they get written correctly
                if isinstance(inner_val, tuple):
                    clean_inner_dict.update({inner_key: list(inner_val)})
                elif inner_val is not None:
                    clean_inner_dict.update({inner_key: inner_val})
            clean_dict.update({key: clean_inner_dict})
        if extra_info:
            clean_dict = add_info(clean_dict)
        return clean_dict


class BaseBuilder(ABC):  # pylint: disable=too-few-public-methods
    """Base class for building the backend specific builders

    This class handles the interface to the backend with the generic ConfigArgBuilder so that different
    backends can be used to handle processing

    *Attributes*

        input_classes: list of input classes that link to a backend
        _configs: None or List of configs to read from
        _create_save_path: boolean to make the path to save to
        _desc: description for the arg parser
        _no_cmd_line: flag to force no command line reads
        save_path: list of path(s) to save the configs to

    """
    def __init__(self, *args, configs=None, create_save_path=False, desc='', no_cmd_line=False, **kwargs):
        self.input_classes = args
        self._configs = configs
        self._create_save_path = create_save_path
        self._desc = desc
        self._no_cmd_line = no_cmd_line
        self.save_path = None

    @abstractmethod
    def print_usage_and_exit(self, msg=None, sys_exit=True):
        """Prints the help message and exits

        *Args*:

            msg: message to print pre exit

        *Returns*:

            None

        """

    @abstractmethod
    def _handle_arguments(self, args, class_obj):
        """Handles all argument mapping

        Creates a dictionary of named parameters that are mapped to the final type of object

        *Args*:

            args: read file arguments
            class_obj: instance of a class obj

        *Returns*:

            fields: dictionary of mapped parameters

        """

    def generate(self, dict_args):
        """Method to auto-generate the actual class instances from the generated args

        Based on the generated arguments groups and the args read in from the config file(s)
        this function instantiates the classes with the necessary field or attr values

        *Args*:

            dict_args: dictionary of arguments from the configs

        *Returns*:

            namespace containing automatically generated instances of the classes
        """
        auto_dict = {}
        for attr_classes in self.input_classes:
            attr_build = self._auto_generate(dict_args, attr_classes)
            auto_dict.update({type(attr_build).__name__: attr_build})
        return argparse.Namespace(**auto_dict)

    def _auto_generate(self, args, input_class):
        """Builds an instance of a DataClass

        Builds an instance of a dataclass with the necessary field values from the argument
        dictionary read from the config file(s)

        *Args*:

            args: dictionary of arguments read from the config file(s)
            data_class: data class to build

        *Returns*:

            An instance of data_class with correct values assigned to fields
        """
        # Handle the basic data types
        fields = self._handle_arguments(args, input_class)
        return input_class(**fields)

    def get_config_paths(self):
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
            args = self._build_override_parsers(desc=self._desc)
        else:
            args = argparse.Namespace(config=[], help=False)
        if self._configs is not None:
            args = self._get_from_kwargs(args, self._configs)
        return args

    def _build_override_parsers(self, desc):
        """Creates parsers for command-line overrides

        Builds the basic command line parser for configs and help, iterates through all defined attr to make
        a general override parser, and then iterates through each attr instance to make namespace specific override
        parsers

        *Args*:

            desc: argparser description

        *Returns*:

            args: argument namespace

        """
        parser = argparse.ArgumentParser(description=desc, add_help=False)
        parser.add_argument('-c', '--config', required=False, nargs='+', default=[])
        parser.add_argument('-h', '--help', action='store_true')
        # Build out a general parser for parent level attr
        parser = self._make_general_override_parser(parser=parser, input_classes=self.input_classes)
        # Build out each class specific parser
        for val in self.input_classes:
            parser = self._make_group_override_parser(parser=parser, class_obj=val)
        # args = parser.parse_args()
        args, _ = parser.parse_known_args(sys.argv)
        return args

    def _make_general_override_parser(self, parser, input_classes):
        """Makes a general level override parser

        Flattens all the attrs into a single dictionary and makes a general level parser for the attr name

        *Args*:

            parser: argument parser
            input_classes: list of input classes for a specific backend

        *Returns*:

            parser: argument parser with new general overrides

        """
        # Make all names list
        all_attr = {}
        for class_obj in input_classes:
            for val in class_obj.__attrs_attrs__:
                val_type = val.metadata['type'] if 'type' in val.metadata else val.type
                if hasattr(all_attr, val.name):
                    if all_attr[val.name] is not val_type:
                        print(f"Warning: Ignoring general override for {val.name} as the class specific types differ")
                else:
                    all_attr.update({val.name: val_type})
        self._check_protected_keys(all_attr)
        group_parser = parser.add_argument_group(title="General Overrides")
        for k, v in all_attr.items():
            arg_name = '--' + k
            group_parser = make_argument(arg_name, v, group_parser)
        return parser

    @staticmethod
    def _make_group_override_parser(parser, class_obj):
        """Makes a name specific override parser for a given class obj

        Takes a class object of the backend and adds a new argument group with argument names given with name
        Class.name so that individual parameters specific to a class can be overridden.

        *Args*:

            parser: argument parser
            class_obj: instance of a backend class

        *Returns*:

            parser: argument parser with new class specific overrides

        """
        attr_name = class_obj.__name__
        group_parser = parser.add_argument_group(title=str(attr_name) + " Specific Overrides")
        for val in class_obj.__attrs_attrs__:
            val_type = val.metadata['type'] if 'type' in val.metadata else val.type
            arg_name = '--' + str(attr_name) + '.' + val.name
            group_parser = make_argument(arg_name, val_type, group_parser)
        return parser

    @staticmethod
    def _check_protected_keys(all_attr):
        """Test for protected keys

        Tests to see if an attribute has been defined at the genreral level that is within the protected list that
        would break basic command line handling.

        Args:
            all_attr: dictionary of all attr

        """
        protected_names = ['config', 'help']
        if any([val in all_attr.keys() for val in protected_names]):
            raise ValueError(f"Using a protected name from {protected_names} at general class level which prevents "
                             f"command line overrides")

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


class BasePayload(ABC):  # pylint: disable=too-few-public-methods
    """Handles building the payload for config file(s)

    This class builds out the payload from config files of multiple types. It handles various
    file types and also composition of config files via a recursive calls

    *Attributes*:

        _loaders: maps of each file extension to the loader class

    """
    def __init__(self):
        self._loaders = {'.yaml': YAMLHandler(), '.toml': TOMLHandler(), '.json': JSONHandler()}

    @staticmethod
    @abstractmethod
    def _update_payload(base_payload, input_classes, payload):
        """Updates the payload

        Checks the parameters defined in the config files against the provided classes and if
        passable adds them to the payload

        *Args*:

            base_payload: current payload
            input_classes: class to roll into
            payload: total payload

        *Returns*:

            payload: updated payload

        """

    def payload(self, input_classes, path, cmd_args):
        """Builds the payload from config files

        Public exposed call to build the payload and set any command line overrides

        *Args*:

            input_classes: list of backend classes
            path: path to config file(s)
            cmd_args: command line overrides

        *Returns*:

            payload: dictionary of all mapped parameters

        """
        payload = self._payload(input_classes, path)
        payload = self._handle_overrides(payload, cmd_args)
        return payload

    def _payload(self, input_classes, path):
        """Private call to construct the payload

        Main function call that builds out the payload from config files of multiple types. It handles
        various file types and also composition of config files via a recursive calls

        *Args*:
            input_classes: list of backend classes
            path: path to config file(s)

        *Returns*:

            payload: dictionary of all mapped parameters

        """
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

    def _handle_includes(self, base_payload, config_extension, input_classes, path, payload):  # pylint: disable=too-many-arguments
        """Handles config composition

        For all of the config tags in the config file this function will recursively call the payload function
        with the composition path to get the additional payload(s) from the composed file(s)

        *Args*:

            base_payload: base payload that has a config kwarg
            config_extension: file type
            input_classes: defined backend classes
            path: path to base file
            payload: payload pulled from composed files

        *Returns*:

            payload: payload update from composed files

        """
        included_params = {}
        for inc_path in base_payload['config']:
            if not os.path.exists(inc_path):
                # maybe it's relative?
                abs_inc_path = os.path.join(os.path.dirname(path), inc_path)
            else:
                abs_inc_path = inc_path
            if not os.path.exists(abs_inc_path):
                raise RuntimeError(f'Could not find included {config_extension} file {inc_path}!')
            included_params.update(self._payload(input_classes, abs_inc_path))
        payload.update(included_params)
        return payload

    def _handle_overrides(self, payload, args):
        """Handle command line overrides

        Iterate through the command line override values, determine at what level to set them, and set them if possible

        *Args*:

            payload: current payload dictionary
            args: command line override args

        *Returns*:

            payload: updated payload dictionary with override values set

        """
        skip_keys = ['config', 'help']
        for k, v in vars(args).items():
            # If the name has a . then we are at the class level so we need to get the dict and check
            if len(k.split('.')) > 1:
                dict_key = k.split('.')[0]
                val_name = k.split('.')[1]
                if k not in skip_keys and v is not None:
                    # Handle bool types slightly differently as they are store_true
                    if isinstance(vars(args)[k], bool):
                        if vars(args)[k] is not False:
                            payload = self._dict_payload_override(payload, dict_key, val_name, v)
                    else:
                        payload = self._dict_payload_override(payload, dict_key, val_name, v)
            # else search the first level
            else:
                # Override the value in the payload if present
                if k not in skip_keys and v is not None:
                    # Handle bool types slightly differently as they are store_true
                    if isinstance(vars(args)[k], bool):
                        if vars(args)[k] is not False:
                            payload.update({k: v})
                    else:
                        payload.update({k: v})
        return payload

    @staticmethod
    def _dict_payload_override(payload, dict_key, val_name, value):
        """Updates the payload at the dictionary level

        First checks to see if there is an existing dictionary to insert into, if not creates an empty one. Then it
        inserts the updated value at the correct dictionary level

        Args:
            payload: current payload dictionary
            dict_key: dictionary key to check
            val_name: value name to update
            value: value to update

        Returns:

            payload: updated payload dictionary

        """
        if not hasattr(payload, dict_key):
            payload.update({dict_key: {}})
        payload[dict_key].update({val_name: value})
        return payload
