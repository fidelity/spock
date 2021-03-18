# -*- coding: utf-8 -*-

# Copyright 2019 FMR LLC <opensource@fidelity.com>
# SPDX-License-Identifier: Apache-2.0

"""Handles base Spock classes"""

from abc import ABC
from abc import abstractmethod
import argparse
from attr import NOTHING
from enum import EnumMeta
import os
from pathlib import Path
import re
import sys
from uuid import uuid1
import yaml
from spock.handlers import JSONHandler
from spock.handlers import TOMLHandler
from spock.handlers import YAMLHandler
from spock.utils import add_info
from spock.utils import make_argument


class Spockspace(argparse.Namespace):
    """Inherits from Namespace to implement a pretty print on the obj

    Overwrites the __repr__ method with a pretty version of printing

    """
    def __init__(self, **kwargs):
        super(Spockspace, self).__init__(**kwargs)

    def __repr__(self):
        # Remove aliases in YAML print
        yaml.Dumper.ignore_aliases = lambda *args: True
        return yaml.dump(self.__dict__, default_flow_style=False)


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
        if file_extension not in self._writers:
            raise ValueError(f'Invalid fileout extension. Expected a fileout from {supported_extensions}')
        # Make the filename
        name = str(uuid1()) + '.spock.cfg' + file_extension
        fid = path / name
        # Fix up values -- parameters
        out_dict = self._clean_up_values(payload, file_extension)
        # Get extra info
        extra_dict = add_info() if extra_info else None
        try:
            if not os.path.exists(path) and create_save_path:
                os.makedirs(path)
            with open(fid, 'w') as file_out:
                self._writers.get(file_extension)().save(out_dict, extra_dict, file_out)
        except OSError as e:
            print(f'Not a valid file path to write to: {fid}')
            raise e

    @abstractmethod
    def _clean_up_values(self, payload, file_extension):
        """Clean up the config payload so it can be written to file

        *Args*:

            payload: dirty payload
            extra_info: boolean to add extra info
            file_extension: type of file to write

        *Returns*:

            clean_dict: cleaned output payload

        """

    def _clean_output(self, out_dict):
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
            if isinstance(val, list):
                for idx, list_val in enumerate(val):
                    tmp_dict = {}
                    for inner_key, inner_val in list_val.items():
                        tmp_dict = self._convert(tmp_dict, inner_val, inner_key)
                    val[idx] = tmp_dict
                clean_inner_dict = val
            else:
                for inner_key, inner_val in val.items():
                    clean_inner_dict = self._convert(clean_inner_dict, inner_val, inner_key)
            clean_dict.update({key: clean_inner_dict})
        return clean_dict

    def _convert(self, clean_inner_dict, inner_val, inner_key):
        # Convert tuples to lists so they get written correctly
        if isinstance(inner_val, tuple):
            clean_inner_dict.update({inner_key: self._recursive_tuple_to_list(inner_val)})
        elif inner_val is not None:
            clean_inner_dict.update({inner_key: inner_val})
        return clean_inner_dict

    def _recursive_tuple_to_list(self, value):
        """Recursively turn tuples into lists

        Recursively looks through tuple(s) and convert to lists

        *Args*:

            value: value to check and set typ if necessary
            typed: type of the generic alias to check against

        *Returns*:

            value: updated value with correct type casts

        """
        # Check for __args__ as it signifies a generic and make sure it's not already been cast as a tuple
        # from a composed payload
        list_v = []
        for v in value:
            if isinstance(v, tuple):
                v = self._recursive_tuple_to_list(v)
                list_v.append(v)
            else:
                list_v.append(v)
        return list_v


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
        _max_indent: maximum to indent between help prints
        save_path: list of path(s) to save the configs to

    """
    def __init__(self, *args, configs=None, create_save_path=False, desc='', no_cmd_line=False,
                 max_indent=4, **kwargs):
        self.input_classes = args
        self._configs = configs
        self._create_save_path = create_save_path
        self._desc = desc
        self._no_cmd_line = no_cmd_line
        self._max_indent = max_indent
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
    def _handle_help_info(self):
        """Handles walking through classes to get help info

        For each class this function will search __doc__ and attempt to pull out help information for both the class
        itself and each attribute within the class

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
            if isinstance(attr_build, list):
                class_name = list({type(val).__name__ for val in attr_build})
                if len(class_name) > 1:
                    raise ValueError('Repeated class has more than one unique name')
                auto_dict.update({class_name[0]: attr_build})
            else:
                auto_dict.update({type(attr_build).__name__: attr_build})
        return Spockspace(**auto_dict)
        # return argparse.Namespace(**auto_dict)

    def _auto_generate(self, args, input_class):
        """Builds an instance of a DataClass

        Builds an instance with the necessary field values from the argument
        dictionary read from the config file(s)

        *Args*:

            args: dictionary of arguments read from the config file(s)
            data_class: data class to build

        *Returns*:

            An instance of data_class with correct values assigned to fields
        """
        # Handle the basic data types
        fields = self._handle_arguments(args, input_class)
        if isinstance(fields, list):
            return_value = fields
        else:
            self._handle_late_defaults(args, fields, input_class)
            return_value = input_class(**fields)
        return return_value

    def _handle_late_defaults(self, args, fields, input_class):
        """Handles late defaults when the type is non-standard

        If the default type is not a base python type then we need to catch those defaults here and build the correct
        values from the input classes while maintaining the optional nature. The trick is to exclude all 'base' types
        as these defaults are covered by the attr default value

        *Args*:

            args: dictionary of arguments read from the config file(s)
            fields: current fields returned from _handle_arguments
            input_class: which input class being checked for late defaults

        *Returns*:

            fields: updated field dictionary with late defaults set

        """
        names = [val.name for val in input_class.__attrs_attrs__]
        class_names = [val.__name__ for val in self.input_classes]
        field_list = list(fields.keys())
        arg_list = list(args.keys())
        # Exclude all the base types that are supported -- these can be set by attrs
        exclude_list = ['_Nothing', 'NoneType', 'bool', 'int', 'float', 'str', 'list', 'tuple']
        for val in names:
            if val not in field_list:
                default_type_name = type(getattr(input_class.__attrs_attrs__, val).default).__name__
                if default_type_name not in exclude_list:
                    default_name = getattr(input_class.__attrs_attrs__, val).default.__name__
                else:
                    default_name = None
                if default_name is not None and default_name in arg_list:
                    if isinstance(args.get(default_name), list):
                        default_value = [self.input_classes[class_names.index(default_name)](**arg_val)
                                         for arg_val in args.get(default_name)]
                    else:
                        default_value = self.input_classes[class_names.index(default_name)](**args.get(default_name))
                    fields.update({val: default_value})
        return fields

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
        if any([val in all_attr for val in protected_names]):
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

    @staticmethod
    def _find_attribute_idx(newline_split_docs):
        """Finds the possible split between the header and Attribute annotations

        *Args*:

            newline_split_docs:

        Returns:

            idx: -1 if none or the idx of Attributes

        """
        for idx, val in enumerate(newline_split_docs):
            re_check = re.search(r'(?i)Attribute?s?:', val)
            if re_check is not None:
                return idx
        return -1

    def _split_docs(self, obj):
        """Possibly splits head class doc string from attribute docstrings

        Attempts to find the first contiguous line within the Google style docstring to use as the class docstring.
        Splits the docs base on the Attributes tag if present.

        *Args*:

            obj: class object to rip info from

        *Returns*:

            class_doc: class docstring if present or blank str
            attr_doc: list of attribute doc strings

        """
        if obj.__doc__ is not None:
            # Split by new line
            newline_split_docs = obj.__doc__.split('\n')
            # Cleanup l/t whitespace
            newline_split_docs = [val.strip() for val in newline_split_docs]
        else:
            newline_split_docs = []
        # Find the break between the class docs and the Attribute section -- if this returns -1 then there is no
        # Attributes section
        attr_idx = self._find_attribute_idx(newline_split_docs)
        head_docs = newline_split_docs[:attr_idx] if attr_idx != -1 else newline_split_docs
        attr_docs = newline_split_docs[attr_idx:] if attr_idx != -1 else []
        # Grab only the first contiguous line as everything else will probably be too verbose (e.g. the
        # mid-level docstring that has detailed descriptions
        class_doc = ''
        for idx, val in enumerate(head_docs):
            class_doc += f' {val}'
            if idx + 1 != len(head_docs) and head_docs[idx + 1] == '':
                break
        # Clean up any l/t whitespace
        class_doc = class_doc.strip()
        return class_doc, attr_docs

    @staticmethod
    def _match_attribute_docs(attr_name, attr_docs, attr_type_str, attr_default=NOTHING):
        """Matches class attributes with attribute docstrings via regex

        *Args*:

            attr_name: attribute name
            attr_docs: list of attribute docstrings
            attr_type_str: str representation of the attribute type
            attr_default: str representation of a possible default value

        *Returns*:

            dictionary of packed attribute information

        """
        # Regex match each value
        a_str = None
        for a_doc in attr_docs:
            match_re = re.search(r'(?i)^' + attr_name + '?:', a_doc)
            # Find only the first match -- if more than one than ignore
            if match_re:
                a_str = a_doc[match_re.end():].strip()
        return {attr_name: {
            'type': attr_type_str,
            'desc': a_str if a_str is not None else "",
            'default': "(default: " + repr(attr_default) + ")" if type(attr_default).__name__ != '_Nothing'
            else "",
            'len': {'name': len(attr_name), 'type': len(attr_type_str)}
        }}

    def _handle_attributes_print(self, info_dict):
        """Prints attribute information in an argparser style format

        *Args*:

            info_dict: packed attribute info dictionary to print

        """
        # Figure out indents
        max_param_length = max([len(k) for k in info_dict.keys()])
        max_type_length = max([v['len']['type'] for v in info_dict.values()])
        # Print akin to the argparser
        for k, v in info_dict.items():
            print(f'    {k}' + (' ' * (max_param_length - v["len"]["name"] + self._max_indent)) +
                  f'{v["type"]}' + (' ' * (max_type_length - v["len"]["type"] + self._max_indent)) +
                  f'{v["desc"]} {v["default"]}')
        # Blank for spacing :-/
        print('')

    def _extract_enum_types(self, typed):
        """Takes a high level type and recursively extracts any enum types

        *Args*:

            typed: highest level type

        *Returns*:

            return_list: list of nums (dot notation of module_path.enum_name)

        """
        return_list = []
        if hasattr(typed, '__args__'):
            for val in typed.__args__:
                recurse_return = self._extract_enum_types(val)
                if isinstance(recurse_return, list):
                    return_list.extend(recurse_return)
                else:
                    return_list.append(self._extract_enum_types(val))
        elif isinstance(typed, EnumMeta):
            return f'{typed.__module__}.{typed.__name__}'
        return return_list

    @staticmethod
    def _get_enum_from_sys_modules(enum_name):
        """Gets the enum class from a dot notation name

        *Args*:

            enum_name: dot notation enum name

        *Returns*:

            module: enum class

        """
        # Split on dot notation
        split_string = enum_name.split('.')
        module = None
        for idx, val in enumerate(split_string):
            # idx = 0 will always be a call to the sys.modules dict
            if idx == 0:
                module = sys.modules[val]
            # all other idx are paths along the module that need to be traversed
            # idx = -1 will always be the final Enum object name we want to grab (final getattr call)
            else:
                module = getattr(module, val)
        return module


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

    def payload(self, input_classes, path, cmd_args, deps):
        """Builds the payload from config files

        Public exposed call to build the payload and set any command line overrides

        *Args*:

            input_classes: list of backend classes
            path: path to config file(s)
            cmd_args: command line overrides
            deps: dictionary of config dependencies

        *Returns*:

            payload: dictionary of all mapped parameters

        """
        payload = self._payload(input_classes, path, deps, root=True)
        payload = self._handle_overrides(payload, cmd_args)
        return payload

    def _payload(self, input_classes, path, deps, root=False):
        """Private call to construct the payload

        Main function call that builds out the payload from config files of multiple types. It handles
        various file types and also composition of config files via a recursive calls

        *Args*:
            input_classes: list of backend classes
            path: path to config file(s)
            deps: dictionary of config dependencies

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
        # Check and? update the dependencies
        deps = self._handle_dependencies(deps, path, root)
        payload = {}
        if 'config' in base_payload:
            payload = self._handle_includes(
                base_payload, config_extension, input_classes, path, payload, deps)
        payload = self._update_payload(base_payload, input_classes, payload)
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
        if root and path in deps.get('paths'):
            raise ValueError(f'Duplicate Read -- Config file {path} has already been encountered. '
                             f'Please remove duplicate reads of config files.')
        elif path in deps.get('paths') or path in deps.get('rel_paths'):
            raise ValueError(f'Cyclical Dependency -- Config file {path} has already been encountered. '
                             f'Please remove cyclical dependencies between config files.')
        else:
            # Update the dependency lists
            deps.get('paths').append(path)
            deps.get('rel_paths').append(os.path.basename(path))
            if root:
                deps.get('roots').append(path)
        return deps

    def _handle_includes(self, base_payload, config_extension, input_classes, path, payload, deps):  # pylint: disable=too-many-arguments
        """Handles config composition

        For all of the config tags in the config file this function will recursively call the payload function
        with the composition path to get the additional payload(s) from the composed file(s)

        *Args*:

            base_payload: base payload that has a config kwarg
            config_extension: file type
            input_classes: defined backend classes
            path: path to base file
            payload: payload pulled from composed files
            deps: dictionary of config dependencies

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
            included_params.update(self._payload(input_classes, abs_inc_path, deps))
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

        *Args*:

            payload: current payload dictionary
            dict_key: dictionary key to check
            val_name: value name to update
            value: value to update

        *Returns*:

            payload: updated payload dictionary

        """
        if not hasattr(payload, dict_key):
            payload.update({dict_key: {}})
        payload[dict_key].update({val_name: value})
        return payload
