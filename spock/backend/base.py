# -*- coding: utf-8 -*-

# Copyright 2019 FMR LLC <opensource@fidelity.com>
# SPDX-License-Identifier: Apache-2.0

"""Handles base Spock classes"""

from abc import ABC
from abc import abstractmethod
import argparse
import os
from pathlib import Path
from spock.handlers import JSONHandler
from spock.handlers import TOMLHandler
from spock.handlers import YAMLHandler
from spock.utils import add_info
import sys
from uuid import uuid1


class BaseSaver(ABC):
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
        name = str(uuid1()) + '.spck.cfg' + file_extension
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
        pass

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
                if type(inner_val) == tuple:
                    clean_inner_dict.update({inner_key: list(inner_val)})
                elif inner_val is not None:
                    clean_inner_dict.update({inner_key: inner_val})
            clean_dict.update({key: clean_inner_dict})
        if extra_info:
            clean_dict = add_info(clean_dict)
        return clean_dict


class BaseBuilder(ABC):
    def __init__(self, *args, configs=None, create_save_path=False, desc='', no_cmd_line=False, **kwargs):
        self.input_classes = args
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
    def _handle_arguments(self, args, class_obj):
        """Handles all argument mapping

        Creates a dictionary of named parameters that are mapped to the final type of object

        *Args*:

            args: read file arguments
            class_obj: instance of a class obj

        *Returns*:

            fields: dictionary of mapped parameters

        """
        pass

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


class BasePayload(ABC):
    """Handles building the payload for config file(s)

    This class builds out the payload from config files of multiple types. It handles various
    file types and also composition of config files via a recursive calls

    *Attributes*:

        _loaders: maps of each file extension to the loader class

    """
    def __init__(self):
        self._loaders = {'.yaml': YAMLHandler(), '.toml': TOMLHandler(), '.json': JSONHandler()}

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

    def _handle_includes(self, base_payload, config_extension, input_classes, path,
                         payload):  # pylint: disable=too-many-arguments
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
